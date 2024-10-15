import psycopg2
from psycopg2.extras import execute_values
import requests
import json

# Ollama API endpoint
OLLAMA_API = "http://localhost:11434/api/embeddings"

# Database connection parameters
DB_PARAMS = {
    "dbname": "mydb",
    "user": "myuser",
    "password": "mypassword",
    "host": "localhost",
    "port": "5444"
}

def get_embedding(text):
    response = requests.post(OLLAMA_API, json={"model": "all-minilm", "prompt": text})
    return response.json()['embedding']

def insert_documents(documents):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()

    try:
        data = [(doc['title'], doc['content'], get_embedding(doc['content'])) for doc in documents]
        execute_values(cur, """
            INSERT INTO documents (title, content, embedding)
            VALUES %s
        """, data)
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

# Example usage
documents = [
    {"title": "Seoul Tower", "content": "Seoul Tower is a communication and observation tower located on Namsan Mountain in central Seoul, South Korea."},
    {"title": "Gwanghwamun Gate", "content": "Gwanghwamun is the main and largest gate of Gyeongbokgung Palace, in Jongno-gu, Seoul, South Korea."},
    {"title": "Bukchon Hanok Village", "content": "Bukchon Hanok Village is a Korean traditional village in Seoul with a long history."},
    {"title": "Myeong-dong Shopping Street", "content": "Myeong-dong is one of the primary shopping districts in Seoul, South Korea."},
    {"title": "Dongdaemun Design Plaza", "content": "The Dongdaemun Design Plaza is a major urban development landmark in Seoul, South Korea."}

]

insert_documents(documents)