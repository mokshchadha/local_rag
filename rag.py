from utils import connect_db

def retrieve_and_generate_response(query):
    conn = connect_db()
    cur = conn.cursor()
    
    # Embed the query using the ollama_embed function
    cur.execute("""
        SELECT ollama_embed('nomic-embed-text', %s);
    """, (query,))
    query_embedding = cur.fetchone()[0]
    
    # Retrieve relevant documents based on cosine distance
    cur.execute("""
        SELECT title, content, 1 - (embedding <=> %s) AS similarity
        FROM documents
        ORDER BY similarity DESC
        LIMIT 5;
    """, (query_embedding,))
    
    rows = cur.fetchall()
    
    # Prepare the context for generating the response
    context = "\n\n".join([f"Title: {row[0]}\nContent: {row[1]}" for row in rows])
    
    # Generate the response using the ollama_generate function
    cur.execute("""
        SELECT ai.ollama_generate('mistral', %s);
    """, (f"Query: {query}\nContext: {context}",))
    
    response = cur.fetchone()[0]
    print(f"Response: {response}")
    
    cur.close()
    conn.close()

def main():
    retrieve_and_generate_response("Tell me about landmarks in Seoul")

if __name__ == "__main__":
    main()