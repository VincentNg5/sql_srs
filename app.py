import streamlit as st
import pandas as pd
import duckdb
import io

st.title("SQL spaced repetition")

with st.sidebar:
    option = st.selectbox(
        "What would you like to review ?",
        ["Joins", "Group By", "Window functions"],
        index=None,
    )

csv = """
beverage,price
orange juice,2.5
Expresso,2
Tea,3
"""

beverages = pd.read_csv(io.StringIO(csv))

csv2 = """
food_item,food_price
cookie juice,2.5
chocolatine,2
muffin,3
"""

food_items = pd.read_csv(io.StringIO(csv2))

answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution = duckdb.query(answer).df()

sql_query = st.text_area("SQL", "SELECT * FROM beverages")
if sql_query:
    result = duckdb.query(sql_query).df()
    st.dataframe(result)

    if len(result.columns) != len(solution.columns):
        st.write("Some columns are missing")

    try:
        result = result[solution.columns]
        st.dataframe(result.compare(solution))
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_difference = len(result) - len(solution)
    if n_lines_difference != 0:
        st.write(f"Number of lines is different by {n_lines_difference}")


tables, solutions = st.tabs(["Tables", "Solutions"])
with tables:
    st.write("Beverages")
    st.dataframe(beverages)
    st.write("Food items")
    st.dataframe(food_items)
    st.write("Expected:")
    st.dataframe(solution)

with solutions:
    st.write(answer)
