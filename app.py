import os
from fastapi import FastAPI
import psycopg2

app = FastAPI()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://devops:secret123@localhost:5432/counter")


def get_count():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS counter (id SERIAL PRIMARY KEY, value INT DEFAULT 0);")
    cur.execute("SELECT value FROM counter WHERE id = 1;")
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO counter (id, value) VALUES (1, 0);")
        conn.commit()
        result = 0
    else:
        result = row[0]
    cur.close()
    conn.close()
    return result


def set_count(value):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("UPDATE counter SET value = %s WHERE id = 1;", (value,))
    conn.commit()
    cur.close()
    conn.close()


@app.get("/")
def read_root():
    return {"counter": get_count()}


@app.post("/increment")
def increment():
    current = get_count() + 1
    set_count(current)
    return {"counter": current}
