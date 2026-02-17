import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from streamlit_agraph import agraph, Node, Edge, Config
from datetime import datetime
import random

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('sentinel_final.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS audit_logs (user TEXT, timestamp TEXT, action TEXT, status TEXT, risk INTEGER, reason TEXT)')
conn.commit()

st.set_page_config(page_title="AM Universal Fraud Sentinel", layout="wide")

# CLASSIC THEME (Wahi purana look)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton > button { height: 90px; width: 100%; font-size: 22px; font-weight: bold; border-radius: 15px; background-color: #1f2937 !important; border: 2px solid #3b82f6 !important; }
    .stButton > button:hover { background-color: #3b82f6 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'page' not in st.session_state: st.session_state.page = 'home'

# --- 2. SIDEBAR: Naye Advance Features Yahan Hain ---
with st.sidebar:
    st.title("⚙️ Advanced Settings")
    if st.session_state.auth:
        st.write(f"User: *{st.session_state.user}*")
        st.divider()
        # Naya Advance Control
        enable_map = st.checkbox("Show Global Risk Heatmap", value=False)
        enable_ticker = st.checkbox("Enable Live Threat Feed", value=False)
        auto_resolve = st.toggle("Auto-Problem Resolution", value=True)
        st.divider()
        if st.button("🚪 Logout"):
            st.session_state.auth = False
            st.rerun()
    else:
        st.info("Login to access advanced tools.")

# --- 3. LOGIN PAGE ---
if not st.session_state.auth:
    st.title("🛡️ AM SENTINEL - ENTERPRISE LOGIN")
    col1, col2 = st.columns([1, 1])
    with col1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Access Dashboard"):
            if (u == "ankit" and p == "123") or (u == "admin" and p == "admin"):
                st.session_state.auth = True
                st.session_state.user = u
                st.rerun()
            else: st.error("Invalid Credentials")
    st.stop()

# --- 4. LIVE TICKER (Agar Sidebar se ON ho) ---
if enable_ticker:
    st.markdown(f'<p style="color:#58a6ff; font-family:monospace; background:#161b22; padding:10px; border-radius:5px;">● LIVE FEED: {random.choice(["Scanning UPI Gateway...", "Analyzing IP 102.16.x.x", "Monitoring Bank-Node-Alpha"])}</p>', unsafe_allow_html=True)

# --- 5. MAIN DASHBOARD (PURANA WAHI LOOK) ---
if st.session_state.page == 'home':
    st.title("🛡️ AM UNIVERSAL FRAUD SENTINEL")
    st.write("### Welcome, Investigator. Select a module to begin.")
    
    # Wahi purane 6 bade buttons
    row1_col1, row1_col2, row1_col3 = st.columns(3)
    with row1_col1:
        if st.button("📱 UPI / Wallet"): st.session_state.page = 'upi'
    with row1_col2:
        if st.button("🏛️ Bank Accounts"): st.session_state.page = 'bank'
    with row1_col3:
        if st.button("📄 Insurance Claims"): st.session_state.page = 'insurance'

    row2_col1, row2_col2, row2_col3 = st.columns(3)
    with row2_col1:
        if st.button("🕸️ GNN Network"): st.session_state.page = 'graph'
    with row2_col2:
        if st.button("📁 Bulk Analysis"): st.session_state.page = 'bulk'
    with row2_col3:
        if st.button("📜 Audit Logs"): st.session_state.page = 'logs'

    # Naya Heatmap Feature (Sirf tab dikhega jab tum Sidebar se ON karoge)
    if enable_map:
        st.divider()
        st.subheader("🌍 Regional Threat Heatmap")
        map_df = pd.DataFrame({'lat': [28.6, 19.0, 55.7], 'lon': [77.2, 72.8, 37.6], 'risk': [20, 50, 95]})
        fig = px.scatter_mapbox(map_df, lat="lat", lon="lon", size="risk", color="risk", mapbox_style="carto-darkmatter", zoom=1)
        st.plotly_chart(fig, use_container_width=True)

# --- 6. ADVANCED MODULE LOGIC (With Automatic Update) ---
elif st.session_state.page == 'upi':
    st.header("📱 UPI Forensic Scanner")
    target = st.text_input("Enter UPI ID or Mobile Number")
    amt = st.number_input("Transaction Amount", min_value=0)
    
    if st.button("Scan Account"):
        # Automatic Problem-wise Logic
        risk = 92 if "fraud" in target.lower() or amt > 500000 else 15
        st.metric("Risk Score", f"{risk}%")
        
        if risk > 50:
            st.error("🚨 ALERT: High Risk Detected!")
            if auto_resolve:
                st.warning("⚡ Automatic Action: Problem categorized as 'High Value Anomaly'. Account placed under 24h freeze.")
        else:
            st.success("✅ Verified Safe Transaction")

    if st.button("⬅️ Back to Dashboard"): 
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'graph':
    st.header("🕸️ GNN Intelligence - Money Trail")
    # Purana Graph Visualization
    nodes = [Node(id="A", label="User", color="green"), Node(id="B", label="Suspect", color="red")]
    edges = [Edge(source="A", target="B")]
    agraph(nodes=nodes, edges=edges, config=Config(width=800, height=500))
    if st.button("⬅️ Back"): 
        st.session_state.page = 'home'
        st.rerun()

elif st.session_state.page == 'logs':
    st.header("📜 Forensic Audit Logs")
    # Display log table from database
    st.write("Fetching latest forensics reports...")
    if st.button("⬅️ Back"): 
        st.session_state.page = 'home'
        st.rerun()
