import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import requests
from modules.rag import generate_answer

st.title("Football Knowledge Assistant")
st.write("Ask me anything about football! 🚀")

query = st.text_input("Your question:")
if query:
    with st.spinner("Scraping latest headlines..."):
        # Call FastAPI endpoint to scrape headlines
        response = requests.get("http://localhost:8000/scrape-headlines")
        if response.ok and response.json().get("success"):
            st.success("Headlines updated!")
        else:
            st.warning("Could not update headlines. Using previous data.")
    with st.spinner("Thinking..."):
        answer = generate_answer(query)
        st.write("**Answer:**")
        st.write(answer)