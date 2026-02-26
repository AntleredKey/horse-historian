import requests
import sqlite3
import json
url = "https://raw.githubusercontent.com/AntleredKey/horse-historian/main/horseraces.db"
db_path = "./horseraces.db"

def fetch_data_from_github():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def update_database(data, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id TEXT PRIMARY KEY,
            name TEXT,
            value INTEGER,
            last_updated TEXT
        )
    ''')
    for item in data:
        cursor.execute('''
            INSERT OR REPLACE INTO items (id, name, value, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (item['id'], item['name'], item['value'], item['last_updated']))
    conn.commit()
    conn.close()
    print("Database updated successfully.")

def updatedb():
    github_data = fetch_data_from_github()
    if github_data:
        update_database(github_data, db_path)