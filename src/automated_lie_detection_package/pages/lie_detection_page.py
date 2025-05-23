import streamlit as st
from utility import predictionloop

st.title("Automated Lie Detector")
st.write("Do you want to know if your autobiographical statement is truthful or deceptive?")
st.write("If you want to test another statement, simply delete your input and press submit again.")

# Containers for dynamic updates
input_container = st.empty()
submit_cont = st.empty()
feedback_container = st.empty()
progr_cont = st.empty()

# Input for the user to write their statement
user_input = input_container.text_area("**You can write or paste your autobiographical statement here**")

# Submit button to process the input
if submit_cont.button("Submit"):
    
    feedback_container.markdown(
        f"### Model Feedback\n"
        f"The model predicts that your statement is classified as **{'TRUTHFUL' if risposta == 0 else 'DECEPTIVE'}**.\n"
        f"**Confidence Score:** {prob:.2f}%"
        )
    progr_cont.progress(int(prob))  # Display progress bar for confidence score

            
