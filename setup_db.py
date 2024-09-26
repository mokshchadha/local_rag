from utils import connect_db

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