# 🤖 Business Insights Chatbot

An AI-powered tool that lets business users ask questions in plain English
and get back SQL query results + charts — no SQL knowledge needed.

> **Status:** 🚧 Actively in development

---

## 💡 What it does
Type a question like *"Which region had the highest revenue?"*
and the app generates the SQL, runs it, and returns a chart automatically.

---

## 🔧 Tech Stack
`Python` `LangChain` `OpenAI API` `SQLite` `Streamlit` `Pandas` `Plotly`

---

## 📁 Project Structure
```
business-insights-chatbot/
├── data/            # Sales dataset (CSV)
├── src/
│   ├── database.py  # SQLite loader & query runner
│   ├── llm.py       # LLM integration
│   └── app.py       # Streamlit UI
└── requirements.txt

---

## 🌐 Live Demo
👉 [Try the app live](https://business-insights-chatbot-kajalsrivastava.streamlit.app)
