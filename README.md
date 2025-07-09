# FedRAG: Retrieval-Augmented Generation System for the U.S. Federal Register

**FedRAG** is an intelligent, agentic RAG (Retrieval-Augmented Generation) system that enables users to ask questions about U.S. Federal Register documents and receive concise, AI-generated answers based on official government content.

This system uses:
- ✅ **MySQL** as a source of truth
- ✅ **Ollama + Qwen2.5 LLM** for local inference
- ✅ **Keyword-based SQL retrieval**
- ✅ **Summarization using local LLM**
- ✅ **Streamlit** for a user-friendly frontend
- ✅ **Asynchronous Python pipeline**

---

## 🔧 Features

- 📥 **Automated Data Pipeline**  
  Fetches JSON documents from the Federal Register and inserts them into a MySQL database.

- 🧠 **Local LLM Agent (Ollama + Qwen)**  
  Extracts relevant keywords and generates concise answers using locally hosted LLMs.

- 🔍 **RAG System**  
  Retrieves top-matching rows using MySQL full-text search on extracted keywords.

- 📊 **Streamlit Interface**  
  A web-based UI where users can ask natural language questions.

- 🧵 **Context Formatting**  
  Combines multiple matching rows into a coherent document for the LLM to summarize.

---

## 📁 Project Structure

```
├── data_pipeline/
│   ├── downloader.py         # Downloads JSON data from official site
│   └── processor.py          # Inserts parsed data into MySQL
│
├── agent/
│   ├── KEY_QUERY.py          # Keyword extractor using Ollama
│   ├── SQL_FETCH.py          # SQL search logic using extracted keywords
│   └── LLM.py                # Main RAG logic (keyword → search → summarize)
│
├── streamlit_app.py          # Streamlit UI to interact with the system
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fedrag.git
cd fedrag
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up MySQL

Create a MySQL database named `federal_register` with a table:

```sql
CREATE TABLE federal_documents (
    document_number VARCHAR(255),
    title TEXT,
    publication_date DATE,
    html_url TEXT,
    abstract TEXT
);
```

Update your MySQL credentials in `processor.py` and `SQL_FETCH.py`.

### 4. Run Data Pipeline

```bash
python data_pipeline/downloader.py
python data_pipeline/processor.py
```

### 5. Start the Agent

```bash
python agent/LLM.py
```

Or run the UI:

```bash
streamlit run streamlit_app.py
```

---

## 📦 Requirements

- Python 3.10+
- MySQL Server
- [Ollama](https://ollama.com) installed locally
- LLM model like `qwen:0.5b` pulled into Ollama

```bash
ollama pull qwen:0.5b
```

---

## 🧠 Sample Query

> **User:** "Show me proposals on illegal discrimination"  
> **System:** Extracts keywords → retrieves matching documents → summarizes them using the LLM → displays the final answer

---

## ✨ Future Enhancements

- Add agent memory and history tracking
- Semantic search using vector embeddings
- Schedule automatic updates of database
- Enable document upload for private RAG

---

## 🛡 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Vinoth Zavier**  
For support or collaboration, feel free to connect.