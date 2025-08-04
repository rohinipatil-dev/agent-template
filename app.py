import streamlit as st
import PyPDF2
import faiss
import numpy as np
from openai import OpenAI
from tiktoken import Tokenizer

# Initialize OpenAI client
client = OpenAI()

# Initialize tokenizer
tokenizer = Tokenizer()

# Streamlit UI
st.title("AI Document Assistant")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
if uploaded_file is not None:
    pdf = PyPDF2.PdfReader(uploaded_file)
    document_text = ""
    for page in pdf.pages:
        document_text += page.extract_text()

    # Chunk the document text
    chunks = [document_text[i:i+500] for i in range(0, len(document_text), 500)]

    # Generate embeddings for each chunk
    embeddings = []
    for chunk in chunks:
        tokens = tokenizer.encode(chunk)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            tokens=tokens
        )
        embeddings.append(response.embeddings)

    # Store embeddings in a FAISS index
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))

    # User query
    query = st.text_input("Enter your query")
    if query:
        # Generate an embedding for the query
        tokens = tokenizer.encode(query)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            tokens=tokens
        )
        query_embedding = response.embeddings

        # Retrieve the top 3 most relevant chunks
        D, I = index.search(np.array([query_embedding]), 3)
        relevant_chunks = [chunks[i] for i in I[0]]

        # Construct a prompt that includes only these chunks as context along with the user query
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for chunk in relevant_chunks:
            messages.append({"role": "document", "content": chunk})
        messages.append({"role": "user", "content": query})

        # Generate the answer
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        st.write(response.choices[0].message.content)