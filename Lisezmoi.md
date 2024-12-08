
# Ce fichier Markdown explique comment installer les dépendances, créer et remplir la base de données, et exécuter l'application FastAPI localement avec Docker.
---
### FastAPI Books API

Cette application est une API FastAPI qui permet de gérer une collection de livres. Les données des livres sont stockées dans une base de données SQLite.

  from fastapi import FastAPI, HTTPException
  from pydantic import BaseModel
  from typing import List
  import sqlite3
  
  app = FastAPI()
  
  #### Connexion à la base de données
  def get_db_connection():
      conn = sqlite3.connect('fichier.db')
      conn.row_factory = sqlite3.Row
      return conn
  
  #### Modèles Pydantic
  class Book(BaseModel):
      id: int
      title: str
      content: str
      author: str
      date: str
  
  #### Routes
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

### De Json à Nouvelle base de données
import json
import sqlite3

#### lecture du json
with open('Livres.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

#### Connexion à la base de données
conn = sqlite3.connect('fichier.db')
cursor = conn.cursor()

#### creation des tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS auteurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_auteur TEXT UNIQUE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT,
    pitch TEXT,
    auteur_id INTEGER,
    date_public TEXT,
    FOREIGN KEY (auteur_id) REFERENCES auteurs (id)
)
''')

#### Insetion de données
for book in data:
    # Insérer l'auteur s'il n'existe pas déjà
    cursor.execute('INSERT OR IGNORE INTO auteurs (nom_auteur) VALUES (?)', (book['author'],))
    cursor.execute('SELECT id FROM auteurs WHERE nom_auteur = ?', (book['author'],))
    auteur_id = cursor.fetchone()[0]

    # livres
    cursor.execute('''
    INSERT INTO livres (id, titre, pitch, auteur_id, date_public)
    VALUES (?, ?, ?, ?, ?)
    ''', (book['id'], book['title'], book['content'], auteur_id, book['date']))

conn.commit()
conn.close()


## Utilisation
---

### Prérequis

- Python 3.11
- Docker 

### Exécuter le conteneur Docker :

**docker run -d -p 8000:8000 fastapi-books**

**L'API sera accessible à l'adresse http://127.0.0.1:8000**
