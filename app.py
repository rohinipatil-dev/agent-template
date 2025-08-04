import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
from tiktoken import Tokenizer
import chromadb

# Initialize OpenAI client
client = OpenAI()

# Initialize ChromaDB client
db = chromadb.PersistentClient(path="./chroma_db")

# Initialize tokenizer
tokenizer = Tokenizer()

@st.cache(allow_output_mutation=True)
def get_embeddings(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        documents=[{"text": text}]
    )
    return response.embeddings[0].embedding

def upload_pdf():
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file is not None:
        pdf = PdfReader(uploaded_file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text
    return None

def chunk_text(text, chunk_size=500):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def store_embeddings(chunks):
    for chunk in chunks:
        embedding = get_embeddings(chunk)
        db.insert(embedding, chunk)

def retrieve_chunks(query):
    query_embedding = get_embeddings(query)
    results = db.nearest(query_embedding, n=3)
    return [result[1] for result in results]

def generate_answer(contexts, query):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for context in contexts:
        messages.append({"role": "user", "content": context})
    messages.append({"role": "user", "content": query})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content

def main():
    st.title("AI Document Assistant")
    text = upload_pdf()
    if text is not None:
        chunks = chunk_text(text)
        store_embeddings(chunks)
        query = st.text_input("Enter your query")
        if query:
            contexts = retrieve_chunks(query)
            answer = generate_answer(contexts, query)
            st.write(answer)

if __name__ == "__main__":
    main()