import streamlit as st

# --------------------------------------------------
# Streamlit config (MUST be first Streamlit command)
# --------------------------------------------------
st.set_page_config(page_title="Fact Checker", layout="wide")

from pypdf import PdfReader
from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv
import os
import json
import re

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
load_dotenv()

# --------------------------------------------------
# Clients (env-based auth ONLY)
# --------------------------------------------------
llm = Groq()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# --------------------------------------------------
# UI Header
# --------------------------------------------------
st.title("📄 Fact-Checking Web App")
st.write("Upload a PDF to extract and verify factual claims using live web data.")

# --------------------------------------------------
# PDF Extraction
# --------------------------------------------------
def extract_text(pdf):
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text[:12000]

# --------------------------------------------------
# Claim Extraction (STRICT)
# --------------------------------------------------
def extract_claims(text):
    prompt = f"""
You are a professional fact-checker.

Extract ONLY complete, self-contained factual claims from the text.

STRICT RULES:
- Each claim MUST be a full sentence.
- Each claim MUST contain subject + fact + context.
- DO NOT return years, numbers, entities, or technologies alone.
- DO NOT return fragments or partial phrases.
- Skip vague or unverifiable statements.

GOOD:
- "The iPhone 15 was launched in 2019 with a USB-C charging port."

BAD (DO NOT RETURN):
- "2019"
- "USB-C"
- "Apple"
- "1.4 billion"

Return ONLY a JSON array of strings. No explanation.

TEXT:
{text}
"""

    response = llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=900,
    )

    raw = response.choices[0].message.content.strip()

    try:
        claims = json.loads(raw)
    except:
        return []

    # Final safety filter
    clean_claims = []
    for c in claims:
        if isinstance(c, str) and len(c.split()) >= 6:
            clean_claims.append(c.strip())

    return clean_claims

# --------------------------------------------------
# Claim Verification
# --------------------------------------------------
def verify_claim(claim):
    search_results = tavily.search(query=claim, max_results=3)

    prompt = f"""
Claim:
{claim}

Evidence from web search:
{search_results}

Classify the claim STRICTLY as JSON:

{{
  "status": "Verified | Inaccurate | False",
  "explanation": "brief explanation with corrected info if needed"
}}

Rules:
- If evidence contradicts the claim → False
- If claim is outdated → Inaccurate
- If evidence clearly supports → Verified
"""

    response = llm.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=500,
    )

    raw = response.choices[0].message.content.strip()

    try:
        result = json.loads(raw)
    except:
        return {"status": "Unknown", "explanation": raw}

    status = result.get("status", "Unknown").strip().capitalize()
    explanation = result.get("explanation", "").strip()

    if status not in ["Verified", "Inaccurate", "False"]:
        status = "Unknown"

    return {"status": status, "explanation": explanation}

# --------------------------------------------------
# UI Logic
# --------------------------------------------------
uploaded = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded:
    with st.spinner("Reading document..."):
        text = extract_text(uploaded)

    with st.spinner("Extracting claims..."):
        claims = extract_claims(text)

    st.subheader(f"🔍 Found {len(claims)} claims")

    for claim in claims:
        with st.spinner("Verifying claim..."):
            result = verify_claim(claim)

        status = result["status"]
        explanation = result["explanation"]

        color = {
            "Verified": "green",
            "Inaccurate": "orange",
            "False": "red",
            "Unknown": "gray"
        }[status]

        st.markdown(
            f"""
### **{claim}**
**Status:** :{color}[{status}]

{explanation}
"""
        )
