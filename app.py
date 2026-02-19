import os
import streamlit as st
import requests
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

# Page Config
st.set_page_config(page_title="University FAQ Chatbot 🎓")
st.markdown(
    "<h1 style='text-align:center;'>🏫 University AI Assistant</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center; font-size:16px; color:#dddddd;'>Ask anything about admissions, courses, fees, hostel & campus life</p>",
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.header("🎯 What You Can Ask")
    st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Admission Process")
    st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Courses")
    st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Hostel & Facilities")
    st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Fees & Scholarships")
    st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;• Exams & Academic Policies")
    st.write("")
    st.write("Available 24/7 for quick student support.")

# Load Environment Variables
load_dotenv()
SCALEDOWN_API_KEY = os.getenv("SCALEDOWN_API_KEY")
# Load FAISS
@st.cache_resource
def load_vectorstore():
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2"
    )
    db = FAISS.load_local(
        "faiss_db",
        embedding,
        allow_dangerous_deserialization=True
    )
    return db
db = load_vectorstore()
# Load Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)
# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
# User Input
query = st.chat_input("💬Ask a question about university...")
if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)
    docs = db.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])
    # Compress using ScaleDown
    headers = {
        "x-api-key": SCALEDOWN_API_KEY,
        "Content-Type": "application/json"
    }
    compressed_response = requests.post(
        "https://api.scaledown.xyz/compress/raw/",
        headers=headers,
        json={
            "context": context,
            "prompt": query,
            "model": "llama-3.1-8b-instant",
            "scaledown": {"rate": "auto"}
        }
    )
    if compressed_response.status_code == 200:
        compressed_context = compressed_response.json().get(
            "compressed_prompt", context
        )
    else:
        compressed_context = context

    # Final Prompt
    final_prompt = f"""
Answer the student's question based ONLY on the context below.

Context:
{compressed_context}

Question: {query}
"""

    # LLM Response
    response = llm.invoke(final_prompt)
    bot_reply = response.content

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )
