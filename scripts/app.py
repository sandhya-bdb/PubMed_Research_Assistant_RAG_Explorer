import streamlit as st
from pubmed import PubMedRetriever
from vector_store import VectorStore
from summarizer import LLMSummarizer
from config import PERSIST_DIR, EMBEDDING_MODEL_NAME, TOP_K_RESULTS

from config import GROQ_API_KEY

print(GROQ_API_KEY)
# use GROQ_API_KEY when calling the API


def sidebar_search_and_ingest(vector_store: VectorStore):
    st.sidebar.header("🔍 Search & Ingest PubMed Articles")
    search_term = st.sidebar.text_input("Enter search term:")
    max_results = st.sidebar.number_input("Max results to retrieve:", min_value=1, max_value=500, value=50, step=10)
    if st.sidebar.button("Search & Ingest"):
        with st.spinner("Retrieving PMIDs…"):
            pmids = PubMedRetriever.search_pubmed_articles(search_term, max_results=max_results)
        st.sidebar.write(f"Retrieved {len(pmids)} PMIDs")
        with st.spinner("Fetching article metadata/abstracts…"):
            articles = PubMedRetriever.fetch_pubmed_abstracts(pmids)
        st.sidebar.write(f"Fetched {len(articles)} articles")

        # Prepare ingestion
        docs = [
            f"{a['title']} - {' '.join(a['abstract'].values()) if isinstance(a['abstract'], dict) else a['abstract']}"
            for a in articles
        ]
        ids = [a['pmid'] for a in articles]
        metadatas = [
            {
                "pmid": a['pmid'],
                "journal": a['journal'],
                "publication_date": a['publication_date'],
                "authors": a['authors']
            }
            for a in articles
        ]

        with st.spinner("Ingesting into vector store…"):
            vector_store.ingest(docs=docs, metadatas=metadatas, ids=ids)
        st.sidebar.success(f"Ingested {len(docs)} documents into vector store.")

def main_interface(vector_store: VectorStore, summarizer: LLMSummarizer):
    st.title("PubMed-Powered RAG Explorer,a Research Assistant")
    st.write("Ask a question based on the ingested PubMed articles below.")

    query = st.text_input("Enter your question here:")
    if st.button("Submit Query"):
        if not query:
            st.warning("Please enter a question first.")
            return

        with st.spinner("Querying vector store…"):
            result = vector_store.query(query, k=TOP_K_RESULTS)

        # Build docs list for summarizer
        docs_for_summary = []
        for idx, doc_text in enumerate(result["documents"][0]):
            pmid = result["ids"][0][idx]
            title = result["metadatas"][0][idx].get("title", "")
            docs_for_summary.append({
                "pmid": pmid,
                "title": title,
                "abstract": doc_text
            })

        st.write("### Retrieved Documents")
        for d in docs_for_summary:
            st.write(f"**PMID:** {d['pmid']}  \n**Title:** {d['title']}  \n**Abstract fragment:** {d['abstract'][:300]}…")
            st.write("------")

        with st.spinner("Generating answer…"):
            answer = summarizer.generate_answer(query, docs_for_summary)

        st.write("### 🧠 Answer")
        st.write(answer)

def run_app():
    st.set_page_config(page_title="PubMed RAG App", layout="wide", initial_sidebar_state="expanded")

    # Initialize vector store & summarizer
    vs = VectorStore(persist_directory=PERSIST_DIR, model_name=EMBEDDING_MODEL_NAME)
    summarizer = LLMSummarizer()

    sidebar_search_and_ingest(vs)
    st.divider()
    main_interface(vs, summarizer)

if __name__ == "__main__":
    run_app()
