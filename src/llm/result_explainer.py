# src/llm/result_explainer.py
# SQL result-ah simple English-la explain pannum
# User ku just numbers kaatta mattum illa,
# "enna meaning" nu sollum

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

EXPLAIN_PROMPT = """You are a helpful data analyst assistant.

User asked: "{question}"

SQL Query used: {sql_query}

Result data:
{result_data}

Explain this result to the user in 1-2 simple sentences. 
Be conversational and friendly. Mention specific numbers/names from the data.
Do not mention SQL or technical terms - explain like talking to a non-technical person.
"""


def explain_result(question: str, sql_query: str, df: pd.DataFrame) -> str:
    """
    # SQL result-ah simple language-la explain pannum
    #
    # Example:
    # question = "Top 5 employees by salary"
    # result -> "Karan Malhotra is the highest paid employee
    #            with a salary of 95000, followed by Vikram Singh..."
    """

    # Result empty-ah irundha
    if df.empty:
        return "No results found for your question."

    # DataFrame-ah text format-ku convert pannu - LLM ku kudukka
    result_text = df.to_string(index=False)

    # Result romba periya irundha, mattum kaattu (token saving ku)
    if len(result_text) > 1000:
        result_text = result_text[:1000] + "... (more rows)"

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,  # Konjam creative-ah explain panna
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", EXPLAIN_PROMPT)
    ])

    chain = prompt | llm

    response = chain.invoke({
        "question": question,
        "sql_query": sql_query,
        "result_data": result_text
    })

    return response.content


if __name__ == "__main__":
    # Test pannalam
    sample_df = pd.DataFrame({
        "emp_name": ["Karan Malhotra", "Vikram Singh"],
        "salary": [95000, 85000]
    })

    explanation = explain_result(
        "Top 2 employees by salary",
        "SELECT emp_name, salary FROM employees ORDER BY salary DESC LIMIT 2",
        sample_df
    )

    print(explanation)

