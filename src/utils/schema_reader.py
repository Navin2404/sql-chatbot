# src/utils/schema_reader.py
# Idhu function database structure (schema) padikkum
# LLM ku database structure theriyanum, athukku idhu use aagum
#
# Example: LLM ku "employees table-la enna columns irukku"
# nu therinjaal dhan correct SQL generate pannum

import sqlite3

DB_PATH = "data/company.db"


def get_database_schema() -> str:
    """
    # Database-la irukura ella tables and columns details eduthu
    # text format-la return pannum
    #
    # Idhu LLM ku prompt-la kudukurom - "database structure idhu"
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Database-la irukura ella table names eduku
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    schema_text = "DATABASE SCHEMA:\n\n"

    # Ovvoru table ku columns details eduku
    for table in tables:
        table_name = table[0]

        # SQLite system table-ah skip pannu (idhu user data illa)
        if table_name == "sqlite_sequence":
            continue

        schema_text += f"Table: {table_name}\n"

        # PRAGMA command - table structure details kudukum
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        for col in columns:
            # col format: (cid, name, type, notnull, default, pk)
            col_name = col[1]
            col_type = col[2]
            is_primary = "PRIMARY KEY" if col[5] else ""
            schema_text += f"  - {col_name} ({col_type}) {is_primary}\n"

        schema_text += "\n"

    conn.close()
    return schema_text


def get_sample_data(table_name: str, limit: int = 2) -> str:
    """
    # Ovvoru table-layum konjam sample rows eduthu kaattum
    # LLM ku data eppadi irukku-nu oru idea kidaikum
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
    rows = cursor.fetchall()

    # Column names eduku
    column_names = [description[0] for description in cursor.description]

    result = f"Sample data from {table_name}:\n"
    result += f"Columns: {column_names}\n"
    for row in rows:
        result += f"  {row}\n"

    conn.close()
    return result


if __name__ == "__main__":
    # Test panni paaru
    print(get_database_schema())
    print(get_sample_data("employees"))