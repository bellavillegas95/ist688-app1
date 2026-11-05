import streamlit as st

# This file is the entry point. It defines the app's pages
# and runs whichever one is picked in the sidebar.

tip_page = st.Page("tip_calculator.py", title="Tip Calculator")
lab1_page = st.Page("document_qa.py", title="Lab 1: Document Q&A")
# default=True makes Lab 2 the page that opens first
lab2_page = st.Page("Lab2.py", title="Lab 2: PDF Summarizer", default=True)

page = st.navigation([lab2_page, lab1_page, tip_page])
page.run()
