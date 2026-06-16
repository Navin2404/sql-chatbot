# src/llm/sql_generator.py
# Idhu thaan main part!
# User oda English question-ah SQL query-ah maathum

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

# System prompt - LLM ku strict instructions kudukurom
# Idhu romba important - LLM correct SQL mattum generate pannanum
SYSTEM_PROMPT = """You are an expert SQL query generator for SQLite database.

{schema}

STRICT RULES:
1. Generate ONLY a valid SQLite SQL query - nothing else
2. Do NOT include explanations, markdown formatting, or ```sql tags
3. Do NOT use any tables or columns that are not in the schema above
4. Use proper SQL syntax for SQLite
5. If the question cannot be answered using the schema, respond with: SELECT 'Cannot answer this question with available data' as message
6. Always end the query with a semicolon

Return ONLY the raw SQL query, nothing else.
"""


def generate_sql(question: str, schema: str) -> str:
    """
    # User question + database schema kudutha
    # LLM SQL query generate pannum
    #
    # Example:
    # question = "Show me employees in Engineering department"
    # output = "SELECT * FROM employees WHERE dept_id =
    #            (SELECT dept_id FROM departments WHERE dept_name='Engineering');"
    """

    # LLM initialize pannurom - Groq use pannurom (free!)
    llm = ChatGroq(
        model="llama-3.1-8b-instant",  # Fast and free model
        temperature=0,  # 0 = consistent, predictable output
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    # Prompt template create pannu
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "Question: {question}\n\nSQL Query:")
    ])

    # Chain create pannu - prompt + llm sera connect aagum
    chain = prompt | llm

    # LLM call pannu
    response = chain.invoke({
        "schema": schema,
        "question": question
    })

    sql_query = response.content.strip()

    # LLM sometimes ```sql tags add pannum - athai clean pannu
    sql_query = clean_sql_query(sql_query)

    return sql_query


def clean_sql_query(sql: str) -> str:
    """
    # LLM output-la extra characters irundha clean pannurom
    # Example: ```sql SELECT * FROM employees; ```
    #          -> SELECT * FROM employees;
    """

    # Markdown code block tags remove pannu
    sql = sql.replace("```sql", "").replace("```", "")

    # Extra spaces remove pannu
    sql = sql.strip()

    return sql


if __name__ == "__main__":
    # Test pannalam
    from src.utils.schema_reader import get_database_schema

    schema = get_database_schema()

    test_question = "Show me top 5 employees by salary"
    sql = generate_sql(test_question, schema)

    print(f"Question: {test_question}")
    print(f"Generated SQL: {sql}")