import streamlit as st
from database import execute_sql_query
from llm_sql_generator import get_sql_query_from_nl
from graph_generator import generate_graph_if_needed, generate_pie_chart
import os

st.set_page_config(layout="wide")
st.title("Text-to-SQL App with Graph Support")

user_query = st.text_input("Ask your question (e.g., 'Show me total sales by artist')")

if st.button("Run"):
    if user_query:
        with st.spinner("Generating SQL..."):
            sql_query = get_sql_query_from_nl(user_query)
        st.code(sql_query, language="sql")

        results, columns = execute_sql_query(sql_query)
        if results is not None and not results.empty:
            col1, col2 = st.columns([2, 2])
            with col1:
                st.subheader("Query Results")
                st.dataframe(results, use_container_width=True)

            chart_data = generate_graph_if_needed(user_query, results, columns)
            if chart_data:
                chart_type, x_vals, y_vals = chart_data
                with col2:
                    st.subheader("Graph")
                    if chart_type == "bar":
                        st.bar_chart({"x": x_vals, "y": y_vals})
                    elif chart_type == "line":
                        st.line_chart({"x": x_vals, "y": y_vals})
                    elif chart_type == "pie":
                        st.plotly_chart(generate_pie_chart(x_vals, y_vals))
        else:
            st.error(f"No results or error: {columns}")
