import json
import sqlite3

# lecture du json
with open('Livres.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Connexion à la base de données
conn = sqlite3.connect('fichier.db')
cursor = conn.cursor()

# creation des tables
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

# Insetion de données
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
