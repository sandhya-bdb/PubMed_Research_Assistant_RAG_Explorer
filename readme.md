# PubMed-RAG-Explorer,a Reserach Assistant - Streamlit Web App 🧬

A **Retrieval-Augmented Generation (RAG)** system wrapped in a user-friendly Streamlit web interface, enabling users to:

- Search scientific literature on National Center for Biotechnology Information (PubMed) by keyword  
- Ingest selected article abstracts and metadata into a persistent vector store (ChromaDB) using SentenceTransformers for embeddings  
- Ask natural-language questions and obtain context-informed answers using the Groq LLaMA-3 model  
- Inspect retrieved documents and generated answers side-by-side in the app

---

## 🚀 Project Overview

With this app you can:
1. Enter a search term (e.g., *“gene therapy cancer”*) in the sidebar  
2. Click **Search & Ingest** to fetch PMIDs, retrieve article metadata and abstracts, embed and store the documents  
3. In the main screen, type a question about the ingested dataset  
4. The system will retrieve the most relevant documents from the vector store, then pass them + your question to LLaMA-3 via Groq to generate a concise answer with PMIDs cited  
5. View the selected documents (title, partial abstract) and the generated answer in the UI  

---

## 🧰 Tech Stack

| Component             | Technology Used                                              |
|------------------------|-------------------------------------------------------------|
| Front-end / UI         | Streamlit                                                  |
| Embeddings             | SentenceTransformers (model: `all-MiniLM-L6-v2`)           |
| Vector Database        | ChromaDB (persistent client)                                |
| Language Model         | Groq LLaMA-3 (via Groq API)                                 |
| Document Retrieval API | PubMed (via NCBI E-utilities)                               |
| Configuration & Secrets| `.env`, `config.py`, environment variables                  |

---
## 🗂 Project Structure

pubmed_rag_app/
├── app.py # Main Streamlit application (UI)
├── pubmed.py # Module: search & fetch PubMed PMIDs/metadata
├── vector_store.py # Module: embed documents, ingest into ChromaDB, query
├── summarizer.py # Module: build prompt & call Groq LLaMA-3 for answer
├── config.py # Config file: paths, model names, environment variable reading
├── requirements.txt # Python dependencies
├── .gitignore # Files/folders to ignore from version control
└── README.md # This documentation

---

## 🧭 Getting Started

### 1. Clone the repository  
```bash
git clone https://github.com/<your-username>/pubmed_rag_app.git
cd pubmed_rag_app
2. Set up your virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # On Mac/Linux  
# or  
venv\Scripts\activate           # On Windows
3. Install dependencies
pip install -r requirements.txt
4. Add your API key
Create a file named .env in the project root (it’s listed in .gitignore) and add:
GROQ_API_KEY=your_real_groq_api_key
In config.py, ensure you load environment variables using dotenv (or os.environ).
Example:
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
5. Run the Streamlit app
streamlit run app.py
Open the URL shown in the terminal (usually http://localhost:8501) in your browser.
 
🧩 Usage Guide
A. Search & Ingest Documents
•	Use the sidebar to input your search term and set maximum number of results (default: 50)
•	Click Search & Ingest
•	The app will fetch PMIDs, retrieve article titles/abstracts, embed them and store them in ChromaDB
•	A success notification will confirm ingestion
B. Ask a Question
•	In the main panel, type your question (e.g., “What are recent advances in CAR-T therapy for leukaemia?”)
•	Click Submit Query
•	The app will retrieve relevant documents and display them
•	Then it will use LLaMA-3 (Groq) to generate an answer, which will be shown below
•	Documents are listed with their PMIDs, titles and abstract snippets for transparency
 
📌 Configuration Options
•	Embedding model: Configured in config.py under EMBEDDING_MODEL_NAME (default: all-MiniLM-L6-v2)
•	Vector store path: Default directory PERSIST_DIR = "chroma_db"
•	Groq model: Defined in config.py as GROQ_MODEL = "llama3-70b-8192" (or whichever variant you have access to)
•	Top-k results: TOP_K_RESULTS (default: 5) controls how many documents to retrieve for each query
 
🛡 Security & Secrets
•	Never commit your API keys (e.g., GROQ_API_KEY) or secret credentials in source files
•	Use .env or environment variables to store secrets locally
•	Ensure config.py only reads environment variables (does not hard-code keys)
•	Add .env, config.py (if containing secrets) and other sensitive files to .gitignore
•	If you ever accidentally commit a key, revoke/rotate it immediately
 
🤝 Contributing
Contributions are welcome!
•	Fork the repository and create a new branch (git checkout -b feature-xyz)
•	Adhere to PEP8 / consistent formatting
•	Add tests or validation if applicable
•	Submit a pull request with a clear description of changes
📅 Future Roadmap
•	✅ Core functionality: search, ingest, query, answer
•	🔧 Add metadata filters (e.g., publication year, journal, authors)
•	🌐 Deploy the app publicly (e.g., Streamlit Cloud, Heroku)
•	🧠 Add session history (past questions/answers) and export of answer + citations
•	📊 Add analytics or topic clustering of retrieved articles
