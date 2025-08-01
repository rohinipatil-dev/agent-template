import streamlit as st
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

# OpenAI client
client = OpenAI()

# Function to get trending news
def get_trending_news():
    url = "https://www.cybersecurity-insiders.com/category/cyber-security-news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h3', class_='entry-title td-module-title')
    return [headline.text for headline in headlines]

# Function to generate blog content
def generate_blog_content(headline):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Write a blog post about the following cybersecurity news: {headline}"}
    ]
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    return response.choices[0].message.content

# Streamlit app
def main():
    st.title("Cybersecurity News Blog")
    st.write("This website automatically generates blog posts based on trending cybersecurity news.")

    news_headlines = get_trending_news()

    for headline in news_headlines:
        st.subheader(headline)
        blog_content = generate_blog_content(headline)
        st.write(blog_content)

if __name__ == "__main__":
    main()