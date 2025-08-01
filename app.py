import base64
import urllib.parse
import html
from openai import OpenAI
import streamlit as st

# OpenAI client
client = OpenAI()

def decode_base64(data):
    return base64.b64decode(data).decode('utf-8')

def decode_url(data):
    return urllib.parse.unquote(data)

def decode_html(data):
    return html.unescape(data)

st.title('Decode Encoded Strings')

# Select format
format = st.selectbox('Select format', ['Base64', 'URL', 'HTML'])

# Input field
data = st.text_input('Enter encoded string')

# Decode button
if st.button('Decode'):
    if format == 'Base64':
        try:
            decoded_data = decode_base64(data)
            st.success(f'Decoded String: {decoded_data}')
        except Exception as e:
            st.error(f'Error: {str(e)}')
    elif format == 'URL':
        try:
            decoded_data = decode_url(data)
            st.success(f'Decoded String: {decoded_data}')
        except Exception as e:
            st.error(f'Error: {str(e)}')
    elif format == 'HTML':
        try:
            decoded_data = decode_html(data)
            st.success(f'Decoded String: {decoded_data}')
        except Exception as e:
            st.error(f'Error: {str(e)}')