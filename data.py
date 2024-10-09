from utils import connect_db

dummy_data = [
    {"title": "Seoul Tower", "content": "Seoul Tower is a communication and observation tower located on Namsan Mountain in central Seoul, South Korea."},
    {"title": "Gwanghwamun Gate", "content": "Gwanghwamun is the main and largest gate of Gyeongbokgung Palace, in Jongno-gu, Seoul, South Korea."},
    {"title": "Bukchon Hanok Village", "content": "Bukchon Hanok Village is a Korean traditional village in Seoul with a long history."},
    {"title": "Myeong-dong Shopping Street", "content": "Myeong-dong is one of the primary shopping districts in Seoul, South Korea."},
    {"title": "Dongdaemun Design Plaza", "content": "The Dongdaemun Design Plaza is a major urban development landmark in Seoul, South Korea."}
]
  

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