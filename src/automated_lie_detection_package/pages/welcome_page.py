import streamlit as st

#Page text
st.title("Welcome to the _'AUTOMATED LIE DETECTOR'_")
st.write("""
This interactive app lets you explore how an AI model, trained on autobiographical statements, classifies text as **truthful** or **deceptive**.

- 📝 **Single Statement:** Enter your own or someone else's autobiographical statement and receive an instant prediction with a confidence score.
- 🧠 **Explainability:** See which words influenced the model's decision for each statement.
- 📂 **Batch Mode:** Upload a CSV file of statements for group analysis, complete with downloadable results and visualizations.
- 📊 **Visual Insights:** View charts and statistics for your batch predictions.

**Disclaimer:**  
This tool is for educational and demonstration purposes only. The model is not perfect and should not be used for high-stakes or legal decisions.
""")

#Button
if st.button("Next"):
    st.switch_page("pages/lie_detection_page.py")