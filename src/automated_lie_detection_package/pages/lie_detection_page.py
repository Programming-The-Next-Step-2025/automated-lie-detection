import streamlit as st
from automated_lie_detection_package.utility import load_local_model, predictionloop
import pandas as pd
import os
from transformers_interpret import SequenceClassificationExplainer

# Load the pretrained model and tokenizer from the local 'models' directory
tokenizer, model = load_local_model("models")

# Initialize prediction history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Page text
st.title("Lie Detection of Single Statements")
st.write("Do you want to know if your autobiographical statement is truthful or deceptive?")
st.write("If you want to test another statement, simply delete your input and press submit again.")

# Create empty containers for dynamic elements
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
        f"The model predicts that your statement is classified as **{'TRUTHFUL' if risposta == 1 else 'DECEPTIVE'}**.\n"
        f"**Confidence Score:** {prob:.2f}%"
    )
    # Show a progress bar representing the confidence score
    progr_cont.progress(int(prob))
    # Add to history
    st.session_state.history.append({
        "Statement": user_input,
        "Prediction": "TRUTHFUL" if risposta == 0 else "DECEPTIVE",
        "Confidence (%)": f"{prob:.2f}"
    })
    # Explainability
    with st.expander("Show model explainability (word importance)"):
        explainer = SequenceClassificationExplainer(model, tokenizer)
        word_attributions = explainer(user_input)
        st.markdown("**Word importances (green means more likely to be classified as predicted):**")
        highlighted_text = ""
        for word, score in word_attributions:
            color = "#ffcccc" if score < 0 else "#ccffcc"
            highlighted_text += f'<span style="background-color: {color}">{word}</span> '
        st.markdown(highlighted_text, unsafe_allow_html=True)

# Show history panel and download button if there is history
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.subheader("Prediction History")
    st.dataframe(df)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download history as CSV",
        data=csv,
        file_name="prediction_history.csv",
        mime="text/csv"
    )
    # Export to exp_data subfolder
    exp_data_dir = "data/exp_data"
    os.makedirs(exp_data_dir, exist_ok=True)
    df.to_csv(os.path.join(exp_data_dir, "prediction_history.csv"), index=False)

#Next button           
if st.button("Next"):
    st.switch_page("pages/batch_lie_detection_page.py")