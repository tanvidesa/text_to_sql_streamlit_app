import streamlit as st
import os

import plotly.express as px
import sqlite3
import pandas as pd
openai.api_key = os.getenv("OPENAI_API_KEY")
st.title("🧠 Text-to-SQL Query App")
#  User Input
user_question = st.text_input("Ask a question in English:")
def ask_llm(question):
    prompt = f"""
    Convert this English question into an SQL query using SQLite format (Chinook DB):
    Question: {question}
    SQL:"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    sql = response['choices'][0]['message']['content']
    return sql.strip().strip("```sql").strip("```")
def run_sql(sql):
    conn = sqlite3.connect("chinook.db")
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df
def detect_graph_need(question):
    keywords = ["trend", "over time", "compare", "distribution", "chart", "graph", "visualize", "plot"]
    return any(kw in question.lower() for kw in keywords)
def plot_graph(df):
    if df.shape[1] < 2:
        return None
    col1, col2 = df.columns[:2]
    fig = px.bar(df, x=col1, y=col2, title="Bar Chart")
    st.plotly_chart(fig)
if st.button("Generate"):
    if user_question:
        with st.spinner("Thinking..."):
            sql_query = ask_llm(user_question)
            st.code(sql_query, language='sql')
            try:
                data = run_sql(sql_query)
                st.dataframe(data)

                if detect_graph_need(user_question):
                    plot_graph(data)
            except Exception as e:
                st.error(f"Error running query: {e}")

