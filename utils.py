import psycopg2

def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="mydb",
        user="myuser",
        password="mypassword",
        port="5444"
  )


