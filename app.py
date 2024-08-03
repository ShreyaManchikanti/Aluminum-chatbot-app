import streamlit as st
import numpy as np
import openai
import json
import requests

def get_openai_key(email):
    response = requests.post(
        "http://52.66.239.27:8504/get_keys",
        json={"email": email}
    )
    return response.json().get("openai_key")

email = "shreya.manchikanti_2025@gmail.com"
openai.api_key = get_openai_key(email)

def load_embeddings():
    with open('news_data.json', 'r') as f:
        articles = json.load(f)
    embeddings = np.load('embeddings.npy')
    return articles, embeddings

def get_closest_article(query, articles, embeddings):
    query_embedding = openai.Embedding.create(input=[query], model="text-embedding-ada-002")['data'][0]['embedding']
    distances = np.linalg.norm(embeddings - np.array(query_embedding), axis=1)
    closest_article_idx = np.argmin(distances)
    return articles[closest_article_idx]

articles, embeddings = load_embeddings()

st.title("Aluminium Industry News Chatbot")
query = st.text_input("Enter your query about the Aluminium Industry:")

if query:
    article = get_closest_article(query, articles, embeddings)
    st.write("### " + article['title'])
    st.write(article['summary'])
    st.write("Published on: " + article['date'])
