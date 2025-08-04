import streamlit as st
from openai import OpenAI
from PyPDF2.pdf import PdfReader
import chromadb
from tiktoken import Tokenizer

# Create OpenAI client
client = OpenAI()

# Initialize ChromaDB
db = chromadb.ChromaDB()

# Initialize tokenizer
tokenizer = Tokenizer()

# Streamlit app
def main():
    st.title("AI Document Assistant")

    uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")
    if uploaded_file is not None:
        # Read PDF
        pdf = PdfReader(uploaded_file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

        # Chunk the text into ~500-character segments
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]

        # Generate embeddings for each chunk
        for chunk in chunks:
            tokens = tokenizer.tokenize(chunk)
            response = client.text_embedding.create(
                model="text-embedding-3-small",
                tokens=tokens
            )
            embedding = response.embeddings[0]
            db.insert(embedding, chunk)

        st.success("Document uploaded and processed successfully!")

    query = st.text_input("Enter your query")
    if st.button("Get Answer"):
        if query:
            # Generate an embedding for the query
            tokens = tokenizer.tokenize(query)
            response = client.text_embedding.create(
                model="text-embedding-3-small",
                tokens=tokens
            )
            query_embedding = response.embeddings[0]

            # Retrieve the top 3 most relevant chunks
            results = db.query(query_embedding, k=3)
            context = " ".join([result[1] for result in results])

            # Construct a prompt
            prompt = {
                "role": "system",
                "content": "You are a helpful assistant."
            }
            user_message = {
                "role": "user",
                "content": query
            }
            assistant_context = {
                "role": "assistant",
                "content": context
            }

            # Generate the answer
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[prompt, user_message, assistant_context]
            )
            answer = response.choices[0].message.content

            st.write(answer)
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()