import streamlit as st
import json
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
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()  # Return empty DataFrame if DB doesn't exist
    # Connect to the SQLite database and load data into a DataFrame
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM spells", conn)
    conn.close()
    return df

def get_unique_classes(df):
    class_set = set()
    for class_list in df["classes"]:
        if class_list:
            try:
                for cls in json.loads(class_list):
                    class_set.add(cls)
            except json.JSONDecodeError:
                pass 
    return sorted(class_set)

def get_unique_subclasses(df):
    subclass_set = set()
    for subclass_list in df["subclasses"]:
        if subclass_list:
            try:
                for subclass in json.loads(subclass_list):
                    subclass_set.add(subclass)
            except json.JSONDecodeError:
                pass
    return sorted(subclass_set)



def main():
    st.title("D&D 5E Spellbook")
    st.markdown("Explore spells from the D&D 5E API with filters and search.")

    df = load_data()
    if df.empty:
        st.warning("No spells data found. The API may be down or the database is empty.")
        return
    
    # get unique classes and subclasses
    all_classes = get_unique_classes(df)
    all_subclasses = get_unique_subclasses(df)

    selected_classes = st.sidebar.multiselect("Select Classes", all_classes, default=all_classes)
    selected_subclasses = st.sidebar.multiselect("Select Subclasses", all_subclasses, default=all_subclasses)

    # Filter the DataFrame based on selected classes and subclasses
    def class_filter(row):
        try:
            return selected_class in json.loads(row["classes"])
        except:
            return False
            
    def subclass_filter(row):
        try:
            return selected_subclass in json.loads(row["subclasses"])
        except:
            return False
        
    
    filtered_df = df[df.apply(class_filter, axis=1)]
    filtered_df = df[df.apply(subclass_filter, axis=1)]

    # --- Sidebar ---
    st.sidebar.header("Filter Spells")

    schools = sorted(df["school"].dropna().unique())
    levels = sorted(df["level"].dropna().unique())

    selected_school = st.sidebar.selectbox("School of Magic", ["All"] + schools)
    selected_level = st.sidebar.selectbox("Spell Level", ["All"] + [str(l) for l in levels])

    search = st.text_input("Search by name or description:")

    # --- Filtering ---
    filtered_df = df.copy()

    # Filter by class, subclass, school, and level

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
