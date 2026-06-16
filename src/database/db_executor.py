# src/database/db_executor.py
# Idhu generate aana SQL query-ah database-la run pannum
# Result-ah pandas DataFrame format-la return pannum (table maathiri)

import sqlite3
import pandas as pd

DB_PATH = "data/company.db"


def execute_sql(sql_query: str) -> dict:
    """
    # SQL query run panni result return pannurom
    #
    # Return format:
    # {
    #   "success": True/False,
    #   "data": DataFrame (success aana),
    #   "error": error message (fail aana)
    # }
    """

    try:
        # Database connection create pannu
        conn = sqlite3.connect(DB_PATH)

        # pandas use panni query run pannurom
        # Idhu automatically table format result kudukum
        df = pd.read_sql_query(sql_query, conn)

        conn.close()

        return {
            "success": True,
            "data": df,
            "error": None,
            "row_count": len(df)
        }

    except Exception as e:
        # Query wrong-ah irundha, error catch pannurom
        # App crash aagama, error message kaattum
        return {
            "success": False,
            "data": None,
            "error": str(e),
            "row_count": 0
        }


def is_safe_query(sql_query: str) -> bool:
    """
    # IMPORTANT SAFETY CHECK!
    # User database-ah delete/modify panna koodathu
    # Andha maathiri queries-ah block pannurom
    #
    # Idhu mattum dhan SELECT queries allow pannum
    """

    # Dangerous keywords list
    dangerous_keywords = [
        "DROP", "DELETE", "UPDATE", "INSERT",
        "ALTER", "CREATE", "TRUNCATE", "REPLACE"
    ]

    sql_upper = sql_query.upper()

    # Ethavadhu dangerous keyword irukka check pannu
    for keyword in dangerous_keywords:
        if keyword in sql_upper:
            return False

    return True


if __name__ == "__main__":
    # Test pannalam
    test_sql = "SELECT * FROM employees LIMIT 5;"
    result = execute_sql(test_sql)

    if result["success"]:
        print(result["data"])
    else:
        print(f"Error: {result['error']}")