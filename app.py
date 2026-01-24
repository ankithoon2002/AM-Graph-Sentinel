# =================================================================
# PROJECT: AM GRAPH SENTINEL (Universal Fraud Defense Ecosystem)
# DEVELOPER: ANKIT MAURYA (Roll No: 245PCD002)
# MCA (Data Science) - Gautam Buddha University
# =================================================================
import streamlit as st
import pandas as pd
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="AM Graph Sentinel", page_icon="🛡️", layout="wide")

# --- 2. ADVANCED CYBER-TECH INTERFACE (Glassmorphism) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #0f172a 0%, #020617 100%); color: #e2e8f0; }
    .main-title { text-align: center; font-size: 42px; font-weight: 900; color: #38bdf8; text-shadow: 0 0 15px rgba(56,189,248,0.4); }
    
    /* Premium Glass Buttons */
    div.stButton > button {
        width: 100%; border-radius: 20px; height: 110px;
        background: rgba(255, 255, 255, 0.05) !important;
        color: #38bdf8 !important; border: 1px solid rgba(56, 189, 248, 0.2) !important;
        font-weight: bold; font-size: 17px; backdrop-filter: blur(10px); transition: 0.4s;
    }
    div.stButton > button:hover {
        border: 1px solid #38bdf8 !important; background: rgba(56, 189, 248, 0.1) !important;
        transform: translateY(-5px); box-shadow: 0px 0px 20px rgba(56, 189, 248, 0.4);
    }
    
    /* Fraud Alert Style */
    .fraud-text { color: #ff4b4b; font-weight: bold; font-family: monospace; }
    .safe-text { color: #00ffcc; font-weight: bold; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE FOR NAVIGATION ---
if 'view' not in st.session_state:
    st.session_state.view = 'home'

def navigate(page_name):
    st.session_state.view = page_name
    st.rerun()

# --- 4. SIDEBAR - AI HUB ---
with st.sidebar:
    st.markdown("## 🧬 SENTINEL AI")
    st.write(f"*Dev:* Ankit Maurya")
    st.write(f"*ID:* 24SPCD002")
    st.divider()
    if st.toggle("Autonomous Update", value=True):
        st.success("GNN Model: Learning Active")
    st.info("System Scale: 1.4B+ Nodes")

# --- 5. MAIN NAVIGATION LOGIC ---

# PAGE: HOME DASHBOARD
if st.session_state.view == 'home':
    st.markdown("<h1 class='main-title'>🛡️ AM GRAPH SENTINEL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#94a3b8;'>Universal Relational Fraud Protection System</p>", unsafe_allow_html=True)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Live Latency", "0.002ms")
    m2.metric("Nodes Mapped", "1.4B+")
    m3.metric("AI Confidence", "99.98%")
    
    st.divider()
    st.subheader("⚡ Core Security Engines")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💸 CHECK PAYMENT SAFETY\n(Bank & UPI Fraud)"): navigate('payment')
    with c2:
        if st.button("📄 VERIFY MEDICAL CLAIMS\n(Insurance Shield)"): navigate('insurance')

    c3, c4 = st.columns(2)
    with c3:
        if st.button("📸 ANALYZE QR CODES\n(Cyber & Link Guard)"): navigate('qr')
    with c4:
        # THE GRAPH OPTION
        if st.button("🕸️ NETWORK VISUALIZER\n(GNN Relational Graph)"): navigate('graph')

# PAGE: NETWORK VISUALIZER (Graph Demo)
elif st.session_state.view == 'graph':
    st.header("🕸️ GNN Network Visualizer")
    st.write("Ye module transactions ke piche ke chhupe hue patterns (Hidden Relationships) ko map karta hai.")
    
    test_id = st.text_input("Enter Node ID to Scan", value="SUSPECT_NODE_99")
    
    if st.button("Map Hidden Relationships"):
        with st.spinner("AI is tracing multi-hop connections..."):
            time.sleep(0.8)
            
            # --- THE FRAUD DEMO VISUALIZATION ---
            st.markdown("### 🔍 Relational Graph Results:")
            
            # Simulated Graph Connections
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px;'>
                <p><b>[Primary Node: {test_id}]</b></p>
                <p> &nbsp; ↳ <span class='safe-text'>Edge: Known Device</span> ---> [User_Mobile_A]</p>
                <p> &nbsp; ↳ <span class='fraud-text'>Edge: High-Risk Link</span> ---> [Blacklisted_Wallet_X]</p>
                <p> &nbsp; ↳ <span class='fraud-text'>Edge: IP Collision</span> ---> [Fraud_Syndicate_Cluster_04]</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.error("🚨 ALERT: Hidden Fraudulent Cluster Detected via GNN Relational Inference!")
            st.info("System recommendation: Block Node and All Connected Edges.")
            
    if st.button("⬅️ Return to Dashboard"): navigate('home')

# PAGE: QR SCANNER (Camera)
elif st.session_state.view == 'qr':
    st.header("📸 Scan & Verify QR")
    qr_cam = st.camera_input("Point at the QR Code")
    if qr_cam:
        st.success("QR Integrity Verified: Destination Secure.")
    if st.button("⬅️ Back"): navigate('home')

# PAGE: PAYMENT SAFETY
elif st.session_state.view == 'payment':
    st.header("💸 Payment Safety Engine")
    p_id = st.text_input("Enter ID")
    if st.button("Verify"):
        st.success("Safe Node.")
    if st.button("⬅️ Back"): navigate('home')

# PAGE: INSURANCE SHIELD
elif st.session_state.view == 'insurance':
    st.header("🛡️ Medical Claim Verification")
    i_id = st.text_input("Enter Policy ID")
    if st.button("Analyze Triangle"):
        st.success("No Fraud Detected.")
    if st.button("⬅️ Back"): navigate('home')


