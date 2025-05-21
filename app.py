import streamlit as st
import json
import pandas as pd

# Load data
with open("data/programs.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)

st.title("🎓 PhD Path Predictor")

st.markdown("Find PhD programs in the US based on your preferences.")

# Filters
funding_filter = st.selectbox("Require Funding?", ["Any", "Yes", "No"])
visa_filter = st.selectbox("Need Visa Support?", ["Any", "Yes", "No"])
gre_filter = st.selectbox("Require GRE?", ["Any", "Yes", "No"])

# Apply filters
filtered_df = df.copy()

if funding_filter != "Any":
    filtered_df = filtered_df[filtered_df["funding"] == funding_filter]

if visa_filter != "Any":
    filtered_df = filtered_df[filtered_df["visa_support"] == visa_filter]

if gre_filter != "Any":
    filtered_df = filtered_df[filtered_df["gre_required"] == gre_filter]

# Show results
st.subheader("Matching Programs")
st.dataframe(filtered_df.reset_index(drop=True))
