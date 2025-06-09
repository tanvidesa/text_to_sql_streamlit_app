import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_sql_query_from_nl(nl_query: str) -> str:
    prompt = f"""You are an expert SQL developer. Convert this natural language question into an SQL query for a SQLite Chinook database:\n\n{nl_query}"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip("```sql").strip("```").strip()
