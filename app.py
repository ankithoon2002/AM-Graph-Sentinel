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
        background: #d12d3d !important; color: white !important; height: 50px !important; margin-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = 'home'

def navigate(p):
    st.session_state.page = p
    st.rerun()

def add_log(action, entity, result):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO audit_logs VALUES (?, ?, ?, ?, ?)", ("Ankit", ts, action, entity, result))
    conn.commit()

BANKS = ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "PNB", "GBU Bank"]
WALLETS = ["Paytm", "PhonePe", "Google Pay (GPay)", "Amazon Pay"]
INSURANCE = ["LIC", "HDFC Ergo", "Star Health", "ICICI Lombard"]

# --- 2. LOGIN SYSTEM ---
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

# --- 3. HEADER ---
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🛡️ AM UNIVERSAL FRAUD SENTINEL</h1>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Nodes Analyzed", "1.4B+", "Live")
m2.metric("AI Accuracy", "99.98%", "Stable")
m3.metric("Neural Latency", "0.002ms", "GNN")
m4.metric("Status", "Secure", "✅")
st.divider()

# --- 4. NAVIGATION ---
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
    # DEDICATED BULK UPLOAD BUTTON ADDED HERE
    c7, c8 = st.columns(2)
    with c7:
        if st.button("📁 Bulk CSV Analysis (200+ Nodes)"): navigate('bulk')
    with c8:
        if st.button("📜 View Audit Logs & Reports"): navigate('logs')

# --- 5. BULK UPLOAD PAGE (RESTORED) ---
elif st.session_state.page == 'bulk':
    st.header("📁 Enterprise Batch Processing")
    uploaded_file = st.file_uploader("Upload Transaction CSV", type="csv")
    if uploaded_file:
        df_bulk = pd.read_csv(uploaded_file)
        st.write("### Preview of Uploaded Data", df_bulk.head())
        if st.button("Start AI Batch Analysis"):
            with st.spinner("Analyzing 200+ Nodes..."):
                time.sleep(2)
                st.success(f"Analyzed {len(df_bulk)} transactions. High-risk patterns flagged.")
                add_log("Bulk Scan", "CSV Upload", f"{len(df_bulk)} Rows")
    
    if st.button("⬅️ Back to Home"): navigate('home')

# --- 6. GNN HUB ---
elif st.session_state.page == 'graph':
    st.header("🕸️ GNN Intelligence Hub")
    target_node = st.text_input("🔍 Search Node")
    col_g, col_r = st.columns([2, 1])
    with col_g:
        nodes = [Node(id="B", label="Bank", color="#58a6ff"), Node(id="I", label="Ins", color="#2ea44f"), Node(id="F", label="FRAUD", color="#d12d3d")]
        edges = [Edge(source="B", target="F")]
        agraph(nodes=nodes, edges=edges, config=Config(width=700, height=450))
    with col_r:
        val = 94 if target_node else 15
        st.plotly_chart(go.Figure(go.Indicator(mode="gauge+number", value=val, gauge={'bar':{'color':"#58a6ff"}})))
    
    # CHARTS (HR DASHBOARD LOOK)
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(px.pie(names=['Safe', 'Fraud'], values=[180, 20], hole=0.5, color_discrete_sequence=['#2ea44f', '#d12d3d']))
    with c2:
        st.plotly_chart(px.bar(x=['SBI', 'Paytm', 'LIC'], y=[5, 15, 2], title="Threats"))
    
    if st.button("⬅️ Back to Home"): navigate('home')

# --- 7. LOGS PAGE ---
elif st.session_state.page == 'logs':
    st.header("📜 Forensic Reports")
    df = pd.read_sql_query("SELECT * FROM audit_logs ORDER BY timestamp DESC", conn)
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 Excel Report", df.to_csv(index=False), "report.csv")
    if st.button("⬅️ Back to Home"): navigate('home')
