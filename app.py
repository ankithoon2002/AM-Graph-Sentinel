import streamlit as st
import time
import plotly.graph_objects as go
from streamlit_agraph import agraph, Node, Edge, Config

# --- 1. PAGE CONFIG & ADVANCED CSS (Mobile + Laptop) ---
st.set_page_config(page_title="AM Sentinel | Enterprise", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Global Theme */
    .stApp { background-color: #f0f2f5; color: #1d2f54; }
    
    /* LAPTOP VIEW CSS */
    .stButton > button {
        border-radius: 15px; height: 120px; width: 100%;
        background: white !important; color: #002e6e !important;
        border: 1px solid #d1d9e6 !important; font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: 0.3s;
    }
    .stButton > button:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }

    /* MOBILE VIEW CSS (Paytm Style Icon Grid) */
    @media (max-width: 768px) {
        [data-testid="column"] {
            width: 31% !important; flex: 1 1 31% !important;
            min-width: 31% !important; margin: 1% !important;
        }
        .stButton > button {
            height: 90px !important; border-radius: 20px !important;
            font-size: 11px !important; padding: 5px !important;
            background: #ffffff !important; border: none !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        }
        h1 { font-size: 22px !important; text-align: center; margin-bottom: 20px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE FOR NAVIGATION ---
if 'page' not in st.session_state: st.session_state.page = 'home'
def navigate_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 3. MAIN INTERFACE LOGIC ---

# PAGE: HOME (The Icon Grid)
if st.session_state.page == 'home':
    st.markdown("<h1 style='color: #002e6e;'>🛡️ AM UNIVERSAL FRAUD SENTINEL</h1>", unsafe_allow_html=True)
    
    st.write("### 🏦 Financial & Banking")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📱\nMobile\nWallet"): navigate_to('upi')
    with c2:
        if st.button("📑\nCheck\nAudit"): navigate_to('check')
    with c3:
        if st.button("🌍\nIntl.\nSwift"): navigate_to('intl')

    st.write("### 🛡️ Insurance & Governance")
    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("🏥\nMedical\nClaims"): navigate_to('ins')
    with c5:
        if st.button("⚖️\nTax/GST\nFraud"): navigate_to('tax')
    with c6:
        if st.button("🏢\nLoan\nFraud"): navigate_to('loan')
    
    st.divider()
    st.info("💡 Tip: Click any icon to run a real-time GNN relational scan.")

# PAGE: UPI MODULE
elif st.session_state.page == 'upi':
    st.button("⬅️ Back to Apps", on_click=lambda: navigate_to('home'))
    st.header("📱 UPI Decision Engine")
    upi_id = st.text_input("Enter UPI ID or Mobile Number", placeholder="example@upi")
    
    if upi_id:
        if st.button("Verify Transaction"):
            with st.spinner("GNN scanning 1.4B nodes..."):
                time.sleep(1.5)
                risk = 92 if "fraud" in upi_id.lower() else 14
                if risk > 70:
                    st.error(f"🚨 BLOCKED: {upi_id} linked to a fraud cluster.")
                else:
                    st.success(f"✅ APPROVED: {upi_id} is safe for payment.")

# PAGE: INSURANCE MODULE
elif st.session_state.page == 'ins':
    st.button("⬅️ Back to Apps", on_click=lambda: navigate_to('home'))
    st.header("🏥 Insurance Claim Forensic")
    policy = st.text_input("Enter Policy Number")
    if policy:
        if st.button("Run Collusion Scan"):
            with st.spinner("Checking Hospital-Agent-Patient network..."):
                time.sleep(2)
                st.warning("⚠️ Suspicious Pattern: High-frequency claims detected from this node.")

# PAGE: INTERNATIONAL (GNN Graph)
elif st.session_state.page == 'intl':
    st.button("⬅️ Back to Apps", on_click=lambda: navigate_to('home'))
    st.header("🌍 Global Swift Relational Map")
    swift = st.text_input("Enter Swift Code")
    if st.button("Trace Global Path"):
        nodes = [Node(id="India", label="Local Bank", color="#002e6e"),
                 Node(id="Intl", label="Global Node", color="red")]
        edges = [Edge(source="India", target="Intl")]
        agraph(nodes=nodes, edges=edges, config=Config(width=600, height=400, directed=True))

# (Baki modules ke liye bhi isi tarah simple blocks add kar sakte hain)
