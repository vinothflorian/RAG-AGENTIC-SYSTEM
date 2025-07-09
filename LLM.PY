
import ollama
import datetime
import asyncio
from KEY_QUERY import fetch_keywords
from SQL_FETCH import fetch_sqlrows
from downloader import fetch_last_7_days
import processor
import os
import streamlit as st

st.set_page_config(page_title="Federal RAG System", layout="wide")
st.title("Retrieval-Augmented Generation System for Federal Register Using Local LLM")

if st.button("Fetch and Process Last 7 Days Data"):
    with st.spinner("Fetching data for the last 7 days"):
        data_json = asyncio.run(fetch_last_7_days())
        st.success("Data fetched successfully!")
        for filename in os.listdir(r"D:\PYTHON\RAG Agentic System\agent\JSON_FILE"):
            data = processor.process_file(os.path.join(r"D:\PYTHON\RAG Agentic System\agent\JSON_FILE", filename))
            processor.save_to_database(data)


st.subheader("Ask a Question About the Federal Register")        
query = st.text_input("Enter your question", "")

key_word = []
sql_rows = []

if st.button("Fetch Keywords"):
    if not query.strip():
        st.error("Please enter a valid question.")
    else:
        with st.spinner("Fetching keywords..."):
            key_word = asyncio.run(fetch_keywords(query))
            if key_word:
                st.success(f"Keywords fetched: {key_word}")
                sql_rows = fetch_sqlrows(key_word)
            else:
                st.error("No keywords found for the given query.")


def format_row(row):
    doc_num, title, pub_date, url, content = row
    return f"""Document Number: {doc_num}
    Title: {title}
    Date: {pub_date}
    URL: {url}
    Content: {content or "No abstract available."}
    """


def create_context_from_rows(rows):
    return "\n\n---\n\n".join([format_row(row) for row in rows])

if sql_rows:
    st.markdown("### SQL Results:")
    st.markdown(create_context_from_rows(sql_rows))

def summarize_rows_llm(context, user_question, model="qwen:0.5b"):
    prompt = f"""
           You are an AI assistant tasked with answering user question based on the context.
           Only use the given context to answer the user query or summarise the context — do not make up content.
            Context:
            {context}

            Question: {user_question}
            Answer:
            """

    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])

    return response['message']['content']


if st.button("LLM Summary"):
        st.subheader("LLM Summary:")
        st.markdown(summarize_rows_llm(sql_rows, query, model="qwen:0.5b"))
    
