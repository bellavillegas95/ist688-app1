import streamlit as st

# This file is the entry point. It defines the app's two pages
# and runs whichever one is picked in the sidebar.

tip_page = st.Page("tip_calculator.py", title="Tip Calculator")
qa_page = st.Page("document_qa.py", title="Document Q&A")

page = st.navigation([tip_page, qa_page])
page.run()
