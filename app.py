import os
import streamlit as st
from io import BytesIO
import PyPDF2

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI

# Set your OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Initialize ChromaDB with OpenAI embeddings
embedding_fn = OpenAIEmbeddingFunction(api_key=openai_api_key)
chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="pdf_chunks", embedding_function=embedding_fn)

# Streamlit UI
st.title("PDF Question Answering (RAG using ChromaDB)")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
    return " ".join(page.extract_text() or "" for page in reader.pages)

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    return splitter.split_text(text)

def store_chunks(chunks):
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, ids=ids)

def retrieve_relevant_chunks(query, top_k=3):
    results = collection.query(query_texts=[query], n_results=top_k)
    return results["documents"][0] if results["documents"] else []

def generate_answer(query, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = f"Use the following content to answer the question.\n\n{context}\n\nQuestion: {query}"
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

if uploaded_file:
    st.success("PDF uploaded successfully.")
    pdf_text = extract_text(uploaded_file)
    chunks = chunk_text(pdf_text)
    collection.delete()  # Clear previous data
    store_chunks(chunks)

    user_query = st.text_input("Ask a question about the PDF content")
    if user_query:
        relevant = retrieve_relevant_chunks(user_query)
        answer = generate_answer(user_query, relevant)
        st.markdown("### Answer")
        st.write(answer)
