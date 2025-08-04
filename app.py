import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import chromadb
import tiktoken
from openai.api_resources.experimental import text_embedding

# Initialize OpenAI client
client = OpenAI()

# Initialize ChromaDB persistent client
chroma_db = chromadb.PersistentClient(path="./chroma_db")

# Streamlit UI
st.title("AI Document Assistant")
uploaded_file = st.file_uploader("Upload a PDF document", type=['pdf'])

if uploaded_file is not None:
    # Read PDF
    pdf = PdfReader(uploaded_file)

    # Extract text and chunk into ~500-character segments
    chunks = []
    for page in pdf.pages:
        text = page.extract_text()
        chunks += [text[i:i+500] for i in range(0, len(text), 500)]

    # Generate embeddings for each chunk
    for chunk in chunks:
        response = client.text_embedding.create(
            model="text-embedding-3-small",
            document=chunk
        )
        embedding = response.embedding

        # Store in ChromaDB
        chroma_db.add_document(embedding, chunk)

    # User query
    query = st.text_input("Enter your query")

    if query:
        # Generate embedding for query
        response = client.text_embedding.create(
            model="text-embedding-3-small",
            document=query
        )
        query_embedding = response.embedding

        # Retrieve top 3 most relevant chunks
        top_chunks = chroma_db.search(query_embedding, num_results=3)

        # Construct prompt
        prompt = "\n".join([chunk[1] for chunk in top_chunks]) + "\n" + query

        # Generate answer
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}]
        )

        # Display answer
        st.write(response.choices[0].message.content)