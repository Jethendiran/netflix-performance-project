from fastapi import FastAPI, Query
import psycopg2
from psycopg2.extras import RealDictCursor

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "YOUR_POSTGRES_PASSWORD"
DB_HOST = "127.0.0.1"
DB_PORT = "9470"

app = FastAPI(title="Netflix API")

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        cursor_factory=RealDictCursor
    )

@app.get("/genre/{genre}")
def get_by_genre(genre: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies WHERE genre ILIKE %s LIMIT 50", (f"%{genre}%",))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

@app.get("/actor/{actor}")
def get_by_actor(actor: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies WHERE director ILIKE %s LIMIT 50", (f"%{actor}%",))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

@app.get("/recent/{year}")
def get_recent(year: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies WHERE release_year = %s LIMIT 50", (year,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

@app.get("/search")
def search(q: str = Query(...)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM movies WHERE title ILIKE %s OR director ILIKE %s OR genre ILIKE %s LIMIT 50",
        (f"%{q}%", f"%{q}%", f"%{q}%")
    )
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results