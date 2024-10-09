from utils import connect_db
from data import dummy_data 
from data import insert_data
from data import create_table



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