import openai
import json
import numpy as np
import requests

def get_openai_key(email):
    response = requests.post(
        "http://52.66.239.27:8504/get_keys",
        json={"email": email}
    )
    return response.json().get("openai_key")

email = "shreya.manchikanti_2025@gmail.com"
openai.api_key = get_openai_key(email)

with open('news_data.json', 'r') as f:
    articles = json.load(f)

texts = [article['summary'] for article in articles]
response = openai.Embedding.create(input=texts, model="text-embedding-ada-002")
embeddings = np.array([embedding['embedding'] for embedding in response['data']])

np.save('embeddings.npy', embeddings)
with open('news_data.json', 'w') as f:
    json.dump(articles, f)
