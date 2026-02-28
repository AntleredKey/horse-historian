import requests
import sqlite3
import os
url = "https://raw.githubusercontent.com/AntleredKey/horse-historian/main/horseraces.db"
db_path = "./horseraces.db"
temp_db = "./tempdb.db"

def workingtitle():
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

    with open(temp_db, 'wb') as f:
        f.write(response.content)
    os.replace(temp_db, db_path)



def fetch_data_from_github():
    """Fetches data (e.g., JSON) from the GitHub raw URL."""
    print("trying to fetch data")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def update_database(data, db_path):
    """Connects to SQLite and updates the data."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if it doesn't exist (adjust schema as needed)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id TEXT PRIMARY KEY,
            name TEXT,
            value INTEGER,
            last_updated TEXT
        )
    ''')

    # Example: Inserting or updating data
    # This assumes 'data' is a list of dictionaries with 'id', 'name', 'value', 'last_updated' keys
    for item in data:
        cursor.execute('''
            INSERT OR REPLACE INTO items (id, name, value, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (item['id'], item['name'], item['value'], item['last_updated']))

    conn.commit()
    conn.close()
    print("Database updated successfully.")

def updatedb():
    workingtitle()