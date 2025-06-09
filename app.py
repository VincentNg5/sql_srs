import os
import logging
import streamlit as st
import pandas as pd
import duckdb
from datetime import date

if "data" not in os.listdir():
    print("Creating folder data...")
    logging.error(os.listdir())
    logging.error("Creating folder data...")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

st.title("SQL spaced repetition")

with st.sidebar:
    available_themes_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    available_themes = available_themes_df["theme"].unique()

    theme = st.selectbox(
        "What would you like to review ?",
        options=available_themes,
        index=None,
    )
    st.write("You selected:", theme)

if theme:
    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'")
else:
    exercise = con.execute("SELECT * FROM memory_state")
exercise_df = exercise.df().sort_values("last_reviewed").reset_index(drop=True)
st.write(exercise_df)

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""


# solution = duckdb.query(answer).df()

sql_query = st.text_area("SQL", "SELECT * FROM beverages")
if sql_query:
    result_df = con.execute(sql_query).df()
    st.dataframe(result_df)

    exercise_name = exercise_df.loc[0, "exercise_name"]
    solution_fname = f"answers/{exercise_name}.sql"
    with open(solution_fname, "r") as f:
        solution = f.read()

    solution_df = con.execute(solution).df()

    if len(result_df.columns) != len(solution_df.columns):
        st.write("Some columns are missing")

    n_lines_difference = len(result_df) - len(solution_df)
    if n_lines_difference != 0:
        st.write(f"Number of lines is different by {n_lines_difference}")

for n_days in [2, 7, 30]:
    if st.button(f"Revoir dans {n_days} jours"):
        next_review = date.today() + pd.Timedelta(days=n_days)
        spaced_repetition_query = f"""
            UPDATE memory_state
            SET last_reviewed = '{next_review}'
            WHERE exercise_name = '{exercise_name}'
        """
        con.execute(spaced_repetition_query)
        st.rerun()

if st.button("Reset"):
    con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()

tab_tables, tab_solution = st.tabs(["Tables", "Solution"])
with tab_tables:
    exercice_tables = exercise_df.loc[0, "tables"]
    for table in exercice_tables:
        st.write(f"table: {table}")
        table_df = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(table_df)

with tab_solution:
    try:
        st.write(solution)
    except NameError:
        st.write("No solution available for this exercise.")