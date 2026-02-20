# 🎓 University FAQ Chatbot (RAG Based AI Assistant)

This project is a *Streamlit-based AI chatbot* designed to answer university-related questions such as admissions, courses, fees, hostel facilities, and academic policies.
It uses *Retrieval Augmented Generation (RAG)* to provide accurate responses based only on stored FAQ data instead of generating random AI answers.
The system combines *semantic search, context compression, and LLM response generation* to deliver fast and reliable information.

---

## 🚀 Features

* Answers student queries in real-time  
* Uses semantic search instead of keyword matching  
* Provides accurate responses from FAQ dataset  
* Context compression for faster LLM processing  
* Clean Streamlit chat interface  
* Supports 24/7 automated student support  

---

## 🧠 Technologies Used

- Python
- Streamlit (Frontend UI)
- LangChain (RAG Pipeline)
- FAISS (Vector Database)
- HuggingFace Sentence Transformers (Embeddings)
- Groq LLaMA-3.1 Model (LLM)
- ScaleDown API (Context Compression)
- Pandas (CSV Data Processing)

---

## 📂 Dataset

The chatbot uses a CSV dataset containing:

* 500 realistic university FAQs  
* Questions related to admissions, courses, fees, hostel, exams, and campus life  
* Pre-processed and converted into embeddings  

---

## ⚙️ How to Get Started

### 1️⃣ Clone the Repository

```
git clone https://github.com/yourusername/university-faq-chatbot.git
cd university-faq-chatbot

```

###  2️⃣ Install Dependencies

```
pip install -r requirements.txt

```

3️⃣ Add API Keys

Create a .env file in the project folder and add:

```

GROQ_API_KEY=your_groq_api_key
SCALEDOWN_API_KEY=your_scaledown_api_key

```

4️⃣ Run the Streamlit App

```

streamlit run app.py

```

The chatbot will open in your browser.

