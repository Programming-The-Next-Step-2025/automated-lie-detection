import streamlit as st
import pandas as pd
from automated_lie_detection_package.utility import batch_modelprediction
import csv
import matplotlib.pyplot as plt

# Page text
st.title("Lie Detection of Multiple Statements")
st.write("Upload a CSV file with a column containing autobiographical statements for batch prediction, or use the default example file.")

# Default CSV
use_default = st.checkbox("Use default example CSV from data/autobiographical_statements.csv")

uploaded_file = None
df = None

# Data upload
if use_default:
    default_path = "data/autobiographical_statements.csv"
    try:
        df = pd.read_csv(default_path, sep=";")
        st.success(f"Loaded default file: {default_path}")
    except Exception as e:
        st.error(f"Could not load default file: {e}")
else:
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        # Auto-detect separator 
        sample = uploaded_file.read(2048).decode("utf-8")
        uploaded_file.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
            sep = dialect.delimiter
        except Exception:
            sep = ","
        df = pd.read_csv(uploaded_file, sep=sep)

# Data preview and column choice
if df is not None:
    st.write("Preview of data:")
    st.dataframe(df.head())
    # Let user pick the column
    possible_columns = list(df.columns)
    if possible_columns:
        default_col = "statement" if "statement" in possible_columns else possible_columns[0]
        column_name = st.selectbox(
            "Column name containing statements",
            possible_columns,
            index=possible_columns.index(default_col)
        )
    else:
        st.error("No suitable columns found in the data.")
        column_name = None

# Batch prediction and results
if df is not None and column_name:
    if st.button("Run Batch Prediction"):
        # Save the DataFrame to a temporary CSV with sep=";"
        temp_input = "data/temp_uploaded.csv"
        df.to_csv(temp_input, index=False, sep=";")
        output_file = "data/exp_data/batch_predictions_from_upload.csv"
        results_df = batch_modelprediction(
            input_file=temp_input,
            output_file=output_file,
            column=column_name
        )
        st.success("Prediction complete!")
        st.dataframe(results_df)
        csv_bytes = results_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download results as CSV",
            data=csv_bytes,
            file_name="batch_predictions.csv",
            mime="text/csv"
        )

        # Visualization 
        st.subheader("Prediction Distribution")
        # Bar chart
        st.bar_chart(results_df["prediction"].value_counts())
        # Pie chart
        st.write("Pie Chart:")
        st.pyplot(
            results_df["prediction"].value_counts().plot.pie(
                autopct='%1.1f%%', ylabel='', title='Truthful vs. Deceptive'
            ).get_figure()
        )

        # Confidence score visualization
        st.subheader("Confidence Score Distribution")

        # Convert confidence column to float if needed
        results_df["confidence_float"] = results_df["confidence (%)"].astype(float)

        # Histogram of all confidence scores
        fig, ax = plt.subplots()
        ax.hist(results_df["confidence_float"], bins=10, color="skyblue", edgecolor="black")
        ax.set_xlabel("Confidence (%)")
        ax.set_ylabel("Number of Statements")
        ax.set_title("Histogram of Confidence Scores")
        st.pyplot(fig)

        # Boxplot grouped by prediction
        fig2, ax2 = plt.subplots()
        results_df.boxplot(column="confidence_float", by="prediction", ax=ax2)
        ax2.set_ylabel("Confidence (%)")
        ax2.set_title("Confidence by Prediction")
        plt.suptitle("")
        st.pyplot(fig2)