import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import chromadb
import tiktoken

from openai.api_resources import Completion

# Create OpenAI client
client = OpenAI()

# Create ChromaDB client
db = chromadb.PersistentClient(path="./chroma_db")

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# Function to chunk text
def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

# Function to generate embeddings
def generate_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        response = client.completions.create(
            model="text-embedding-3-small",
            prompt=chunk,
            max_tokens=1
        )
        embeddings.append(response.choices[0].message.content)
    return embeddings

# Function to store embeddings in ChromaDB
def store_embeddings(embeddings, chunks):
    for embedding, chunk in zip(embeddings, chunks):
        db.insert(embedding, chunk)

# Function to retrieve relevant chunks
def retrieve_chunks(query):
    query_embedding = generate_embeddings([query])[0]
    results = db.search(query_embedding, k=3)
    return [result[1] for result in results]

# Function to generate answer
def generate_answer(context, query):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for chunk in context:
        messages.append({"role": "assistant", "content": chunk})
    messages.append({"role": "user", "content": query})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("AI Agent")
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)
    chunks = chunk_text(text)
    embeddings = generate_embeddings(chunks)
    store_embeddings(embeddings, chunks)
    query = st.text_input("Enter your question")
    if st.button("Ask"):
        context = retrieve_chunks(query)
        answer = generate_answer(context, query)
        st.write(answer)