import streamlit as st
import json
import pandas as pd

# Load data
with open("data/programs.json") as f:
    data = json.load(f)

df = pd.DataFrame(data)

st.title("🎓 PhD Path Predictor")

st.markdown("Find PhD programs in the US based on your preferences.")

# New: Keyword search bar
keyword = st.text_input("Search by keyword (e.g., AI, Robotics, University name)")

# Filters
funding_filter = st.selectbox("Require Funding?", ["Any", "Yes", "No"])
visa_filter = st.selectbox("Need Visa Support?", ["Any", "Yes", "No"])
gre_filter = st.selectbox("Require GRE?", ["Any", "Yes", "No"])
location_filter = st.text_input("Filter by location (city or state)")

# Apply filters
filtered_df = df.copy()

# Apply keyword filter
if keyword:
    filtered_df = filtered_df[
        filtered_df["program"].str.contains(keyword, case=False) |
        filtered_df["university"].str.contains(keyword, case=False)
    ]

# Apply location filter
if location_filter:
    filtered_df = filtered_df[
        filtered_df["location"].str.contains(location_filter, case=False)
    ]

# Apply dropdown filters
if funding_filter != "Any":
    filtered_df = filtered_df[filtered_df["funding"] == funding_filter]

if visa_filter != "Any":
    filtered_df = filtered_df[filtered_df["visa_support"] == visa_filter]

if gre_filter != "Any":
    filtered_df = filtered_df[filtered_df["gre_required"] == gre_filter]

# Show results
st.subheader(f"Matching Programs ({len(filtered_df)})")
st.dataframe(filtered_df.reset_index(drop=True))
