import streamlit as st
import pandas as pd
import duckdb

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=True)

st.title("SQL spaced repetition")

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review ?",
        ["cross_joins", "Group By", "Window functions"],
        index=None,
    )
    st.write("You selected:", theme)

exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'")
exercise_df = exercise.df()
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

    try:
        result_df = result_df[solution_df.columns]
        df_comparison = result_df.compare(solution_df)
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_difference = len(result_df) - len(solution_df)
    if n_lines_difference != 0:
        st.write(f"Number of lines is different by {n_lines_difference}")
    

tab_tables, tab_solution = st.tabs(["Tables", "Solution"])
with tab_tables:
    exercice_tables = exercise_df.loc[0, "tables"]
    for table in exercice_tables:
        st.write(f"table: {table}")
        table_df = con.execute(f"SELECT * FROM {table}").df()
        st.dataframe(table_df)

with tab_solution:
    st.write(solution)
    