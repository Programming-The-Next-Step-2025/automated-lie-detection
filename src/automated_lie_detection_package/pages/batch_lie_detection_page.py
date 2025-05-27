import streamlit as st
import pandas as pd
from automated_lie_detection_package.utility import batch_modelprediction

st.title("Batch Lie Detection (CSV Upload)")
st.write("Upload a CSV file with a column containing autobiographical statements for batch prediction, or use the default example file.")

use_default = st.checkbox("Use default example CSV from data/autobiographical_statements.csv")

uploaded_file = None
df = None

if use_default:
    default_path = "data/autobiographical_statements.csv"
    try:
        df = pd.read_csv(default_path, sep=";", engine="python")
        st.success(f"Loaded default file: {default_path}")
    except Exception as e:
        st.error(f"Could not load default file: {e}")
else:
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, sep=None, engine="python")

column_name = st.text_input("Column name containing statements", value="statement")

if df is not None:
    st.write("Preview of data:")
    st.dataframe(df.head())

    if column_name not in df.columns:
        st.error(f"Column '{column_name}' not found in the data.")
    else:
        if st.button("Run Batch Prediction"):
            # Save file temporarily
            temp_input = "data/temp_uploaded.csv"
            df.to_csv(temp_input, index=False)
            output_file = "data/exp_data/batch_predictions_from_upload.csv"
            results_df = batch_modelprediction(
                input_file=temp_input,
                output_file=output_file,
                column=column_name
            )
            st.success("Batch prediction complete!")
            st.dataframe(results_df)
            csv = results_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download results as CSV",
                data=csv,
                file_name="batch_predictions.csv",
                mime="text/csv"
            )