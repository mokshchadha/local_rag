import psycopg2
import requests

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

def connect_db():
    return psycopg2.connect(**DB_PARAMS)

def get_embedding(text):
    response = requests.post(OLLAMA_API, json={"model": "all-minilm", "prompt": text})
    return response.json()['embedding']

def generate_response(prompt):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "llama3.2",
        "prompt": prompt
    })
    return response.json()['response']

def retrieve_and_generate_response(query):
    conn = connect_db()
    cur = conn.cursor()
    
    # Embed the query
    query_embedding = get_embedding(query)
    
    # Format the embedding for pg_vector
    embedding_string = f"[{','.join(map(str, query_embedding))}]"
    
    # Retrieve relevant documents using cosine similarity
    cur.execute("""
        SELECT title, content, 1 - (embedding <=> %s::vector) AS similarity
        FROM documents
        ORDER BY similarity DESC
        LIMIT 5;
    """, (embedding_string,))
    
    rows = cur.fetchall()
    print("embeddings in databse")
    print(rows)

    
    # Prepare the context for generating the response
    context = "\n\n".join([f"Title: {row[0]}\nContent: {row[1]}" for row in rows])
    
    # Generate the response
    prompt = f"Query: {query}\nContext: {context}\nPlease provide a concise answer based on the given context."
    response = generate_response(prompt)
    
    print(f"Response: {response}")
    
    cur.close()
    conn.close()

def main():
    retrieve_and_generate_response("Tell me about landmarks in Seoul")

if __name__ == "__main__":
    main()