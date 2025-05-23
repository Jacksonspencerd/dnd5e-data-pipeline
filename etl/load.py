# write to sqlite database
import sqlite3
import logging

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
                    description TEXT,
                    classes TEXT,
                    higher_level TEXT,
                    subclasses TEXT
                    )""")
    
def load_spells(conn, spells_data):
    inserted_rows = 0
    cursor = conn.cursor()
    for spell in spells_data:
        cursor.execute("""
        INSERT OR REPLACE INTO spells (id, name, level, school, casting_time, range, components, material, duration, concentration, ritual, description, classes, higher_level, subclasses)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
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
         spell["description"],
         spell["classes"],
         spell["higher_level"],
         spell["subclasses"]
         ))
        inserted_rows += 1
    conn.commit()
    logging.info(f"Inserted {inserted_rows} rows into the spells table.")
    