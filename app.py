# app.py
# Main Streamlit application
# Ella components-um sera connect pannurom

import streamlit as st
import pandas as pd
from src.utils.schema_reader import get_database_schema
from src.llm.sql_generator import generate_sql
from src.database.db_executor import execute_sql, is_safe_query
from src.llm.result_explainer import explain_result
import os

# Page configuration
st.set_page_config(
    page_title="Text-to-SQL Chatbot",
    page_icon="🗄️",
    layout="wide"
)

st.title("🗄️ Text-to-SQL Chatbot")
st.caption("Ask questions about your database in plain English")

# Database illana, create pannu
if not os.path.exists("data/company.db"):
    st.warning("Database not found! Creating sample database...")
    from src.database.db_setup import create_database

    create_database()
    st.success("Database created!")


# Schema cache pannurom - ovvoru time padikkanam vendaam
@st.cache_data
def load_schema():
    """
    # Database schema oru time padichu cache pannurom
    # @st.cache_data - idhu function result-ah memory-la store pannum
    """
    return get_database_schema()


schema = load_schema()

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("📊 Database Schema")
    st.text(schema)

    st.divider()

    st.header("💡 Example Questions")
    example_questions = [
        "Show me top 5 employees by salary",
        "How many employees are in each department?",
        "List all projects that are in progress",
        "What is the average salary in Engineering department?",
        "Show me employees hired after 2022",
        "Which department has the highest budget?"
    ]

    for q in example_questions:
        # Button click pannina, question text box-la fill aagum
        if st.button(q, key=q):
            st.session_state.question = q

# ---------- MAIN AREA ----------

# session_state - page refresh aanaalum data lose aagama irukka
if "question" not in st.session_state:
    st.session_state.question = ""

if "history" not in st.session_state:
    st.session_state.history = []

# Input box
question = st.text_input(
    "Ask a question about the database:",
    value=st.session_state.question,
    placeholder="Example: Show me all employees in Sales department"
)

# Ask button
if st.button("🔍 Ask", type="primary") and question:

    with st.spinner("Generating SQL query..."):
        try:
            # ---------- STEP 1: SQL GENERATE PANNU ----------
            sql_query = generate_sql(question, schema)

            # ---------- STEP 2: SAFETY CHECK ----------
            if not is_safe_query(sql_query):
                st.error("This query is not allowed for safety reasons. Only SELECT queries are permitted.")
                st.stop()

            # ---------- STEP 3: SQL DISPLAY PANNU ----------
            st.markdown("### Generated SQL Query")
            st.code(sql_query, language="sql")

            # ---------- STEP 4: SQL EXECUTE PANNU ----------
            result = execute_sql(sql_query)

            if result["success"]:
                df = result["data"]

                # ---------- STEP 5: RESULT EXPLAIN PANNU ----------
                with st.spinner("Generating explanation..."):
                    explanation = explain_result(question, sql_query, df)

                # ---------- STEP 6: DISPLAY RESULT ----------
                st.markdown("### 💬 Answer")
                st.info(explanation)

                st.markdown("### 📋 Data Table")
                st.dataframe(df, use_container_width=True)

                st.caption(f"Found {result['row_count']} row(s)")

                # History-la save pannu
                st.session_state.history.append({
                    "question": question,
                    "sql": sql_query,
                    "rows": result['row_count']
                })

            else:
                # SQL error aana, error message kaattu
                st.error(f"Query execution failed: {result['error']}")
                st.info("Try rephrasing your question or check the example questions.")

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

# ---------- QUERY HISTORY ----------
if st.session_state.history:
    st.divider()
    st.markdown("### 📜 Query History")

    for i, item in enumerate(reversed(st.session_state.history[-5:])):
        with st.expander(f"Q: {item['question']}"):
            st.code(item['sql'], language="sql")
            st.caption(f"Returned {item['rows']} row(s)")