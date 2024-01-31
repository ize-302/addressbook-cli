import sqlite3
from sqlite3 import Error
import os

db_file = "data.db"


conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute(
        'CREATE TABLE IF NOT EXISTS addresses (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT, created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'
)
conn.commit()


