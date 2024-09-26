import psycopg2


def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="mydb",
        user="myuser",
        password="mypassword",
        port="5444"
  )


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