import streamlit as st
import pandas as pd

# Title of the web app
st.title("Simple Data Upload, Cleaning, and Display Website")

# File uploader widget
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Data Preview")
    st.dataframe(data)

    st.subheader("Basic Data Information")
    st.write(f"Number of rows: {data.shape[0]}")
    st.write(f"Number of columns: {data.shape[1]}")

    st.subheader("Summary Statistics")
    st.write(data.describe())

    st.subheader("Data Cleaning")

    # Let user select columns to check for duplicates
    columns = list(data.columns)
    selected_cols = st.multiselect("Select columns to check duplicates for (default: all columns)", options=columns, default=columns)

    # Remove duplicates based on selected columns
    if st.button("Remove Duplicates"):
        if selected_cols:
            data = data.drop_duplicates(subset=selected_cols)
            st.success("Duplicates removed based on selected columns.")
        else:
            st.warning("Please select at least one column.")

    # Handling missing values
    missing_option = st.selectbox("How to handle missing values?", 
                                  ["Do nothing",
                                   "Drop rows with missing values",
                                   "Fill missing numeric values with mean",
                                   "Fill missing values with zero"])

    if missing_option == "Drop rows with missing values":
        data = data.dropna()
        st.success("Rows with missing values dropped.")
    elif missing_option == "Fill missing numeric values with mean":
        for col in data.select_dtypes(include=['float64', 'int64']).columns:
            data[col].fillna(data[col].mean(), inplace=True)
        st.success("Missing numeric values filled with mean.")
    elif missing_option == "Fill missing values with zero":
        data.fillna(0, inplace=True)
        st.success("Missing values filled with zero.")

    # Strip whitespace from string columns
    def strip_whitespace(df):
        str_cols = df.select_dtypes(include=['object']).columns
        for col in str_cols:
            df[col] = df[col].str.strip()
        return df

    data = strip_whitespace(data)

    st.subheader("Cleaned Data Preview")
    st.dataframe(data)

    st.subheader("Cleaned Data Information")
    st.write(f"Number of rows: {data.shape[0]}")
    st.write(f"Number of columns: {data.shape[1]}")

    st.subheader("Cleaned Data Summary Statistics")
    st.write(data.describe())

else:
    st.info("Please upload a CSV file to see data preview and cleaning options.")
