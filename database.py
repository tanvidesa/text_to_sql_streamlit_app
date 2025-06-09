import sqlite3
import pandas as pd

def execute_sql_query(query: str):
    try:
        conn = sqlite3.connect("chinook.db")
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(data, columns=cols)
        return df, cols
    except Exception as e:
        return None, str(e)
