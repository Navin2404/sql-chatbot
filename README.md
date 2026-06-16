# Text-to-SQL Chatbot

Ask questions about your database in plain English and get instant answers — no SQL knowledge required. The system converts natural language into SQL queries, executes them safely, and explains results in simple terms.

## Problem It Solves

Business teams often depend on data analysts just to answer simple questions like "how many employees joined this year" or "which department has the highest budget." This tool lets anyone query a database directly using plain English, removing that bottleneck.

## How It Works

1. User asks a question in plain English
2. The question and database schema are sent to an LLM (Groq - Llama 3)
3. LLM generates a SQL query based on the actual schema
4. A safety layer blocks any destructive queries (DELETE, DROP, UPDATE, etc.) — only SELECT is allowed
5. The query runs on the database and returns results
6. LLM explains the result back in plain English
7. Both the explanation and the raw data table are shown to the user

## Tech Stack

- **LLM** — Groq (Llama 3 8B) for SQL generation and result explanation
- **Database** — SQLite
- **Framework** — LangChain
- **UI** — Streamlit
- **Language** — Python 3.11

## Key Features

- Natural language to SQL conversion
- Query safety validation (read-only, prevents destructive operations)
- Plain English explanation of results, not just raw data
- Query history tracking within a session
- Example questions provided in the UI for quick testing
- Schema-aware generation — LLM only uses tables/columns that actually exist

## Project Structure

```
text-to-sql-chatbot/
├── data/
│   └── company.db              # SQLite database
├── src/
│   ├── database/
│   │   ├── db_setup.py         # Creates sample database and tables
│   │   └── db_executor.py      # Executes SQL safely
│   ├── llm/
│   │   ├── sql_generator.py    # Converts English to SQL
│   │   └── result_explainer.py # Explains SQL results in plain English
│   └── utils/
│       └── schema_reader.py    # Reads database schema for the LLM
├── app.py                      # Main Streamlit application
└── requirements.txt
```

## Getting Started

```bash
git clone https://github.com/yourusername/text-to-sql-chatbot.git
cd text-to-sql-chatbot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

Initialize the database and run:
```bash
python src/database/db_setup.py
streamlit run app.py
```

## Example Queries

- "Show me top 5 employees by salary"
- "How many employees are in each department?"
- "List all projects that are in progress"
- "What is the average salary in Engineering department?"
- "Which department has the highest budget?"

## Safety Design

A dedicated validation layer scans every generated query before execution and blocks any query containing DROP, DELETE, UPDATE, INSERT, ALTER, CREATE, TRUNCATE, or REPLACE. Only SELECT statements are permitted, ensuring the database can never be modified through the chat interface.

## Future Improvements

- Support for PostgreSQL/MySQL in addition to SQLite
- Multi-turn conversation context (follow-up questions)
- Query result caching for repeated questions
- Export results to CSV/Excel

## Author

**Your Name** — [GitHub](https://github.com/yourusername) | [LinkedIn](https://linkedin.com/in/yourprofile)
