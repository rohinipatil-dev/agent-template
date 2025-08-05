import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import chromadb
from chromadb.config import Settings
import tiktoken

# Initialize OpenAI client
client = OpenAI()

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="docs")

def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def generate_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )
        embeddings.append(response.data[0].embedding)
    return embeddings

def store_in_chromadb(chunks, embeddings):
    ids = [f"id_{i}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids
    )

def retrieve_relevant_chunks(query_embedding, n_results=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return [result.document for result in results]

def generate_answer(context, query):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": context},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content

def main():
    st.title("AI Agent with RAG model")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file is not None:
        text = extract_text_from_pdf(uploaded_file)
        chunks = chunk_text(text)
        embeddings = generate_embeddings(chunks)
        store_in_chromadb(chunks, embeddings)
        st.success("PDF uploaded and processed successfully.")
        
        query = st.text_input("Enter your question:")
        if query:
            encoding = tiktoken.get_encoding("cl100k_base")
            query_embedding = client.embeddings.create(
                model="text-embedding-3-small",
                input=query
            ).data[0].embedding
            relevant_chunks = retrieve_relevant_chunks(query_embedding)
            context = " ".join(relevant_chunks)
            answer = generate_answer(context, query)
            st.write(answer)

if __name__ == "__main__":
    main()