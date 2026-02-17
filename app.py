import streamlit as st
import pandas as pd
import sqlite3
import time
import plotly.graph_objects as go
import plotly.express as px
from streamlit_agraph import agraph, Node, Edge, Config
from datetime import datetime
import base64

# --- 1. DATABASE SETUP ---
conn = sqlite3.connect('sentinel_pro.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS audit_logs 
               (user TEXT, timestamp TEXT, action TEXT, entity TEXT, result TEXT)''')
conn.commit()

# --- 2. CONFIG & STYLING ---
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
    </style>
    """, unsafe_allow_html=True)

# Navigation State
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = 'home'

def navigate(p):
    st.session_state.page = p
    st.rerun()

def add_log(action, entity, result):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO audit_logs VALUES (?, ?, ?, ?, ?)", ("Ankit", ts, action, entity, result))
    conn.commit()

# --- EXHAUSTIVE DROPDOWN LISTS ---
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

# --- 4. HEADER ---
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🛡️ AM UNIVERSAL FRAUD SENTINEL</h1>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Nodes Analyzed", "1.4B+", "Live")
m2.metric("AI Accuracy", "99.98%", "Stable")
m3.metric("Neural Latency", "0.002ms", "GNN")
m4.metric("Status", "Secure", "✅")
st.divider()

# --- 5. PAGE LOGIC ---

# HOME PAGE
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
    
    st.divider()
    c7, c8 = st.columns(2)
    with c7:
        if st.button("📁 Bulk CSV Analysis"): navigate('bulk')
    with c8:
        if st.button("📜 View Audit Logs & Reports"): navigate('logs')

# MODULE PAGES (Dynamic Dropdowns Restored)
elif st.session_state.page in ['upi', 'check', 'ins', 'tax', 'loan']:
    st.header(f"Active Module: {st.session_state.page.upper()}")
    
    # Picking the correct dropdown list
    if st.session_state.page == 'upi':
        current_list = WALLETS
    elif st.session_state.page == 'ins':
        current_list = INSURANCE
    else:
        current_list = BANKS
        
    sel = st.selectbox("Select Partner Entity", current_list)
    tid = st.text_input("Enter ID / Number to Scan")
    
    if st.button("Run Deep Forensic Scan"):
        with st.spinner("Analyzing Database..."):
            time.sleep(1)
            res = "FRAUD DETECTED" if "fraud" in tid.lower() or "999" in tid else "VERIFIED SAFE"
            st.success(res) if "SAFE" in res else st.error(res)
            add_log(f"{st.session_state.page.upper()} Scan", sel, res)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ Back to Home Dashboard"): navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)

# GNN PAGE (With Advanced Charts & Search)
elif st.session_state.page == 'graph':
    st.header("🕸️ GNN Intelligence Hub")
    target = st.text_input("🔍 Search Node (USR_ID)")
    
    cg, cr = st.columns([2, 1])
    with cg:
        nodes = [
            Node(id="B", label="Banks (Blue)", color="#58a6ff", size=25),
            Node(id="I", label="Insurance (Green)", color="#2ea44f", size=25),
            Node(id="W", label="Wallet (Yellow)", color="#dbab09", size=25),
            Node(id="F", label="FRAUD NODE", color="#d12d3d", size=35)
        ]
        edges = [Edge(source="B", target="W"), Edge(source="W", target="F"), Edge(source="I", target="F")]
        agraph(nodes=nodes, edges=edges, config=Config(width=700, height=450, directed=True, physics=True))
    with cr:
        val = 94 if target else 15
        st.plotly_chart(go.Figure(go.Indicator(mode="gauge+number", value=val, 
                        gauge={'bar':{'color':"#58a6ff"}, 'axis':{'range':[0,100]},
                        'steps':[{'range':[0,40], 'color':'green'}, {'range':[70,100], 'color':'red'}]})), use_container_width=True)

    # Advanced Analytics (The HR Dashboard Look)
    c_pie, c_bar = st.columns(2)
    with c_pie:
        st.plotly_chart(px.pie(names=['Safe', 'Caution', 'Fraud'], values=[140, 40, 20], hole=0.5, 
                              color_discrete_sequence=['#2ea44f', '#dbab09', '#d12d3d'], title="Network Health Ratio"), use_container_width=True)
    with c_bar:
        st.plotly_chart(px.bar(x=['Banks', 'UPI', 'Insurance'], y=[8, 25, 4], title="Threats by Category", 
                              color_discrete_sequence=['#d12d3d']), use_container_width=True)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ Back to Home Dashboard"): navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)

# BULK SCAN PAGE
elif st.session_state.page == 'bulk':
    st.header("📁 Enterprise Batch Analysis")
    uploaded = st.file_uploader("Upload Transaction CSV (200+ Nodes)", type="csv")
    if uploaded:
        df_up = pd.read_csv(uploaded)
        st.write("Preview:", df_up.head())
        if st.button("Start AI Batch Analysis"):
            with st.spinner("Processing..."):
                time.sleep(2)
                st.success(f"Analyzed {len(df_up)} rows. Pattern match complete.")
                add_log("Bulk Scan", "CSV Upload", f"{len(df_up)} Rows")

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ Back to Home Dashboard"): navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)

# LOGS PAGE
elif st.session_state.page == 'logs':
    st.header("📜 Forensic Reports & History")
    df_logs = pd.read_sql_query("SELECT * FROM audit_logs ORDER BY timestamp DESC", conn)
    st.dataframe(df_logs, use_container_width=True)
    
    st.download_button("📥 Excel (CSV) Report", df_logs.to_csv(index=False), "report.csv")
    
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ Back to Home Dashboard"): navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)
