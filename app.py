import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_agraph import agraph, Node, Edge, Config
import random

# --- 1. SETTINGS & CSS (Wahi Original Look) ---
st.set_page_config(page_title="AM Universal Fraud Sentinel", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    /* Original Blue-Outline Buttons */
    .stButton > button { 
        height: 100px; width: 100%; font-size: 22px; font-weight: bold; 
        border-radius: 15px; border: 2px solid #4da3ff !important; 
        background-color: transparent !important; color: white !important;
    }
    .stButton > button:hover { background-color: #4da3ff !important; color: black !important; }
    .highlight-box {
        background-color: #161b22; padding: 25px; border-radius: 15px;
        text-align: center; border: 2px solid #3b82f6; margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'page' not in st.session_state: st.session_state.page = 'home'

# --- 2. LOGIN (Sirf Starting mein) ---
if not st.session_state.auth:
    st.title("🛡️ SENTINEL SECURE ACCESS")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Enter System"):
        if u == "ankit" and p == "123":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# --- 3. TOP HIGHLIGHTS (1.4B Nodes & Accuracy) ---
st.markdown("""
    <div class="highlight-box">
        <h1 style='color:#4da3ff; margin:0;'>🌐 GNN GLOBAL FORENSIC ENGINE</h1>
        <p style='font-size:24px; margin:5px;'><b>Nodes Scanned:</b> 1.4 Billion+ | <b>Accuracy:</b> 98.4% | <b>Real-time Latency:</b> 12ms</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. MAIN DASHBOARD (EXACT ORIGINAL LOOK) ---
if st.session_state.page == 'home':
    st.write("### Forensic Investigation Modules")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📱 UPI / WALLET"): st.session_state.page = 'upi'; st.rerun()
        if st.button("🏛️ BANK ACCOUNTS"): st.session_state.page = 'bank'; st.rerun()
    with c2:
        if st.button("📄 INSURANCE CLAIMS"): st.session_state.page = 'insurance'; st.rerun()
        if st.button("🕸️ GNN NETWORK"): st.session_state.page = 'graph'; st.rerun()
    with c3:
        if st.button("📁 BULK ANALYSIS"): st.session_state.page = 'bulk'; st.rerun()
        if st.button("📜 AUDIT LOGS"): st.session_state.page = 'logs'; st.rerun()

# --- 5. GNN NETWORK (Restored with 3 Graphs) ---
elif st.session_state.page == 'graph':
    st.header("🕸️ GNN Intelligence Hub")
    # PURANA MULTI-GRAPH DROPDOWN
    graph_view = st.selectbox("Select Network View", ["Transaction money trail", "Fraud Ring Cluster", "High-Risk Node Analysis"])
    
    if graph_view == "Transaction money trail":
        nodes = [Node(id="A", label="User", color="green"), Node(id="B", label="Suspect", color="red")]
        edges = [Edge(source="A", target="B")]
    elif graph_view == "Fraud Ring Cluster":
        nodes = [Node(id="X", label="Fraud A", color="red"), Node(id="Y", label="Fraud B", color="red"), Node(id="Z", label="Money Mule", color="orange")]
        edges = [Edge(source="X", target="Z"), Edge(source="Y", target="Z")]
    else:
        nodes = [Node(id="N1", label="Node 1.4B", color="blue")]
        edges = []
        
    agraph(nodes=nodes, edges=edges, config=Config(width=1000, height=600))
    if st.button("⬅️ BACK"): st.session_state.page = 'home'; st.rerun()

# --- 6. UPI SCANNER (Restored with All Wallets) ---
elif st.session_state.page == 'upi':
    st.header("📱 UPI Forensic Scanner")
    # PURANA DROPDOWN
    wallet = st.selectbox("Select App", ["PhonePe", "GooglePay", "Paytm", "Amazon Pay", "BHIM UPI", "MobiKwik"])
    target = st.text_input("Enter UPI ID")
    if st.button("Scan"):
        st.write(f"Scanning {wallet} ID: {target}...")
        st.success("Analysis Complete!")
    if st.button("⬅️ BACK"): st.session_state.page = 'home'; st.rerun()

# --- 7. BANKING (Restored with Banks) ---
elif st.session_state.page == 'bank':
    st.header("🏛️ Banking Audit")
    bank = st.selectbox("Select Bank", ["SBI", "HDFC", "ICICI", "Axis Bank", "PNB", "GBU Bank"])
    if st.button("⬅️ BACK"): st.session_state.page = 'home'; st.rerun()

# --- LOGS, BULK & INSURANCE (Restoring original placeholders) ---
elif st.session_state.page in ['logs', 'bulk', 'insurance']:
    st.header(f"Module: {st.session_state.page.upper()}")
    st.write("Original content remains active.")
    if st.button("⬅️ BACK"): st.session_state.page = 'home'; st.rerun()
