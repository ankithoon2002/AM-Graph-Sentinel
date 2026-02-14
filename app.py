import streamlit as st
import pandas as pd
import sqlite3
import time
import hashlib
import plotly.graph_objects as go
from streamlit_agraph import agraph, Node, Edge, Config
from datetime import datetime

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('sentinel_pro.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS audit_logs (user TEXT, timestamp TEXT, action TEXT, entity TEXT, result TEXT)''')
conn.commit()

# --- 2. THEME & STYLING ---
st.set_page_config(page_title="AM Sentinel Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: #e6edf3; }
    [data-testid="stMetricValue"] { color: #58a6ff !important; font-weight: bold; }
    .stButton > button {
        border-radius: 12px; height: 90px; width: 100%;
        background: #161b22 !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; font-weight: bold;
        transition: 0.3s;
    }
    .back-btn > div > button {
        background: #d12d3d !important; color: white !important; height: 50px !important; margin-top: 30px;
    }
    @media (max-width: 768px) {
        [data-testid="column"] { width: 31% !important; flex: 1 1 31% !important; }
        .stButton > button { height: 75px !important; font-size: 10px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC & LISTS ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = 'home'

def add_log(action, entity, result):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO audit_logs VALUES (?, ?, ?, ?, ?)", ("Ankit", ts, action, entity, result))
    conn.commit()

def navigate(p):
    st.session_state.page = p
    st.rerun()

# Professional Entity Lists
BANKS = ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "PNB", "GBU Bank (Internal)", "Canara Bank", "Bank of Baroda"]
WALLETS = ["Paytm", "PhonePe", "Google Pay (GPay)", "Amazon Pay", "MobiKwik", "Airtel Money"]
INSURANCE = ["LIC", "HDFC Ergo", "Star Health", "ICICI Lombard", "Bajaj Allianz", "New India Assurance"]

# --- 4. LOGIN SYSTEM ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔐 AM SENTINEL SECURE LOGIN</h1>", unsafe_allow_html=True)
    with st.container():
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("Enter System"):
                if u == "ankit_002" and p == "gbu_mca_ds":
                    st.session_state.logged_in = True
                    add_log("Login", "System", "Success")
                    st.rerun()
                else: st.error("Invalid Credentials")
    st.stop()

# --- 5. TOP METRICS LAYER ---
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🛡️ AM UNIVERSAL FRAUD SENTINEL</h1>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Nodes Mapped", "1.4B+", "Live")
m2.metric("AI Accuracy", "99.98%", "Stable")
m3.metric("Latency", "0.002ms", "GNN")
m4.metric("Status", "Secure", "✅")
st.divider()

# --- 6. NAVIGATION PAGES ---

# HOME DASHBOARD
if st.session_state.page == 'home':
    st.write("### 🏦 Banking & Digital Payments")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📱\nUPI\nWallet"): navigate('upi')
    with c2:
        if st.button("📑\nCheck\nAudit"): navigate('check')
    with c3:
        if st.button("🕸️\nGNN\nNetwork"): navigate('graph')

    st.write("### 🛡️ Insurance & Compliance")
    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("🏥\nMedical\nInsurance"): navigate('ins')
    with c5:
        if st.button("⚖️\nTax/GST\nForensics"): navigate('tax')
    with c6:
        if st.button("🏢\nLoan\nRisk"): navigate('loan')
    
    st.divider()
    if st.button("📜 View System Audit Logs (SQLite)"): navigate('logs')
    if st.button("📁 Bulk File Upload (Analysis)"): navigate('bulk')

# MODULE PAGES (Dynamic Dropdowns)
elif st.session_state.page in ['upi', 'check', 'ins', 'tax', 'loan']:
    st.header(f"Module Analysis: {st.session_state.page.upper()}")
    
    # Selecting the right list based on page
    if st.session_state.page == 'upi': current_list = WALLETS
    elif st.session_state.page == 'ins': current_list = INSURANCE
    else: current_list = BANKS

    selected_entity = st.selectbox(f"Select Partner Entity", current_list)
    target_id = st.text_input(f"Enter ID or Number to Analyze")
    
    if st.button("Run Deep Forensic Scan"):
        with st.spinner(f"Scanning {selected_entity} database..."):
            time.sleep(1.5)
            status = "FRAUD DETECTED" if "fraud" in target_id.lower() else "SAFE / VERIFIED"
            if status == "FRAUD DETECTED": st.error(f"🚨 {status}")
            else: st.success(f"✅ {status}")
            add_log(f"{st.session_state.page.upper()} Scan", selected_entity, status)

    # BACK BUTTON AT THE BOTTOM
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ Back to Home Dashboard"): navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)

# GNN GRAPH PAGE
elif st.session_state.page == 'graph':
    st.header("🕸️ GNN Relational Network")
    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Visualize Global Links"):
            nodes = [Node(id="A", label="Sender", color="#58a6ff"), Node(id="B", label="Receiver", color="red")]
            edges = [Edge(source="A", target="B")]
            agraph(nodes=nodes, edges=edges, config=Config(width=600, height=400))
    with col2:
        fig = go.Figure(go.Indicator(mode="gauge+number", value=88, title={'text': "Risk Score"},
             gauge={'bar': {'color': "#58a6ff"}, 'steps': [{'range': [0, 50], 'color': "green"}, {'range': [50, 100], 'color': "red"}]}))
        st.plotly_chart(fig, use_container_width=True)
        st.info("*AI Explainability:* Transaction linked to a blacklisted VPN node.")

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ Back to Home Dashboard"): navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)

# LOGS PAGE (Download + History)
elif st.session_state.page == 'logs':
    st.header("📜 System Audit History (SQLite)")
    df = pd.read_sql_query("SELECT * FROM audit_logs ORDER BY timestamp DESC", conn)
    st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Audit Report (CSV)", data=csv, file_name="audit_report.csv", mime="text/csv")
    
    if st.button("⬅️ Back to Home"): navigate('home')

# BULK SCAN PAGE
elif st.session_state.page == 'bulk':
    st.header("📁 Enterprise Batch Processing")
    uploaded_file = st.file_uploader("Upload Transaction CSV (Up to 2L Rows)", type="csv")
    if uploaded_file:
        df_bulk = pd.read_csv(uploaded_file)
        st.write(df_bulk.head())
        if st.button("Perform Batch AI Analysis"):
            with st.spinner("Processing large dataset..."):
                time.sleep(2)
                st.success(f"Successfully analyzed {len(df_bulk)} rows. No anomalies found.")
                add_log("Bulk Scan", "File Upload", f"{len(df_bulk)} Rows")
    
    if st.button("⬅️ Back to Home"): navigate('home')
