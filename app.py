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
cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
cursor.execute('''CREATE TABLE IF NOT EXISTS audit_logs 
               (user TEXT, timestamp TEXT, action TEXT, entity TEXT, result TEXT, auto_action TEXT)''')
conn.commit()

# --- 2. CONFIG & STYLING (Wahi Original Look Jo Tumhe Chahiye) ---
st.set_page_config(page_title="AM Sentinel Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b1120; color: #e6edf3; }
    [data-testid="stMetricValue"] { color: #58a6ff !important; font-weight: bold; }
    /* Original Blue Buttons Style */
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

# Navigation & Session State
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user' not in st.session_state: st.session_state.user = ""
if 'page' not in st.session_state: st.session_state.page = 'home'

def navigate(p):
    st.session_state.page = p
    st.rerun()

# --- 3. LOGIN & SIGNUP (New Feature - Clean Look) ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🛡️ AM SENTINEL SECURE ACCESS</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Create Account"])
        with tab1:
            u = st.text_input("Username", key="login_u")
            p = st.text_input("Password", type="password", key="login_p")
            if st.button("Enter Dashboard"):
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
                if cursor.fetchone() or (u == "ankit_002" and p == "gbu_mca_ds"):
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Invalid Credentials")
        with tab2:
            nu = st.text_input("New Username")
            np = st.text_input("New Password", type="password")
            if st.button("Register Now"):
                try:
                    cursor.execute("INSERT INTO users VALUES (?, ?)", (nu, np))
                    conn.commit()
                    st.success("Account Created! Now Login.")
                except: st.error("Username already taken!")
    st.stop()

# --- 4. SIDEBAR (Advance Settings) ---
with st.sidebar:
    st.title("⚙️ System Control")
    st.write(f"Investigator: *{st.session_state.user}*")
    st.divider()
    show_map = st.checkbox("Show Global Heatmap", value=False)
    show_feed = st.checkbox("Live Threat Feed", value=False)
    st.divider()
    st.write("🛰️ *System Status:* Online")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- 5. HEADER (Metrics - Wahi 1.4B Nodes Wala) ---
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🛡️ AM UNIVERSAL FRAUD SENTINEL</h1>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Nodes Analyzed", "1.4B+", "Live")
m2.metric("AI Accuracy", "99.98%", "Stable")
m3.metric("Neural Latency", "0.002ms", "GNN")
m4.metric("Status", "Secure", "✅")

if show_feed:
    st.info(f"📡 SCANNING: {random.choice(['Node-X22', 'SBI Gateway', 'Paytm-API', 'HDFC Server'])}")
st.divider()

# --- 6. PAGE LOGIC (Main Dashboard - No Look Change) ---

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

    # New Map Feature (Only if ON from Sidebar)
    if show_map:
        st.divider()
        st.write("### 🌍 Global Risk Heatmap")
        map_df = pd.DataFrame({'lat': [28.6, 19.0, 13.0, 22.5], 'lon': [77.2, 72.8, 80.2, 88.3], 'risk': [20, 95, 40, 70]})
        fig_map = px.scatter_mapbox(map_df, lat="lat", lon="lon", size="risk", color="risk", color_continuous_scale="Reds", mapbox_style="carto-darkmatter", zoom=3)
        st.plotly_chart(fig_map, use_container_width=True)

    st.divider()
    c7, c8 = st.columns(2)
    with c7:
        if st.button("📁 Bulk Analysis"): navigate('bulk')
    with c8:
        if st.button("📜 Audit Logs"): navigate('logs')

# GNN PAGE (Restored original code)
elif st.session_state.page == 'graph':
    st.header("🕸️ GNN Intelligence Hub")
    target = st.text_input("🔍 Search Node (USR_ID)")
    cg, cr = st.columns([2, 1])
    with cg:
        nodes = [Node(id="B", label="Banks", color="#58a6ff", size=25), Node(id="I", label="Insurance", color="#2ea44f", size=25), Node(id="W", label="Wallet", color="#dbab09", size=25), Node(id="F", label="FRAUD", color="#d12d3d", size=35)]
        edges = [Edge(source="B", target="W"), Edge(source="W", target="F"), Edge(source="I", target="F")]
        agraph(nodes=nodes, edges=edges, config=Config(width=700, height=450, directed=True, physics=True))
    with cr:
        val = 94 if target else 15
        st.plotly_chart(go.Figure(go.Indicator(mode="gauge+number", value=val, gauge={'bar':{'color':"#58a6ff"}, 'axis':{'range':[0,100]}})), use_container_width=True)
    if st.button("⬅️ Back"): navigate('home')

# UPI / BANK MODULES (Restored Dropdowns)
elif st.session_state.page in ['upi', 'check', 'ins', 'tax', 'loan']:
    st.header(f"Module: {st.session_state.page.upper()}")
    WALLETS = ["Paytm", "PhonePe", "GPay", "Amazon Pay", "MobiKwik"]
    BANKS = ["SBI", "HDFC", "ICICI", "Axis", "PNB", "GBU Bank"]
    
    current_list = WALLETS if st.session_state.page == 'upi' else BANKS
    sel = st.selectbox("Select Entity", current_list)
    tid = st.text_input("Enter ID to Scan")
    
    if st.button("Run Forensic Scan"):
        is_fraud = "999" in tid or "fraud" in tid.lower()
        if is_fraud:
            st.error("FRAUD DETECTED")
            st.warning("⚡ Auto-Action: Account Frozen & Reported to GNN Node.")
        else: st.success("VERIFIED SAFE")
    if st.button("⬅️ Back"): navigate('home')

# LOGS PAGE
elif st.session_state.page == 'logs':
    st.header("📜 Forensic Audit Logs")
    df_logs = pd.read_sql_query("SELECT * FROM audit_logs", conn)
    st.dataframe(df_logs, use_container_width=True)
    st.download_button("📥 Download Full Report (CSV)", df_logs.to_csv(index=False), "sentinel_report.csv")
    if st.button("⬅️ Back"): navigate('home')
    if show_map:
    st.divider()
    st.write("### 🌍 Global Risk Heatmap")
    map_df = pd.DataFrame({'lat': [28.6, 19.0, 13.0], 'lon': [77.2, 72.8, 80.2], 'risk': [20, 95, 40]})
    fig_map = px.scatter_mapbox(map_df, lat="lat", lon="lon", size="risk", color="risk", mapbox_style="carto-darkmatter", zoom=3)
    st.plotly_chart(fig_map, use_container_width=True)



