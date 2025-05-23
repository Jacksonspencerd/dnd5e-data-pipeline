import sqlite3
import argparse
import logging
from etl.extract import get_spells
from etl.transform import transform_spells
from etl.load import create_tables, load_spells

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline(db_path, sleep_time):
    logging.info("Starting ETL pipeline...")

    if not spells:
        logger.error("No spells data found. Exiting.")
        return # exit early if no data

    # Extract
    spells_raw = get_spells(sleep_time)
    logging.info(f"Extracted {len(spells_raw)} spells.")
    if not spells_raw:
        logging.error("No spells data found. Exiting.")
        return
    
    # Transform
    logging.info("Transforming data...")
    spells_clean = transform_spells(spells_raw)
    logging.info(f"Transformed {len(spells_clean)} spells.")

    # Load
    logging.info("Loading data into the database...")
    conn = sqlite3.connect('spells.db')
    create_tables(conn)
    load_spells(conn, spells_clean)
    conn.close()
    logging.info("Data loaded successfully.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETL pipeline for D&D spells.")
    parser.add_argument("--db", type=str, default="spells.db", help="SQLite database file.")
    parser.add_argument("--sleep", type=float, default=0.1, help="Sleep time between API calls.")
    args = parser.parse_args()
    
    run_pipeline(args.db, args.sleep)
    logging.info("ETL pipeline completed.")


