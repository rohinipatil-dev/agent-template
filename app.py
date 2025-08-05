import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import chromadb
from chromadb.config import Settings
import tiktoken

@st.cache(allow_output_mutation=True)
def get_openai_client():
    return OpenAI()

@st.cache(allow_output_mutation=True)
def get_chromadb_client():
    return chromadb.PersistentClient(path="./chroma_db")

def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def generate_embeddings(chunks, client):
    embeddings = []
    for chunk in chunks:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=chunk
        )
        embeddings.append(response.data[0].embedding)
    return embeddings

def store_in_chromadb(chunks, embeddings, collection):
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"id_{i}"]
        )

def get_relevant_chunks(query_embedding, collection, n_results=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return [result.document for result in results]

def generate_answer(query, context, client):
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
    st.title("AI Agent with RAG Model")
    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
    if uploaded_file is not None:
        client = get_openai_client()
        db_client = get_chromadb_client()
        collection = db_client.get_or_create_collection(name="docs")
        text = extract_text_from_pdf(uploaded_file)
        chunks = chunk_text(text)
        embeddings = generate_embeddings(chunks, client)
        store_in_chromadb(chunks, embeddings, collection)
        query = st.text_input("Ask a question:")
        if query:
            encoding = tiktoken.get_encoding("cl100k_base")
            query_embedding = client.embeddings.create(
                model="text-embedding-3-small",
                input=query
            ).data[0].embedding
            relevant_chunks = get_relevant_chunks(query_embedding, collection)
            context = " ".join(relevant_chunks)
            answer = generate_answer(query, context, client)
            st.write(answer)

if __name__ == "__main__":
    main()