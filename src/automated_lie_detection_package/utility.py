import joblib
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import streamlit as st

def load_model(model_path):
    """
    Loads a machine learning model from a specified file path.

    Args:
        model_path: The file path to the saved model.

    Returns:
        The loaded machine learning model.
    """
    return joblib.load(model_path)

#models and tokenizer
tokenizer = AutoTokenizer.from_pretrained('XXX')
#model = load_file('models/fine_tuned_model/model.safetensors')
model = AutoModelForSequenceClassification.from_pretrained('XXX', use_safetensors=True)

def predictionloop(frase):
    """
    Process the input text and generate prediction and confidence score.
    Args:
        frase: The input text to be processed.
    Returns:
        risposta: The prediction result (1 for truthful, 0 for deceptive).
        prob: The confidence score of the prediction.
    """
     # Tokenize the text and convert to input IDs
    inputs = tokenizer(frase, return_tensors="pt")

    # Get logits, predicted probabilities, and predicted label
    outputs = model(**inputs)
    probabilities = outputs.logits.softmax(dim=-1)  
    predicted_label = probabilities.argmax().item()

    # Get the class probability 
    class_prob = probabilities[0, predicted_label].item()
    return 1-predicted_label, class_prob*100

def modelprediction(input_text):
    """
    Classifies a statement as 'truthful' or 'deceptive' and returns the predicted class and confidence score.

    Args:
        input_text: The input string to classify.

    Returns:
        predicted_class: 'truthful' or 'deceptive'
        confidence: Confidence score as a percentage (float)
    """
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model(**inputs)
    probabilities = outputs.logits.softmax(dim=-1)
    predicted_label = probabilities.argmax().item()
    class_prob = probabilities[0, predicted_label].item()
    class_name = "truthful" if predicted_label == 0 else "deceptive"
    message = f"The statement was classified as {class_name} with {class_prob * 100:.2f}% confidence."
    return message



