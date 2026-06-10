from groq import Groq
import os
from dotenv import load_dotenv
from src.database import get_schema, run_query

load_dotenv()

try:
    import streamlit as st
    api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

def generate_sql(user_question):
    schema = get_schema()
    prompt = f"""You are an expert SQL analyst. Given a database schema and a business question,
write a single valid SQLite SQL query that answers the question.

Rules:
- Return ONLY the SQL query, nothing else
- No explanations, no markdown, no backticks
- Use only columns that exist in the schema
- Always use aggregations (SUM, COUNT, AVG) for numeric questions
- Always add ORDER BY and LIMIT where appropriate

Database schema:
{schema}

Business question: {user_question}

SQL query:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    sql = response.choices[0].message.content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql

def ask(user_question):
    try:
        sql = generate_sql(user_question)
        result = run_query(sql)
        return {
            "question": user_question,
            "sql": sql,
            "result": result,
            "error": None
        }
    except Exception as e:
        return {
            "question": user_question,
            "sql": None,
            "result": None,
            "error": str(e)
        }

if __name__ == "__main__":
    questions = [
        "Which region had the highest total revenue?",
        "Who are the top 3 sales reps by revenue?",
        "What is the best selling product category?",
        "How many orders were placed each month?",
        "What is the average order value by region?"
    ]
    for q in questions:
        print(f"\nQuestion: {q}")
        response = ask(q)
        if response["error"]:
            print(f"Error: {response['error']}")
        else:
            print(f"SQL: {response['sql']}")
            print(f"Result:\n{response['result']}")
            print("-" * 50)