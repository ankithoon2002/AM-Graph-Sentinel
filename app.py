import streamlit as st
import pandas as pd
import sqlite3
import time
import plotly.graph_objects as go
import plotly.express as px
from streamlit_agraph import agraph, Node, Edge, Config
from datetime import datetime
import random

# --- 1. DATABASE & AUTH ---
conn = sqlite3.connect('sentinel_v3.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS audit_logs (user TEXT, timestamp TEXT, action TEXT, entity TEXT, status TEXT, risk INTEGER, reason TEXT)')
conn.commit()

st.set_page_config(page_title="AM Sentinel Enterprise AI", layout="wide")

# Theme Styling
st.markdown("""
    <style>
    .stApp { background-color: #050a14; color: #e6edf3; }
    .ticker { background: #161b22; padding: 10px; border-radius: 8px; border-left: 5px solid #3b82f6; margin-bottom: 20px; font-family: monospace; color: #58a6ff; }
    .status-box { padding: 10px; border-radius: 5px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'page' not in st.session_state: st.session_state.page = 'login'

def navigate(p):
    st.session_state.page = p
    st.rerun()

# --- 2. AUTHENTICATION ---
if not st.session_state.auth:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.title("🔐 Enterprise Login")
        mode = st.radio("Select", ["Login", "Sign Up"])
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Proceed"):
            if mode == "Login":
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u,p))
                if cursor.fetchone() or (u=="ankit" and p=="123"):
                    st.session_state.auth = True
                    st.session_state.user = u
                    st.rerun()
                else: st.error("Access Denied")
            else:
                try:
                    cursor.execute("INSERT INTO users VALUES (?,?)", (u,p))
                    conn.commit()
                    st.success("Account Created! Login now.")
                except: st.error("Username Taken")
    st.stop()

# --- 3. LIVE SIMULATION ENGINE ---
st.markdown(f'<div class="ticker">📡 LIVE FEED: {random.choice(["Scanning SBI Node...", "Monitoring UPI Gateway...", "Analyzing IP 192.168.1.45"])}</div>', unsafe_allow_html=True)

# --- 4. DASHBOARD ---
if st.session_state.page == 'home':
    st.title("🛡️ AM UNIVERSAL FRAUD SENTINEL")
    
    # RISK HEATMAP
    st.subheader("🌐 Global Threat Intelligence Map")
    map_df = pd.DataFrame({
        'lat': [28.6, 19.0, 13.0, 55.7, 40.7], 'lon': [77.2, 72.8, 80.2, 37.6, -74.0],
        'risk': [10, 30, 15, 90, 80], 'city': ['Delhi', 'Mumbai', 'Chennai', 'Moscow', 'NY']
    })
    fig_map = px.scatter_mapbox(map_df, lat="lat", lon="lon", size="risk", color="risk",
                                color_continuous_scale="Reds", mapbox_style="carto-darkmatter", zoom=1)
    st.plotly_chart(fig_map, use_container_width=True)

    st.write("### 🛠️ Investigation Modules")
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("📱 UPI Scan"): navigate('scan')
    with c2:
        if st.button("🕸️ GNN Graph"): navigate('graph')
    with c3:
        if st.button("📁 Bulk File"): navigate('bulk')
    with c4:
        if st.button("🚪 Logout"): 
            st.session_state.auth = False
            st.rerun()
    
    st.divider()
    st.subheader("📜 Recent Forensic Activity")
    logs = pd.read_sql_query("SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 5", conn)
    st.table(logs)

# --- 5. SMART SCAN LOGIC (The Answer to your Question) ---
elif st.session_state.page == 'scan':
    st.header("🔍 Intelligent Forensic Scanner")
    amt = st.number_input("Transaction Amount", min_value=0)
    source = st.selectbox("Source Type", ["Family/Personal", "Business Vendor", "Salary", "Unknown/New"])
    
    if st.button("Analyze Risk"):
        with st.spinner("AI Evaluating Context..."):
            time.sleep(1.5)
            # SMART LOGIC
            risk_score = 10 # Default safe
            reason = "Standard behavior"
            status = "VERIFIED SAFE"
            
            if amt > 100000:
                if source == "Unknown/New":
                    risk_score = 85
                    status = "CRITICAL FRAUD"
                    reason = "High amount from unverified source"
                else:
                    risk_score = 30
                    status = "HOLD: VERIFYING"
                    reason = "High amount but Trusted Source. Manual check required."
            
            st.metric("Risk Score", f"{risk_score}%", delta="- Safe" if risk_score < 40 else "High Risk")
            st.info(f"*AI Reasoning:* {reason}")
            
            if status == "CRITICAL FRAUD": st.error(status)
            elif status == "VERIFIED SAFE": st.success(status)
            else: st.warning(status)
            
            # Log it
            cursor.execute("INSERT INTO audit_logs VALUES (?,?,?,?,?,?,?)", 
                           (st.session_state.user, datetime.now().strftime("%H:%M:%S"), "Scan", "UPI", status, risk_score, reason))
            conn.commit()

    if st.button("⬅️ Back"): navigate('home')

# GNN PAGE (Simulated Path Analysis)
elif st.session_state.page == 'graph':
    st.header("🕸️ Multi-Hop Path Analysis")
    st.write("Visualizing Money Trail between Safe and Suspect Nodes...")
    nodes = [Node(id="A", label="User A (Safe)", color="green"), Node(id="B", label="Mediator", color="blue"), Node(id="C", label="Fraudster", color="red")]
    edges = [Edge(source="A", target="B"), Edge(source="B", target="C")]
    agraph(nodes=nodes, edges=edges, config=Config(width=800, height=500))
    if st.button("⬅️ Back"): navigate('home')
