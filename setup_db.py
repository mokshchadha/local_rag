from utils import connect_db

dummy_data = [
    {"title": "Seoul Tower", "content": "Seoul Tower is a communication and observation tower located on Namsan Mountain in central Seoul, South Korea."},
    {"title": "Gwanghwamun Gate", "content": "Gwanghwamun is the main and largest gate of Gyeongbokgung Palace, in Jongno-gu, Seoul, South Korea."},
    {"title": "Bukchon Hanok Village", "content": "Bukchon Hanok Village is a Korean traditional village in Seoul with a long history."},
    {"title": "Myeong-dong Shopping Street", "content": "Myeong-dong is one of the primary shopping districts in Seoul, South Korea."},
    {"title": "Dongdaemun Design Plaza", "content": "The Dongdaemun Design Plaza is a major urban development landmark in Seoul, South Korea."}
]
  

def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            title TEXT,
            content TEXT,
            embedding VECTOR(768)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_data():
    conn = connect_db()
    cur = conn.cursor()

    for doc in dummy_data:
        cur.execute("""
            INSERT INTO documents (title, content, embedding)
            VALUES (
                %(title)s,
                %(content)s,
                ollama_embed('nomic-embed-text', concat(%(title)s, ' - ', %(content)s))
            )
        """, doc)

    conn.commit()
    cur.close()
    conn.close()


def fetch_data():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT title, content, vector_dims(embedding) 
        FROM documents;
    """)
    rows = cur.fetchall()
    for row in rows:
        print(f"Title: {row[0]}, Content: {row[1]}, Embedding Dimensions: {row[2]}")
    cur.close()
    conn.close()

def main():
    create_table()
    insert_data()
    fetch_data()

if __name__ == "__main__":
    main()