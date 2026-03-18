import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import numpy as np

print("📂 Reading CSV file...")
# Read CSV with proper encoding
df = pd.read_csv(r'C:\Users\Madan kumar\Downloads\archive\netflix_titles.csv', encoding='latin1')

print(f"✅ Read {len(df)} rows")

# Rename 'listed_in' column to 'genre' to match the table
df.rename(columns={'listed_in': 'genre'}, inplace=True)

# Handle empty dates - convert empty strings to None (NULL in SQL)
df['date_added'] = df['date_added'].replace('', None)

# Handle any other NaN values
df = df.fillna('')

print("📥 Connecting to database...")
# Database connection
conn = psycopg2.connect(
    dbname="movies",
    user="postgres",
    password="0000",
    host="127.0.0.1",
    port="5432"
)
cur = conn.cursor()

# Clear existing data
cur.execute("DELETE FROM movies;")
print("🧹 Cleared existing data")

print("📥 Inserting data into PostgreSQL...")
# Prepare data for insertion
data = [tuple(x) for x in df.values]

# Insert data - note quotes around "cast"
insert_query = """
INSERT INTO movies (
    show_id, type, title, director, "cast", country, 
    date_added, release_year, rating, duration, genre, description
) VALUES %s
"""

execute_values(cur, insert_query, data)
conn.commit()
print(f"✅ Successfully inserted {len(data)} rows")

cur.close()
conn.close()
print("✅ Done!")