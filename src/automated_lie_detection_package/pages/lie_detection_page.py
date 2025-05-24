import streamlit as st
from automated_lie_detection_package.utility import load_local_model, predictionloop

# Load the pretrained model and tokenizer from the local 'models' directory
tokenizer, model = load_local_model("models")

# Set up the Streamlit app UI
st.title("Automated Lie Detector")
st.write("Do you want to know if your autobiographical statement is truthful or deceptive?")
st.write("If you want to test another statement, simply delete your input and press submit again.")

# Create empty containers for dynamic UI elements
input_container = st.empty()
submit_cont = st.empty()
feedback_container = st.empty()
progr_cont = st.empty()

# Text area for user input
user_input = input_container.text_area("**You can write or paste your autobiographical statement here**")

# Button for submitting the input and triggering prediction
if submit_cont.button("Submit"):
    # Run the prediction loop with the user's input
    risposta, prob = predictionloop(user_input, tokenizer, model)
    
    # Display the model's prediction and confidence score
    feedback_container.markdown(
        f"### Model Feedback\n"
        f"The model predicts that your statement is classified as **{'TRUTHFUL' if risposta == 0 else 'DECEPTIVE'}**.\n"
        f"**Confidence Score:** {prob:.2f}%"
    )
    # Show a progress bar representing the confidence score
    progr_cont.progress(int(prob))
            
