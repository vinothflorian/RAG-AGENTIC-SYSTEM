import os
import json
from mysql import connector
import pandas as pd
from datetime import datetime
import calendar

connection = connector.connect(
    host="localhost",
    user="root",
    password="1234",
    connection_timeout= 30)
cursor = connection.cursor()
# Create a database if it doesn't exist
cr = "create database if not exists federal_register"
cursor.execute(cr)
cursor.execute("use federal_register")

QR = """CREATE TABLE IF NOT EXISTS federal_documents (
    document_number VARCHAR(50) PRIMARY KEY,
    title TEXT,
    publication_date DATE,
    document_type VARCHAR(255),
    html_url TEXT,
    abstract TEXT,
    search TEXT,
    month TEXT,
    year INT
)"""
cursor.execute(QR)

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = data.get("results", [])
    processed = []

    for doc in documents:
         pub_date = doc.get("publication_date", "")
         month_name = None
         year = None
         if pub_date:
            try:
                month_num = int(pub_date.split("-")[1])
                month_name = calendar.month_name[month_num]
                year = int(pub_date.split("-")[0])
            except Exception:
                month_name = None
                year = None

         processed.append({
            "document_number": doc.get("document_number"),
            "title": doc.get("title"),
            "publication_date": doc.get("publication_date"),
            "document_type": doc.get("document_type"),
            "html_url": doc.get("html_url"),
            "abstract": doc.get("abstract"),
            "search": " ".join([
    str(doc.get("document_number", "") or ""),
    str(doc.get("title", "") or ""),
    str(doc.get("publication_date", "") or ""),
    str(doc.get("document_type", "") or ""),
    str(doc.get("html_url", "") or ""),
    str(doc.get("abstract", "") or ""),
    str(month_name or ""),
    str(year or "")
    ]),
    "month": month_name,
    "year": year
        })

    return processed

def save_to_database(data):
    insert_query = """
    INSERT IGNORE INTO federal_documents (document_number, title, publication_date, document_type, html_url, abstract, search, month, year)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        title = VALUES(title),
        publication_date = VALUES(publication_date),
        document_type = VALUES(document_type),
        html_url = VALUES(html_url)
    """
    for record in data:
        cursor.execute(insert_query, (
            record["document_number"],
            record["title"],
            record["publication_date"],
            record["document_type"],
            record["html_url"],
            record["abstract"],
            record["search"],
            record["month"],
            record["year"]
        ))
    connection.commit()



for filename in os.listdir(r"D:\PYTHON\RAG Agentic System\agent\JSON_FILE"):
   data = process_file(os.path.join(r"D:\PYTHON\RAG Agentic System\agent\JSON_FILE", filename))
   save_to_database(data)
   print(f"Processed and saved data from {filename}")
   


