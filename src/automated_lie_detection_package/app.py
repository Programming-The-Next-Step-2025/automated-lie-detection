import streamlit as st

st.set_page_config(page_title="APA", page_icon="random")

# Load custom CSS
with open("./style/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Define pages
welcome_page = st.Page("pages/welcome_page.py")
lie_detection_page = st.Page("pages/lie_detection_page.py")

# Navigation
pg = st.navigation(
    [welcome_page, lie_detection_page]
)
pg.run()