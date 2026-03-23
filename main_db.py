from fastapi import FastAPI
from psycopg2 import pool
import psycopg2

app = FastAPI()

# ===== Connection Pool Setup =====
DB_POOL = psycopg2.pool.SimpleConnectionPool(
    1, 20,  # min 1, max 20 connections
    dbname="movies",
    user="postgres",
    password="YOUR_DB_PASSWORD",
    host="127.0.0.1",
    port="5432"
)

def get_connection():
    return DB_POOL.getconn()

def release_connection(conn):
    DB_POOL.putconn(conn)

# ===== API Endpoints with Pagination =====

@app.get("/genre/{genre}")
def get_by_genre(genre: str, limit: int = 50, offset: int = 0):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM movies WHERE genre ILIKE %s LIMIT %s OFFSET %s",
        (f"%{genre}%", limit, offset)
    )
    rows = cur.fetchall()
    cur.close()
    release_connection(conn)
    return rows

@app.get("/actor/{actor}")
def get_by_actor(actor: str, limit: int = 50, offset: int = 0):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM movies WHERE cast ILIKE %s LIMIT %s OFFSET %s",
        (f"%{actor}%", limit, offset)
    )
    rows = cur.fetchall()
    cur.close()
    release_connection(conn)
    return rows

@app.get("/recent/{year}")
def get_recent(year: int, limit: int = 50, offset: int = 0):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM movies WHERE release_year = %s LIMIT %s OFFSET %s",
        (year, limit, offset)
    )
    rows = cur.fetchall()
    cur.close()
    release_connection(conn)
    return rows

@app.get("/search")
def search(term: str, limit: int = 50, offset: int = 0):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT * FROM movies 
           WHERE title ILIKE %s OR description ILIKE %s
           LIMIT %s OFFSET %s""",
        (f"%{term}%", f"%{term}%", limit, offset)
    )
    rows = cur.fetchall()
    cur.close()
    release_connection(conn)
    return rows