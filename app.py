import streamlit as st
import pandas as pd
import joblib

# Load the model
model = joblib.load("spoof_model.pkl")

st.set_page_config(page_title="DNS Spoof Detection", page_icon="🛡️")
st.title("🛡️ DNS Spoofing Detection App")
st.markdown("Upload your DNS log data to detect spoofing attacks using a trained ML model.")

# Upload CSV
uploaded_file = st.file_uploader("📤 Upload your CSV file here", type=["csv"])

if uploaded_file is not None:
    # Read the file
    try:
        data = pd.read_csv(uploaded_file)

        # Drop timestamp if present
        if 'timestamp' in data.columns:
            data = data.drop('timestamp', axis=1)

        # Label encode any object columns
        for col in data.columns:
            if data[col].dtype == 'object':
                data[col] = data[col].astype('category').cat.codes

        # Make prediction
        preds = model.predict(data)

        # Add prediction result to dataframe
        result = data.copy()
        result['Prediction'] = preds
        result['Prediction'] = result['Prediction'].map({0: 'Normal', 1: 'Spoofed'})

        st.success("✅ Prediction Complete!")
        st.dataframe(result[['Prediction']])

        # Option to download result
        csv = result.to_csv(index=False)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name='spoof_detection_results.csv',
            mime='text/csv'
        )
    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
