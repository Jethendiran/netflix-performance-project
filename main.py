from fastapi import FastAPI

app = FastAPI()

movies = [
    {"title": "Inception", "genre": "Sci-Fi", "cast": "Leonardo DiCaprio", "year": 2010},
    {"title": "Titanic", "genre": "Romance", "cast": "Leonardo DiCaprio", "year": 1997},
    {"title": "Avengers", "genre": "Action", "cast": "Robert Downey Jr.", "year": 2012},
    {"title": "Interstellar", "genre": "Sci-Fi", "cast": "Matthew McConaughey", "year": 2014},
]

@app.get("/")
def home():
    return {"message": "API is running"}

@app.get("/genre/{genre}")
def get_by_genre(genre: str):
    return [m for m in movies if genre.lower() in m["genre"].lower()]

@app.get("/actor/{actor}")
def get_by_actor(actor: str):
    return [m for m in movies if actor.lower() in m["cast"].lower()]

@app.get("/recent/{year}")
def get_recent(year: int):
    return [m for m in movies if m["year"] == year]

@app.get("/search")
def search(term: str):
    return [
        m for m in movies
        if term.lower() in m["title"].lower()
        or term.lower() in m["genre"].lower()
    ]