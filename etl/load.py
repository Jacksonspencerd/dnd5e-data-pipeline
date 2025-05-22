# write to sqlite database

import sqlite3

def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS spells (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    level INTEGER,
                    school TEXT,
                    casting_time TEXT,
                    range TEXT,
                    components TEXT,
                    material TEXT,
                    duration TEXT,
                    concentration BOOLEAN,
                    ritual BOOLEAN,
                    description TEXT
                    )""")
    
def load_spells(conn, spells_data):
    cursor = conn.cursor()
    for spell in spells_data:
        cursor.execute("""
        INSERT OR REPLACE INTO spells (id, name, level, school, casting_time, range, components, material, duration, concentration, ritual, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
         spell["index"], 
         spell["name"], 
         spell["level"], 
         spell["school"], 
         spell["casting_time"],
         spell["range"], 
         spell["components"], 
         spell["material"], 
         spell["duration"], 
         spell["concentration"], 
         spell["ritual"], 
         spell["description"]
         ))
    conn.commit()