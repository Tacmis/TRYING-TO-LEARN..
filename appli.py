from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# Connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect('fichier.db')
    conn.row_factory = sqlite3.Row
    return conn

# Modèles Pydantic
class Book(BaseModel):
    id: int
    title: str
    content: str
    author: str
    date: str

# Routes
@app.get("/books", response_model=List[Book])
def read_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM livres').fetchall()
    conn.close()
    return [dict(book) for book in books]

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM livres WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    if book is None:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return dict(book)