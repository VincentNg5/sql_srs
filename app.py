import streamlit as st
import pandas as pd
import duckdb

st.title("SQL spaced repetition")

option = st.selectbox(
    "What would you like to review ?", 
    ["Group By", "Window functions"], 
    index=None
)

df = pd.DataFrame({
    'a': [1, 2, 3],
    'b': [4, 5, 6]}
)
sql_query = st.text_area("SQL", "SELECT * FROM df")
st.write("Your query:", sql_query)

result = duckdb.query(sql_query).df()
st.dataframe(result)

