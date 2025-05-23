import streamlit as st
import sqlite3
import pandas as pd
import os
from etl.pipeline import run_pipeline

DB_PATH = "spells.db"

# Check if the database file exists
if not os.path.exists(DB_PATH):
    from etl.pipeline import run_pipeline
    run_pipeline(DB_PATH, sleep_time=0.1)

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM spells", conn)
    conn.close()
    return df

def main():
    st.title("D&D 5E Spellbook")
    st.markdown("Explore spells from the D&D 5E API with filters and search.")

    df = load_data()
    if df.empty:
        st.warning("No spells data found. Please run the ETL process to load data.")
        return

    # Sidebar filters
    st.sidebar.header("Filter Spells")

    schools = sorted(df["school"].dropna().unique())
    levels = sorted(df["level"].dropna().unique())
    classes = sorted(df["classes"].dropna().unique())
    subclasses = sorted(df["subclasses"].dropna().unique())



    selected_school = st.sidebar.selectbox("School of Magic", ["All"] + schools)
    selected_level = st.sidebar.selectbox("Spell Level", ["All"] + [str(l) for l in levels])
    selected_class = st.sidebar.selectbox("Class", ["All"] + classes)
    selected_subclass = st.sidebar.selectbox("Subclass", ["All"] + subclasses)

    search = st.text_input("Search by name or description:")

    # --- Filtering ---
    filtered_df = df.copy()

    # Filter by class, subclass, school, and level
    if selected_class != "All":
        filtered_df = filtered_df[filtered_df["classes"] == selected_class]
    
    if selected_subclass != "All":
        filtered_df = filtered_df[filtered_df["subclasses"] == selected_subclass]

    if selected_school != "All":
        filtered_df = filtered_df[filtered_df["school"] == selected_school]

    if selected_level != "All":
        # Convert selected_level to int if needed
        try:
            level_int = int(selected_level)
            filtered_df = filtered_df[filtered_df["level"] == level_int]
        except ValueError:
            pass

    if search:
        filtered_df = filtered_df[
            filtered_df["name"].str.contains(search, case=False, na=False) |
            filtered_df["description"].str.contains(search, case=False, na=False)
        ]

    # --- Display ---
    st.markdown(f"### Showing {len(filtered_df)} matching spells")
    st.dataframe(filtered_df[[
        "name", "level", "school", "casting_time", "range", "components", "duration", "description", "classes", "higher_level", "subclasses"
    ]])

if __name__ == "__main__":
    main()
