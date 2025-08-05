# app.py

import streamlit as st
import json
import os
from datetime import datetime

LOG_FILE = "frontend/log.json"

st.set_page_config(page_title="Silver News Alerts", layout="wide")
st.title("🧠 Silver AI News Dashboard")
st.markdown("Latest AI-processed silver-related news alerts, directly from MCX/COMEX & global headlines.")

# Check if log file exists
if not os.path.exists(LOG_FILE):
    st.warning("No alerts logged yet. Run the bot at least once.")
    st.stop()

# Load and display logs
with open(LOG_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

if not data:
    st.info("No news alerts available yet.")
else:
    st.success(f"Showing {len(data)} latest news summaries:")

    for article in reversed(data[-15:]):
        st.markdown("---")
        st.subheader(f"📰 {article['title']}")
        st.markdown(f"**🧠 Summary:** {article['summary']}")
        st.markdown(f"🔗 [Read More]({article['link']})")
        st.caption(f"📅 Published: {article['published']}")
