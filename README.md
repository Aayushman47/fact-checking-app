# 📄 Fact-Checking Web App

A deployed web application that automatically extracts factual claims from PDFs, verifies them against live web data, and flags each claim as **Verified**, **Inaccurate**, or **False**.

---

## 🚀 Live Demo

- **App URL:** (https://fact-checking-app-a.streamlit.app/)
- **Demo Video:** https://drive.google.com/file/d/1nKCb8HLkIZEm_4_5im4f_kbUu6AKJ87j/view?usp=sharing

---

## 🎯 Objective

This tool acts as a fact-checking layer between document drafts and publication. It is designed to detect incorrect, outdated, or false claims instead of approving content blindly.

The system:
1. Extracts verifiable factual claims from a PDF  
2. Cross-references each claim using live web search  
3. Classifies each claim as Verified, Inaccurate, or False  

---

## 🧠 How It Works

PDF Upload
↓
Text Extraction
↓
Claim Extraction (LLM)
↓
Live Web Search
↓
Claim Verification (LLM Reasoning)
↓
Verdict + Explanation


---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend / Intelligence
- Groq API (LLM inference)
- LLaMA-3 family models
- Tavily Search API

### Utilities
- PyPDF
- python-dotenv

---

## 🔍 Key Design Choices

- Only complete, self-contained factual claims are extracted  
- Numbers, years, entities, and fragments are explicitly rejected  
- Each claim is verified independently using live web data  
- The system prefers flagging uncertainty over hallucinating correctness  

---

## 📂 Project Structure
.
├── app.py
├── requirements.txt
├── README.md
└── .gitignore


---

## 🔐 Environment Variables

The following environment variables are required:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key

pip install -r requirements.txt
python -m streamlit run app.py

Open in browser:

http://localhost:8501

🧪 Testing

The application is tested using documents that contain:

False claims

Widely circulated myths

Outdated statistics

Correct factual information

The expected behavior is to flag incorrect claims rather than approving them.

🚧 Limitations & Future Improvements

Add explicit source citations per claim

Support additional document formats (DOCX, HTML)

Add confidence scores per verdict

Improve batching for large PDFs

👤 Author

Aayushman Saini
GitHub: https://github.com/Aayushman47


