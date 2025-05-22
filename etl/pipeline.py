import sqlite3
from extract import get_spells
from transform import transform_spells
from load import create_tables, load_spells

def run_pipeline():
    print("Starting ETL pipeline...")

    # Extract
    print("Extracting data...")
    spells_data = get_spells()
    print("sample spells_data", spells_data)

    if not spells_data:
        print("No data extracted. Exiting pipeline.")
        return
    
    # Transform
    print("Transforming data...")
    transformed_data = transform_spells(spells_data)

    # Load
    print("Loading data into database...")
    conn = sqlite3.connect('spells.db')
    create_tables(conn)
    load_spells(conn, transformed_data)
    conn.close()


    print("ETL pipeline completed successfully.")

if __name__ == "__main__":
    run_pipeline()



