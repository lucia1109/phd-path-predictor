import streamlit as st
import json
from openai import OpenAI
from groq import Groq


# Load dataset
with open("data/programs.json") as f:
    programs = json.load(f)

# Configure OpenAI
#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
client = Groq(api_key=st.secrets["OPENAI_API_KEY"])

# Tabs for search and chatbot
tab1, tab2 = st.tabs(["🔍 Search Programs", "🤖 Chatbot"])

# -------------------------
# Tab 1: Search
# -------------------------
with tab1:
    st.title("PhD Path Predictor - Search 🔍")

    # Example filter UI
    query = st.text_input("Search by keyword:")
    funding_filter = st.selectbox("Funding?", ["Any", "Yes", "No"])
    gre_filter = st.selectbox("GRE Required?", ["Any", "Yes", "No"])

    results = []
    for p in programs:
        if query.lower() in p["program"].lower():
            if (funding_filter == "Any" or p["funding"] == funding_filter) and \
               (gre_filter == "Any" or p["gre_required"] == gre_filter):
                results.append(p)

    st.write(f"Found {len(results)} matching programs")
    for r in results:
        st.write(f"**{r['university']}** - {r['program']} ({r['location']})")
        st.caption(f"Funding: {r['funding']}, GRE: {r['gre_required']}, Visa: {r['visa_support']}")

# -------------------------
# Tab 2: Chatbot
# -------------------------
with tab2:
    st.title("PhD Path Predictor - Assistant 🤖")

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    user_input = st.text_input("Ask me about PhD programs:", key="chat_input")

    if st.button("Send", key="chat_send") and user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Add dataset as context
        context = "\n".join([
            f"{p['university']} - {p['program']} ({p['location']}, Funding: {p['funding']}, GRE: {p['gre_required']}, Visa: {p['visa_support']})"
            for p in programs
        ])

        # Prepare prompt for Groq
        system_prompt = (
            "You are a helpful assistant for PhD program advice.\n"
            f"Here is the dataset of programs:\n{context}\n"
        )

        # Combine messages for context
        chat_history = "\n".join([
            f"{msg['role']}: {msg['content']}" for msg in st.session_state["messages"]
        ])

        # Query Groq Llama 3.1
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt + chat_history}],
            model="llama3-70b-8192"
        )

        answer = response.choices[0].message.content
        st.session_state["messages"].append({"role": "assistant", "content": answer})

    # Display chat
    for msg in st.session_state["messages"]:
        role = "🧑 You" if msg["role"] == "user" else "🤖 Assistant"
        st.write(f"**{role}:** {msg['content']}")
