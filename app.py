import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
from chromadb import PersistentClient
from tiktoken import Tokenizer
import openai

# Initialize OpenAI client
client = OpenAI()

# Initialize ChromaDB client
chroma_db = PersistentClient(path="./chroma_db")

# Streamlit UI
st.title("AI Document Assistant")
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_file is not None:
    # Read the PDF
    pdf = PdfReader(uploaded_file)

    # Extract text and break into chunks
    text_chunks = []
    for page in pdf.pages:
        text = page.extract_text()
        for i in range(0, len(text), 500):
            text_chunks.append(text[i:i+500])

    # Generate embeddings for each chunk and store in ChromaDB
    for chunk in text_chunks:
        response = client.text_embedding.create(
            model="text-embedding-3-small",
            text=chunk
        )
        embedding = response.embedding
        chroma_db.insert(chunk, embedding)

    # Get user query
    query = st.text_input("Enter your query")

    if query:
        # Generate embedding for the query
        response = client.text_embedding.create(
            model="text-embedding-3-small",
            text=query
        )
        query_embedding = response.embedding

        # Retrieve top 3 most relevant chunks
        relevant_chunks = chroma_db.query(query_embedding, top_k=3)

        # Construct the prompt
        prompt = "\n".join([chunk for chunk, _ in relevant_chunks]) + "\n" + query

        # Generate the answer
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Display the answer
        st.write(response.choices[0].message.content)