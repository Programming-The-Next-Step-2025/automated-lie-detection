import streamlit as st

# Set page configuration for the Streamlit app including title and icon
st.set_page_config(page_title="LIE-DETECTOR", page_icon="random")

# Define pages
welcome_page = st.Page("pages/welcome_page.py")
lie_detection_page = st.Page("pages/lie_detection_page.py")
batch_lie_detection_page = st.Page("pages/batch_lie_detection_page.py")

# Navigation
pg = st.navigation(
    [welcome_page, lie_detection_page, batch_lie_detection_page],
)
pg.run()