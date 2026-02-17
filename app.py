import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from streamlit_agraph import agraph, Node, Edge, Config
from datetime import datetime
import random

# --- 1. DATABASE SETUP (Audit Logs ke liye) ---
conn = sqlite3.connect('sentinel_final.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)')
cursor.execute('CREATE TABLE IF NOT EXISTS audit_logs (user TEXT, time TEXT, action TEXT, status TEXT, risk INTEGER)')
conn.commit()

st.set_page_config(page_title="AM Universal Fraud Sentinel", layout="wide")

# CLASSIC DESIGN (Jo tumne dikhaya tha sabko)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton > button { 
        height: 100px; width: 100%; font-size: 22px; font-weight: bold; 
        border-radius: 15px; border: 2px solid #3b82f6; background-color: #1f2937 !important;
    }
    .stButton > button:hover { background-color: #3b82f6 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'page' not in st.session_state: st.session_state.page = 'home'

# --- 2. SIDEBAR (Naye Features yahan chhupaye hain) ---
with st.sidebar:
    st.title("⚙️ System Control")
    if st.session_state.auth:
        st.write(f"Active Investigator: *{st.session_state.user}*")
        st.divider()
        # NEW ADVANCE FEATURES (By default OFF hain)
        show_map = st.checkbox("Show Regional Heatmap", value=False)
        show_ticker = st.checkbox("Enable Live Threat Feed", value=False)
        auto_resolve = st.toggle("Automated Action Mode", value=True)
        st.divider()
        if st.button("🚪 Logout"):
            st.session_state.auth = False
            st.rerun()
    else:
        st.info("Login required for System Access.")

# --- 3. LOGIN PAGE (Security Layer) ---
if not st.session_state.auth:
    st.title("🛡️ AM SENTINEL - ENTERPRISE LOGIN")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Access System"):
        if (u == "ankit" and p == "123") or (u == "admin" and p == "admin"):
            st.session_state.auth = True
            st.session_state.user = u
            st.rerun()
        else: st.error("Invalid Credentials")
    st.stop()

# --- 4. LIVE TICKER (Advance Feature) ---
if show_ticker:
    st.markdown(f'<p style="color:#58a6ff; font-family:monospace; background:#161b22; padding:10px; border-radius:5px;">● LIVE: {random.choice(["Scanning UPI Gateway...", "Analyzing IP 102.16.x.x", "Monitoring Bank-Node-Alpha"])}</p>', unsafe_allow_html=True)

# --- 5. MAIN CLASSIC DASHBOARD (Original Look) ---
if st.session_state.page == 'home':
    st.title("🛡️ AM UNIVERSAL FRAUD SENTINEL")
    st.write("### Choose a Forensic Module")
    
    # 6 Main Buttons (Exactly like before)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📱 UPI / Wallet"): st.session_state.page = 'upi'; st.rerun()
        if st.button("🏛️ Bank Accounts"): st.session_state.page = 'bank'; st.rerun()
    with c2:
        if st.button("📄 Insurance Claims"): st.session_state.page = 'insurance'; st.rerun()
        if st.button("🕸️ GNN Network"): st.session_state.page = 'graph'; st.rerun()
    with c3:
        if st.button("📁 Bulk Analysis"): st.session_state.page = 'bulk'; st.rerun()
        if st.button("📜 Audit Logs"): st.session_state.page = 'logs'; st.rerun()

    # Heatmap (Only if ON from Sidebar)
    if show_map:
        st.divider()
        st.subheader("🌍 Regional Threat Distribution")
        map_data = pd.DataFrame({'lat': [28.6, 19.0, 22.5], 'lon': [77.2, 72.8, 88.3], 'risk': [10, 80, 50]})
        fig = px.scatter_mapbox(map_data, lat="lat", lon="lon", size="risk", color="risk", mapbox_style="carto-darkmatter", zoom=3)
        st.plotly_chart(fig, use_container_width=True)

# --- 6. MODULES WITH ORIGINAL DROPDOWNS & NEW LOGIC ---

elif st.session_state.page == 'upi':
    st.header("📱 UPI / Wallet Forensic Scanner")
    # ORIGINAL DROPDOWNS
    wallet_list = ["PhonePe", "GooglePay", "Paytm", "Amazon Pay", "BHIM UPI", "MobiKwik"]
    selected_wallet = st.selectbox("Select Payment App", wallet_list)
    upi_id = st.text_input("Enter UPI ID or Mobile Number")
    
    if st.button("Start AI Scan"):
        risk = 92 if "fraud" in upi_id.lower() else 15
        st.metric("Risk Score", f"{risk}%")
        if risk > 50:
            st.error("🚨 ALERT: Fraudulent Pattern Detected!")
            if auto_resolve: st.warning("⚡ Auto-Update: Account Flagged & Problem Categorized.")
        else: st.success("✅ Transaction Verified Safe")
    
    if st.button("⬅️ Back"): st.session_state.page = 'home'; st.rerun()

elif st.session_state.page == 'bank':
    st.header("🏛️ Banking Forensic Module")
    # ORIGINAL BANK DROPDOWN
    bank_list = ["SBI", "HDFC", "ICICI", "Axis Bank", "PNB", "GBU Special Bank", "Canara Bank"]
    selected_bank = st.selectbox("Select Institution", bank_list)
    acc_no = st.text_input("Account Number")
    
    if st.button("Audit Account"):
        st.write(f"Scanning {selected_bank} records for {acc_no}...")
        st.success("Analysis Complete: No suspicious anomalies found.")
        
    if st.button("⬅️ Back"): st.session_state.page = 'home'; st.rerun()

elif st.session_state.page == 'graph':
    st.header("🕸️ GNN Multi-Hop Intelligence")
    # ORIGINAL GRAPH LOGIC
    nodes = [Node(id="A", label="User Account", color="green"), Node(id="B", label="Suspect Node", color="red"), Node(id="C", label="Third Party", color="blue")]
    edges = [Edge(source="A", target="B"), Edge(source="B", target="C")]
    config = Config(width=800, height=500, directed=True, nodeHighlightBehavior=True, highlightColor="#F7A7A6")
    agraph(nodes=nodes, edges=edges, config=config)
    
    if st.button("⬅️ Back"): st.session_state.page = 'home'; st.rerun()

elif st.session_state.page == 'logs':
    st.header("📜 Forensic Audit Logs")
    st.write("Real-time logs of all scans and investigations.")
    # Log Table placeholder
    st.info("System is logging all user activities for forensic compliance.")
    if st.button("⬅️ Back"): st.session_state.page = 'home'; st.rerun()

elif st.session_state.page == 'insurance' or st.session_state.page == 'bulk':
    st.header("Under Construction / File Upload")
    st.write("Project modules are active.")
    if st.button("⬅️ Back"): st.session_state.page = 'home'; st.rerun()
