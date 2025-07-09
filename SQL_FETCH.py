from mysql import connector
from KEY_QUERY import fetch_keywords
import asyncio

def fetch_sqlrows(par: list):
    connection = connector.connect(
    host="localhost",
    user="root",
    password="1234",
    connection_timeout=30)
    cursor = connection.cursor()

    cursor.execute("use federal_register")



    whereclause = " OR ".join(["search LIKE %s" for p1 in par])
    sql = f"SELECT document_number, title, publication_date, html_url, abstract FROM federal_documents WHERE {whereclause} LIMIT 5"
    values = [f"%{kw}%" for kw in par]  

    cursor.execute(sql, values)
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return results
    

if __name__ == "__main__":
    user_query = "orders from the president about advisory orders"
    keywords = asyncio.run(fetch_keywords(user_query))
    print("Extracted keywords:", keywords)
    results = fetch_sqlrows(keywords)
    print("SQL Results:", results)


    
    
    