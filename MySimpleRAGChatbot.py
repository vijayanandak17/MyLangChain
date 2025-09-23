import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
#from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import tempfile
import os

# -------------------- 🔑 Set API Key Here --------------------
OPENAI_API_KEY = "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"  # <-- Replace with your key

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

st.title("📄🔎 RAG Chatbot with FAISS")
st.write("Upload a PDF, index it in FAISS, and ask questions!")

# -------------------- File Upload --------------------
uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

if uploaded_file:
    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    st.success("✅ PDF uploaded successfully!")

    # -------------------- Load & Split --------------------
    loader = PyPDFLoader(tmp_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # -------------------- Embeddings + FAISS --------------------
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = FAISS.from_documents(splits, embeddings)

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # -------------------- LLM --------------------
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.2, model="gpt-4o-mini")
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    # -------------------- Chat Interface --------------------
    st.subheader("💬 Ask your question")
    query = st.text_input("Enter your query:")

    if query:
        with st.spinner("Thinking... 🤔"):
            response = qa_chain.run(query)

        # -------------------- Display Answer --------------------
        st.markdown("### 📢 Answer")
        st.write(response)

        # Expandable section for sources
        with st.expander("🔍 Retrieved Chunks"):
            for doc in retriever.get_relevant_documents(query):
                st.markdown(f"- **Page {doc.metadata.get('page', 'N/A')}**: {doc.page_content[:300]}...")

    # Clean up temp file
    os.remove(tmp_path)

