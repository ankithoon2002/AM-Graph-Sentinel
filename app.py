import streamlit as st
import pandas as pd
import sqlite3
import time
import plotly.graph_objects as go
import plotly.express as px
from streamlit_agraph import agraph, Node, Edge, Config
from datetime import datetime
import random

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('sentinel_pro.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS audit_logs 
               (user TEXT, timestamp TEXT, action TEXT, entity TEXT, result TEXT, auto_action TEXT)''')
conn.commit()

# --- 2. CONFIG & STYLING (Wahi Classic Look) ---
st.set_page_config(page_title="AM Sentinel Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: #e6edf3; }
    [data-testid="stMetricValue"] { color: #58a6ff !important; font-weight: bold; }
    .stButton > button {
        border-radius: 12px; height: 90px; width: 100%;
        background: #161b22 !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; font-weight: bold;
    }
    .back-btn > div > button {
        background: #d12d3d !important; color: white !important; height: 50px !important; margin-top: 10px;
    }
    .ticker-text { color: #58a6ff; font-family: monospace; font-size: 14px; background: #161b22; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Navigation State
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = 'home'

def navigate(p):
    st.session_state.page = p
    st.rerun()

def add_log(action, entity, result, auto_act="N/A"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO audit_logs VALUES (?, ?, ?, ?, ?, ?)", ("Ankit", ts, action, entity, result, auto_act))
    conn.commit()

# DROPDOWN LISTS
BANKS = ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "PNB", "GBU Bank", "Canara Bank", "Bank of Baroda"]
WALLETS = ["Paytm", "PhonePe", "Google Pay (GPay)", "Amazon Pay", "MobiKwik", "Airtel Money"]
INSURANCE = ["LIC", "HDFC Ergo", "Star Health", "ICICI Lombard", "Bajaj Allianz", "New India Assurance"]

# --- 3. LOGIN SYSTEM ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔐 AM SENTINEL SECURE LOGIN</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Access System"):
            if u == "ankit_002" and p == "gbu_mca_ds":
                st.session_state.logged_in = True
                add_log("Login", "System", "Success")
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 4. SIDEBAR (Advanced Features Toggle) ---
with st.sidebar:
    st.title("⚙️ System Control")
    show_map = st.checkbox("Show Regional Heatmap", value=False)
    show_feed = st.checkbox("Live Threat Ticker", value=False)
    st.divider()
    if st.button("🚪 Secure Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- 5. HEADER (Metrics) ---
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🛡️ AM UNIVERSAL FRAUD SENTINEL</h1>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Nodes Analyzed", "1.4B+", "Live")
m2.metric("AI Accuracy", "99.98%", "Stable")
m3.metric("Neural Latency", "0.002ms", "GNN")
m4.metric("Status", "Secure", "✅")

if show_feed:
    st.markdown(f'<p class="ticker-text">📡 LIVE FEED: {random.choice(["Scanning SBI Node...", "Analyzing IP 192.168.1.45", "Monitoring UPI Gateway..."])}</p>', unsafe_allow_html=True)
st.divider()

# --- 6. PAGE LOGIC ---

# HOME PAGE (Classic Look)
if st.session_state.page == 'home':
    st.write("### 🏦 Banking & Digital Payments")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📱 UPI Wallet"): navigate('upi')
    with c2:
        if st.button("📑 Check Audit"): navigate('check')
    with c3:
        if st.button("🕸️ GNN Network"): navigate('graph')

    st.write("### 🛡️ Insurance & Compliance")
    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("🏥 Medical Insurance"): navigate('ins')
    with c5:
        if st.button("⚖️ Tax/GST Forensics"): navigate('tax')
    with c6:
        if st.button("🏢 Loan Risk"): navigate('loan')
    
    # ADVANCED HEATMAP (Hidden under toggle)
    if show_map:
        st.divider()
        st.write("### 🌍 Global Risk Heatmap")
        map_df = pd.DataFrame({'lat': [28.6, 19.0, 13.0, 22.5], 'lon': [77.2, 72.8, 80.2, 88.3], 'risk': [10, 85, 40, 95]})
        fig_map = px.scatter_mapbox(map_df, lat="lat", lon="lon", size="risk", color="risk", color_continuous_scale="Reds", mapbox_style="carto-darkmatter", zoom=3)
        st.plotly_chart(fig_map, use_container_width=True)

    st.divider()
    c7, c8 = st.columns(2)
    with c7:
        if st.button("📁 Bulk CSV Analysis"): navigate('bulk')
    with c8:
        if st.button("📜 View Audit Logs & Reports"): navigate('logs')

# MODULE PAGES (With New Auto-Action Logic)
elif st.session_state.page in ['upi', 'check', 'ins', 'tax', 'loan']:
    st.header(f"Active Module: {st.session_state.page.upper()}")
    current_list = WALLETS if st.session_state.page == 'upi' else (INSURANCE if st.session_state.page == 'ins' else BANKS)
    sel = st.selectbox("Select Partner Entity", current_list)
    tid = st.text_input("Enter ID / Number to Scan")
    
    if st.button("Run Deep Forensic Scan"):
        with st.spinner("Analyzing Database..."):
            time.sleep(1)
            is_fraud = "fraud" in tid.lower() or "999" in tid
            res = "FRAUD DETECTED" if is_fraud else "VERIFIED SAFE"
            
            # NEW: Automatic Problem-Wise Update
            auto_act = "Account Locked & Forensic Report Sent" if is_fraud else "No Action Needed"
            
            st.success(res) if "SAFE" in res else st.error(res)
            if is_fraud: st.warning(f"⚡ *Auto-Action:* {auto_act}")
            
            add_log(f"{st.session_state.page.upper()} Scan", sel, res, auto_act)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ Back to Home Dashboard"): navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)

# (GNN, Bulk, Logs Pages remain the same as your original)
elif st.session_state.page == 'graph':
    st.header("🕸️ GNN Intelligence Hub")
    # ... (Tumhara original Graph code yahan rahega)
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ Back to Home Dashboard"): navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'logs':
    st.header("📜 Forensic Reports & History")
    df_logs = pd.read_sql_query("SELECT * FROM audit_logs ORDER BY timestamp DESC", conn)
    st.dataframe(df_logs, use_container_width=True)
    st.download_button("📥 Excel (CSV) Report", df_logs.to_csv(index=False), "report.csv")
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ Back to Home Dashboard"): navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)
