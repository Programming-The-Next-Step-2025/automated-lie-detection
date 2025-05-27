import streamlit as st
import pandas as pd
from automated_lie_detection_package.utility import batch_modelprediction
import csv

st.title("Lie Detection of Multiple Statements")
st.write("Upload a CSV file with a column containing autobiographical statements for batch prediction, or use the default example file.")

use_default = st.checkbox("Use default example CSV from data/autobiographical_statements.csv")

uploaded_file = None
df = None

if use_default:
    default_path = "data/autobiographical_statements.csv"
    try:
        # Use the same logic as batch_modelprediction
        df = pd.read_csv(default_path, sep=";")
        st.success(f"Loaded default file: {default_path}")
    except Exception as e:
        st.error(f"Could not load default file: {e}")
else:
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        # Try to auto-detect separator for robustness
        sample = uploaded_file.read(2048).decode("utf-8")
        uploaded_file.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
            sep = dialect.delimiter
        except Exception:
            sep = ","
        df = pd.read_csv(uploaded_file, sep=sep)

if df is not None:
    st.write("Preview of data:")
    st.dataframe(df.head())
    # Let user pick the column, default to "statement" if present
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

if df is not None and column_name:
    if st.button("Run Batch Prediction"):
        # Save the DataFrame to a temp CSV with sep=";"
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