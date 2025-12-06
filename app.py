# In app.py

import streamlit as st
import pandas as pd
from etl.pipeline import run_pipeline
import io

st.title("ETL Pipeline Runner")

# Use st.session_state to persist data across reruns
if 'data_available' not in st.session_state:
    st.session_state['data_available'] = False
if 'pipeline_output' not in st.session_state:
    st.session_state['pipeline_output'] = None

def execute_pipeline():
    """Runs the ETL pipeline and stores the result in session state."""
    with st.spinner("Running ETL pipeline... This may take a moment."):
        df = run_pipeline()
        st.session_state['pipeline_output'] = df
        st.session_state['data_available'] = True
    st.success("Pipeline executed successfully!")

# The "Run Pipeline" button triggers the execution function
st.button("Run ETL Pipeline", on_click=execute_pipeline)

# Conditional display for the download button once data is available
if st.session_state['data_available']:
    st.subheader("Pipeline Output Preview")
    # Display the dataframe in the app
    st.dataframe(st.session_state['pipeline_output'])

    # Function to convert the DataFrame to CSV format for download
    @st.cache_data # Caching the conversion prevents recomputation on every rerun
    def convert_df_to_csv(df):
        # returns the data as a byte string in utf-8 encoding
        return df.to_csv(index=False).encode('utf-8')

    csv_data = convert_df_to_csv(st.session_state['pipeline_output'])

    # The download button uses the prepared CSV data
    st.download_button(
        label="Download Results as CSV",
        data=csv_data,
        file_name='pipeline_output.csv',
        mime='text/csv',
    )
