import streamlit as st

st.title("Welcome to the _'AUTOMATED LIE DETECTOR'_")
st.write("""In this application, you can interact with an AI model that has been trained to classify autobiographical statements as truthful or deceptive.  
             \nThis model can predict whether a statement is true or false with an accuracy of around 77%.
             \nOn the next pages you will be able to paste your own statements or something someone told you. 
             \nYou will receive a prediction of whether the statement is true or false along with the confidence the model has in its prediction.""")
st.write("""**Note**: This model is not perfect and should not be used as a definitive lie detector.""")

if st.button("Next"):
    st.switch_page("pages/lie_detection_page.py")