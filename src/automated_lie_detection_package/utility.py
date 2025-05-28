from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import streamlit as st
import os
import gdown
import pandas as pd


def download_model_folder_from_gdrive(gdrive_folder_url="https://drive.google.com/drive/folders/1BByWnxuJ8gXWDPEWjPjAnU4iVaeQp1dZ?usp=sharing", output_dir="models"):
    """
    Downloads a folder from Google Drive and puts it into the models folder. 

    Args:
        gdrive_folder_url: The Google Drive folder URL.
        output_dir: The directory where the model folder will be placed (default: "models").

    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)
    gdown.download_folder(url=gdrive_folder_url, output=output_dir, quiet=False, use_cookies=False)

def load_local_model(model_dir="models"):
    """
    Loads a pretrained sequence classification model and its tokenizer from a local directory. 

    Args:
        model_dir: The path to the directory containing the model files 
                   (default: "models").

    Returns:
        tokenizer: The loaded tokenizer.
        model: The loaded sequence classification model.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir, use_safetensors=True)
    return tokenizer, model

def predictionloop(frase, tokenizer, model):
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
        message: A string describing the predicted class ('truthful' or 'deceptive') and the confidence score as a percentage.
    """
    tokenizer = AutoTokenizer.from_pretrained("models")
    model = AutoModelForSequenceClassification.from_pretrained("models", use_safetensors=True)
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model(**inputs)
    probabilities = outputs.logits.softmax(dim=-1)
    predicted_label = probabilities.argmax().item()
    class_prob = probabilities[0, predicted_label].item()
    class_name = "truthful" if predicted_label == 0 else "deceptive"
    message = f"The statement was classified as {class_name} with {class_prob * 100:.2f}% confidence."
    return message

def clear_models_folder(models_dir="models"):
    """
    Deletes all files and subdirectories in the specified models folder,
    except for files named '.gitkeep'.

    Args:
        models_dir: The path to the models directory (default: "models").

    Returns:
        None
    """
    if os.path.exists(models_dir):
        for filename in os.listdir(models_dir):
            if filename == ".gitkeep":
                continue
            file_path = os.path.join(models_dir, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

def batch_modelprediction(
    input_file="data/autobiographical_statements.csv",
    output_file="data/exp_data/batch_predictions.csv",
    column="statement"
):
    """
    Runs modelprediction on each statement in a CSV or TXT file and saves results to a new CSV
    with columns: statement, prediction, confidence (%).

    Args:
        input_file: Path to a CSV (with a statement column) or TXT file (one statement per line).
                    Defaults to 'data/autobiographical_statements.csv'.
        output_file: Path to save the results CSV.
                     Defaults to 'data/exp_data/batch_predictions.csv'.
        column: Name of the column in the CSV file containing statements.

    Returns:
        DataFrame with predictions.
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Detect file type
    if input_file.endswith(".csv"):
        df = pd.read_csv(input_file, sep=";")
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in CSV.")
        statements = df[column].tolist()
    elif input_file.endswith(".txt"):
        with open(input_file, "r") as f:
            statements = [line.strip() for line in f if line.strip()]
    else:
        raise ValueError("Input file must be .csv or .txt")

    results = []
    for s in statements:
        tokenizer = AutoTokenizer.from_pretrained("models")
        model = AutoModelForSequenceClassification.from_pretrained("models", use_safetensors=True)
        inputs = tokenizer(s, return_tensors="pt")
        outputs = model(**inputs)
        probabilities = outputs.logits.softmax(dim=-1)
        predicted_label = probabilities.argmax().item()
        class_prob = probabilities[0, predicted_label].item()
        class_name = "truthful" if predicted_label == 0 else "deceptive"
        results.append({
            "statement": s,
            "prediction": class_name,
            "confidence (%)": round(class_prob * 100, 2)
        })

    out_df = pd.DataFrame(results)
    out_df.to_csv(output_file, index=False)
    return out_df
