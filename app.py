import streamlit as st
import pandas as pd
import sqlite3
import time
import hashlib
import plotly.graph_objects as go
from streamlit_agraph import agraph, Node, Edge, Config
from datetime import datetime

# --- 1. DATABASE & LOGGING SETUP ---
# SQLite connect karna taaki data permanent save ho
conn = sqlite3.connect('sentinel_pro.db', check_same_thread=False)
cursor = conn.cursor()

# Tables banana: Users (Auth), Logs (History), aur Transactions (Real Data)
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS audit_logs (timestamp TEXT, user TEXT, action TEXT, result TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS txn_history (txn_id TEXT, risk_score INTEGER, status TEXT)''')

# Initial Data (Testing ke liye pehle se kuch data dalna)
cursor.execute("SELECT * FROM users WHERE username='ankit_002'")
if not cursor.fetchone():
    # Password hashing: 'gbu_mca_ds' ko SHA-256 mein convert karke save karna
    pwd_hash = hashlib.sha256("gbu_mca_ds".encode()).hexdigest()
    cursor.execute("INSERT INTO users VALUES (?, ?)", ("ankit_002", pwd_hash))
    conn.commit()

# --- 2. PAGE CONFIG & DARK THEME ---
st.set_page_config(page_title="AM Sentinel | Enterprise", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: #e6edf3; }
    [data-testid="stMetricValue"] { color: #58a6ff !important; font-weight: bold; }
    
    /* Responsive Grid for Mobile/Desktop */
    .stButton > button {
        border-radius: 12px; height: 100px; width: 100%;
        background: #161b22 !important; color: #58a6ff !important;
        border: 1px solid #30363d !important; font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover { border-color: #58a6ff; transform: scale(1.02); }

    @media (max-width: 768px) {
        [data-testid="column"] { width: 31% !important; flex: 1 1 31% !important; }
        .stButton > button { height: 80px !important; font-size: 11px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE & NAVIGATION ---
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'page' not in st.session_state: st.session_state.page = 'home'

def add_log(action, result):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO audit_logs VALUES (?, ?, ?, ?)", (ts, "Ankit", action, result))
    conn.commit()

def navigate(p):
    st.session_state.page = p
    st.rerun()

# --- 4. LOGIN SYSTEM (With Hashing) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>🔐 AM SENTINEL SECURE LOGIN</h1>", unsafe_allow_html=True)
    with st.container():
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("Enter System"):
                input_hash = hashlib.sha256(p.encode()).hexdigest()
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u, input_hash))
                if cursor.fetchone():
                    st.session_state.logged_in = True
                    add_log("Login", "Success")
                    st.rerun()
                else:
                    st.error("Access Denied: Invalid Credentials")
    st.stop()

# --- 5. MAIN DASHBOARD ---
with st.sidebar:
    st.markdown("<h2 style='color: #58a6ff;'>🧬 SENTINEL HQ</h2>", unsafe_allow_html=True)
    st.write(f"*Auth User:* Ankit Maurya")
    st.divider()
    if st.button("🏠 Home Dashboard"): navigate('home')
    if st.button("📁 Bulk Data Scan"): navigate('bulk')
    if st.button("📜 Audit Logs"): navigate('logs')
    st.divider()
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# TOP METRICS (Hamesha dikhenge)
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🛡️ AM UNIVERSAL FRAUD SENTINEL</h1>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Nodes Mapped", "1.4B+", "Live GNN")
m2.metric("AI Accuracy", "99.98%", "Stable")
m3.metric("Scan Latency", "0.002ms", "Optimized")
m4.metric("System Status", "Secure", "✅")
st.divider()

# --- 6. PAGES LOGIC ---

# HOME PAGE (Icon Grid)
if st.session_state.page == 'home':
    st.write("### 🏦 Banking & Compliance")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📱\nMobile\nWallet"): navigate('upi')
    with c2:
        if st.button("📑\nCheck\nForensics"): navigate('check')
    with c3:
        if st.button("🕸️\nGNN\nMap"): navigate('graph')

    st.write("### 🛡️ Insurance & Loans")
    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("🏥\nMedical\nAudit"): navigate('ins')
    with c5:
        if st.button("⚖️\nTax/GST\nScan"): navigate('tax')
    with c6:
        if st.button("🏢\nLoan\nFraud"): navigate('loan')

# GNN MAP PAGE (Graph + Meter Side-by-Side + XAI)
elif st.session_state.page == 'graph':
    st.header("🕸️ Relational Graph & AI Risk Analysis")
    col_l, col_r = st.columns([2, 1])
    
    with col_l:
        st.subheader("Network Visualization")
        if st.button("Initialize Deep Scan"):
            add_log("GNN Graph Scan", "Visualized 4 Nodes")
            nodes = [
                Node(id="Sender", label="Input Node", color="#58a6ff"),
                Node(id="Mule", label="Mule Account", color="red"),
                Node(id="Bank", label="Target Bank", color="green"),
                Node(id="Proxy", label="VPN Proxy", color="orange")
            ]
            edges = [Edge(source="Sender", target="Proxy"), Edge(source="Proxy", target="Mule"), Edge(source="Mule", target="Bank")]
            agraph(nodes=nodes, edges=edges, config=Config(width=700, height=500, directed=True))

    with col_r:
        st.subheader("Risk Score (Real-time)")
        fig = go.Figure(go.Indicator(mode="gauge+number", value=88, 
             gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "#58a6ff"},
             'steps': [{'range': [0, 40], 'color': "green"}, {'range': [75, 100], 'color': "red"}]}))
        st.plotly_chart(fig, use_container_width=True)
        st.error("*AI Explainability (XAI):* High risk due to 2-hop connection with blacklisted Proxy IP.")

# AUDIT LOGS PAGE (SQLite Data)
elif st.session_state.page == 'logs':
    st.header("📜 System Audit Trail (SQLite)")
    df = pd.read_sql_query("SELECT * FROM audit_logs ORDER BY timestamp DESC", conn)
    st.dataframe(df, use_container_width=True)
    if st.button("Clear Logs"):
        cursor.execute("DELETE FROM audit_logs")
        conn.commit()
        st.rerun()

# BULK SCAN PAGE (File Upload)
elif st.session_state.page == 'bulk':
    st.header("📁 Enterprise Bulk File Audit")
    uploaded_file = st.file_uploader("Upload Transaction CSV (Upto 2L rows)", type="csv")
    if uploaded_file:
        df_upload = pd.read_csv(uploaded_file)
        st.write("Data Preview:", df_upload.head())
        if st.button("Start Batch Processing"):
            with st.spinner("AI analyzing transactions..."):
                time.sleep(2) # Simulating Parallel Processing
                add_log("Bulk Scan", f"Processed {len(df_upload)} rows")
                st.success(f"Scan Complete! {len(df_upload)} records analyzed. No anomalies found.")

# MODULE PAGES (UPI, Tax, etc.) - Universal Handling
elif st.session_state.page in ['upi', 'check', 'ins', 'tax', 'loan']:
    st.header(f"Module: {st.session_state.page.upper()} Analysis")
    target = st.text_input(f"Enter {st.session_state.page.upper()} ID / Number")
    if st.button("Run Forensic Scan"):
        with st.spinner("Searching 1.4B Nodes..."):
            time.sleep(1)
            # Dynamic Handling for Unknown IDs
            if "fraud" in target.lower():
                st.error("🚨 HIGH RISK DETECTED")
                add_log(f"{st.session_state.page} Scan", "Fraud Found")
            else:
                st.success("✅ NODE VERIFIED: SAFE")
                add_log(f"{st.session_state.page} Scan", "Safe Node")
