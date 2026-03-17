import csv
import psycopg2

# Connect to Cloud SQL PostgreSQL
conn = psycopg2.connect(
    host="127.0.0.1",
    port="9470",  # The port Cloud SQL Proxy is using
    dbname="postgres",
    user="postgres",
    password="YOUR_DB_PASSWORD"  # Replace with your actual postgres password
)

cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS movies (
    show_id TEXT,
    type TEXT,
    title TEXT,
    director TEXT,
    country TEXT,
    release_year INT,
    rating TEXT,
    duration TEXT,
    listed_in TEXT
)
""")
conn.commit()

# Open CSV and insert data
with open("../data/netflix_titles.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute("""
        INSERT INTO movies (show_id, type, title, director, country, release_year, rating, duration, listed_in)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row["show_id"],
            row["type"],
            row["title"],
            row["director"],
            row["country"],
            row["release_year"] if row["release_year"] != "" else None,
            row["rating"],
            row["duration"],
            row["listed_in"]
        ))

conn.commit()
cur.close()
conn.close()

print("CSV data imported successfully!")