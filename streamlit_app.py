import streamlit as st
import pandas as pd
import numpy as np
import os
import re
from topsisalgorithm import topsis
import smtplib
from email.message import EmailMessage

# Page configuration
st.set_page_config(page_title="TOPSIS Analysis", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 TOPSIS Analysis Tool")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    st.info("TOPSIS: Technique for Order of Preference by Similarity to Ideal Solution")

# Create folders if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("results", exist_ok=True)

def send_email(to_email, file_path):
    """Send result file via email"""
    try:
        msg = EmailMessage()
        msg['Subject'] = 'TOPSIS Result File'
        msg['From'] = "krishmahajan555@gmail.com"
        msg['To'] = to_email
        msg.set_content("Attached is your TOPSIS result file.")

        with open(file_path, 'rb') as f:
            msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename="result.csv")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("krishmahajan555@gmail.com", "ofrqiftdrekaiirw")
            smtp.send_message(msg)
        
        return True, "Email sent successfully!"
    except Exception as e:
        return False, f"Error sending email: {str(e)}"

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Upload Data File")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("**Preview of your data:**")
        st.dataframe(df.head())

with col2:
    st.subheader("Email Configuration")
    email = st.text_input("Enter your email address", placeholder="your.email@example.com")

st.markdown("---")

# Input parameters
col1, col2 = st.columns(2)

with col1:
    weights_input = st.text_input(
        "Enter weights (comma-separated)",
        placeholder="e.g., 0.25,0.25,0.25,0.25",
        help="Weights must sum to 1 or will be normalized"
    )

with col2:
    impacts_input = st.text_input(
        "Enter impacts (comma-separated: +/-)",
        placeholder="e.g., +,-,+,+",
        help="Use + for benefit criteria, - for cost criteria"
    )

# Process button
if st.button("🚀 Run TOPSIS Analysis", use_container_width=True):
    if uploaded_file is None:
        st.error("❌ Please upload a CSV file first")
    elif not weights_input.strip() or not impacts_input.strip():
        st.error("❌ Please enter weights and impacts")
    elif not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        st.error("❌ Please enter a valid email address")
    else:
        try:
            # Parse inputs
            weights = list(map(float, weights_input.split(',')))
            impacts = [i.strip() for i in impacts_input.split(',')]
            
            # Validation
            if len(weights) != len(impacts):
                st.error("❌ Number of weights must match number of impacts")
            elif len(weights) != len(df.columns) - 1:
                st.error(f"❌ Number of weights/impacts ({len(weights)}) must match number of columns ({len(df.columns) - 1})")
            elif not all(i in ['+', '-'] for i in impacts):
                st.error("❌ Impacts must contain only '+' or '-'")
            else:
                # Run TOPSIS
                with st.spinner("Processing TOPSIS analysis..."):
                    # Save uploaded file
                    upload_path = f"uploads/{uploaded_file.name}"
                    with open(upload_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Call topsis with weights and impacts as strings
                    result_path = "results/result.csv"
                    weights_str = ','.join(map(str, weights))
                    impacts_str = ','.join(impacts)
                    
                    topsis(upload_path, weights_str, impacts_str, result_path)
                    result_df = pd.read_csv(result_path)
                    
                    st.success("✅ Analysis completed successfully!")
                    
                    # Display results
                    st.subheader("Results")
                    st.dataframe(result_df, use_container_width=True)
                    
                    # Download button
                    csv_data = result_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Results as CSV",
                        data=csv_data,
                        file_name="topsis_result.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                    # Send email
                    if st.button("📧 Send Results via Email", use_container_width=True):
                        with st.spinner("Sending email..."):
                            success, message = send_email(email, result_path)
                            if success:
                                st.success(f"✅ {message}")
                            else:
                                st.error(f"⚠️ {message}")
        
        except ValueError as e:
            st.error(f"❌ Invalid input: {str(e)}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
