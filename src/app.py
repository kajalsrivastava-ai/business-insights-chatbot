import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.llm import ask
from src.database import load_to_sqlite, create_sample_data

st.set_page_config(
    page_title="Business Insights Chatbot",
    page_icon="🤖",
    layout="wide"
)

if "history" not in st.session_state:
    st.session_state.history = []

if not os.path.exists("data/sales.db"):
    df = create_sample_data()
    load_to_sqlite(df)

def auto_chart(df):
    if df is None or df.empty or len(df.columns) < 2:
        return None
    cols = df.columns.tolist()
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()
    if len(num_cols) == 0:
        return None
    x = cat_cols[0] if cat_cols else cols[0]
    y = num_cols[0]
    if len(df) == 1:
        fig = px.bar(df, x=x, y=y, color_discrete_sequence=["#378ADD"])
    elif len(df) <= 8:
        fig = px.bar(df, x=x, y=y, color_discrete_sequence=["#378ADD"])
    else:
        fig = px.line(df, x=x, y=y, color_discrete_sequence=["#378ADD"])
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis_title=None,
        yaxis_title=None,
        font=dict(size=12)
    )
    return fig

with st.sidebar:
    st.markdown("## 🤖 Business Insights Chatbot")
    st.markdown("Ask any business question in plain English.")
    st.divider()
    if st.session_state.history:
        st.markdown("**Previous questions**")
        for i, item in enumerate(reversed(st.session_state.history[-10:])):
            st.markdown(f"- {item['question'][:50]}...")
    else:
        st.markdown("*No questions yet*")
    st.divider()
    st.markdown("**Sample questions to try:**")
    samples = [
        "Which region had the highest revenue?",
        "Top 3 products by sales?",
        "Revenue by category this year?",
        "Who are the top sales reps?",
        "Monthly order trends?"
    ]
    for s in samples:
        if st.button(s, use_container_width=True):
            st.session_state.current_question = s

st.title("Business Insights Chatbot")
st.markdown("Type a business question below and get instant SQL-powered answers with charts.")
st.divider()

default_q = st.session_state.get("current_question", "")
question = st.text_input(
    "Ask a business question",
    value=default_q,
    placeholder="e.g. Which region had the highest revenue last quarter?"
)

col1, col2 = st.columns([1, 5])
with col1:
    ask_btn = st.button("Ask", type="primary", use_container_width=True)
with col2:
    if st.button("Clear history", use_container_width=False):
        st.session_state.history = []
        st.rerun()

if ask_btn and question:
    with st.spinner("Thinking..."):
        response = ask(question)
    st.session_state.history.append(response)
    if "current_question" in st.session_state:
        del st.session_state.current_question

if st.session_state.history:
    latest = st.session_state.history[-1]
    if latest["error"]:
        st.error(f"Error: {latest['error']}")
    else:
        st.success(f"Question: {latest['question']}")
        col_table, col_chart = st.columns(2)
        with col_table:
            st.markdown("**Results**")
            st.dataframe(latest["result"], use_container_width=True)
        with col_chart:
            st.markdown("**Chart**")
            fig = auto_chart(latest["result"])
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No chart available for this result")
        with st.expander("Show SQL query"):
            st.code(latest["sql"], language="sql")
        if len(st.session_state.history) > 1:
            st.divider()
            st.markdown("**Previous results**")
            for item in reversed(st.session_state.history[:-1]):
                with st.expander(f"Q: {item['question']}"):
                    if item["error"]:
                        st.error(item["error"])
                    else:
                        st.dataframe(item["result"], use_container_width=True)
                        st.code(item["sql"], language="sql")