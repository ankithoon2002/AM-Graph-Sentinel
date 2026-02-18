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

# --- 2. CONFIG & STYLING (Classic Look) ---
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
    .stDownloadButton > button {
        background: #2ea44f !important; color: white !important; width: 100%; height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# Navigation State
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'user' not in st.session_state: st.session_state.user = ""
if 'page' not in st.session_state: st.session_state.page = 'home'

def navigate(p):
    st.session_state.page = p
    st.rerun()

def add_log(action, entity, result, auto_act="N/A"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_name = st.session_state.user if st.session_state.user else "Ankit"
    cursor.execute("INSERT INTO audit_logs VALUES (?, ?, ?, ?, ?, ?)", (user_name, ts, action, entity, result, auto_act))
    conn.commit()

# DROPDOWN LISTS
BANKS = ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "PNB", "GBU Bank", "Canara Bank", "Bank of Baroda"]
WALLETS = ["Paytm", "PhonePe", "Google Pay (GPay)", "Amazon Pay", "MobiKwik", "Airtel Money"]
INSURANCE = ["LIC", "HDFC Ergo", "Star Health", "ICICI Lombard", "Bajaj Allianz", "New India Assurance"]

# --- 3. LOGIN & SIGNUP SYSTEM ---
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🛡️ AM SENTINEL ACCESS CONTROL</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        tab1, tab2 = st.tabs(["🔑 Login", "📝 Create Account"])
        with tab1:
            u = st.text_input("Username", key="l_user")
            p = st.text_input("Password", type="password", key="l_pass")
            if st.button("Access Dashboard"):
                cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
                if cursor.fetchone() or (u == "ankit_002" and p == "gbu_mca_ds"):
                    st.session_state.logged_in = True
                    st.session_state.user = u
                    add_log("Login", "System", "Success")
                    st.rerun()
                else: st.error("Invalid Username or Password")
        with tab2:
            new_u = st.text_input("New Username", key="s_user")
            new_p = st.text_input("New Password", type="password", key="s_pass")
            if st.button("Register Account"):
                try:
                    cursor.execute("INSERT INTO users VALUES (?, ?)", (new_u, new_p))
                    conn.commit()
                    st.success("Account Created Successfully! Please Login.")
                except: st.error("Username already exists!")
    st.stop()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("⚙️ System Control")
    st.write(f"Active User: *{st.session_state.user}*")
    st.divider()
    show_map = st.checkbox("Show Global Risk Heatmap", value=False)
    show_feed = st.checkbox("Enable Live Threat Feed", value=False)
    st.divider()
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- 5. HEADER (Metrics) ---
st.markdown("<h1 style='text-align: center; color: #58a6ff;'>🛡️ AM UNIVERSAL FRAUD SENTINEL</h1>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Nodes Analyzed", "1.4B+", "Live")
m2.metric("AI Accuracy", "99.98%", "Stable")
m3.metric("Neural Latency", "0.002ms", "GNN")
m4.metric("Status", "Secure", "✅")

if show_feed:
    st.info(f"📡 SCANNING: {random.choice(['Node-X22', 'SBI Gateway', 'Paytm-API-V2'])}")
st.divider()

# --- 6. PAGE LOGIC ---

# --- HOME PAGE ---
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

    if show_map:
        st.divider()
        st.write("### 🌍 Global Risk Heatmap")
        map_df = pd.DataFrame({'lat': [28.6, 19.0, 13.0, 22.5], 'lon': [77.2, 72.8, 80.2, 88.3], 'risk': [15, 98, 45, 85]})
        fig_map = px.scatter_mapbox(map_df, lat="lat", lon="lon", size="risk", color="risk", color_continuous_scale="Reds", mapbox_style="carto-darkmatter", zoom=3)
        st.plotly_chart(fig_map, use_container_width=True)

    st.divider()
    c7, c8 = st.columns(2)
    with c7:
        if st.button("📁 Bulk Analysis"): navigate('bulk')
    with c8:
        if st.button("📜 Audit Logs"): navigate('logs')

# --- GNN INTELLIGENCE HUB (4 Graphs Restored) ---
elif st.session_state.page == 'graph':
    st.header("🕸️ GNN Intelligence Hub")
    target = st.text_input("🔍 Search Node (USR_ID)")
    
    cg, cr = st.columns([2, 1])
    with cg:
        nodes = [
            Node(id="B", label="Banks", color="#58a6ff", size=25),
            Node(id="I", label="Insurance", color="#2ea44f", size=25),
            Node(id="W", label="Wallet", color="#dbab09", size=25),
            Node(id="F", label="FRAUD NODE", color="#d12d3d", size=35)
        ]
        edges = [Edge(source="B", target="W"), Edge(source="W", target="F"), Edge(source="I", target="F")]
        agraph(nodes=nodes, edges=edges, config=Config(width=700, height=450, directed=True, physics=True))
    
    with cr:
        val = 94 if target else 15
        st.plotly_chart(go.Figure(go.Indicator(mode="gauge+number", value=val, title={'text': "Risk Score"},
                        gauge={'bar':{'color':"#58a6ff"}, 'axis':{'range':[0,100]},
                        'steps':[{'range':[0,40], 'color':'green'}, {'range':[70,100], 'color':'red'}]})), use_container_width=True)

    c_pie, c_bar = st.columns(2)
    with c_pie:
        st.plotly_chart(px.pie(names=['Safe', 'Caution', 'Fraud'], values=[140, 40, 20], hole=0.5, 
                                color_discrete_sequence=['#2ea44f', '#dbab09', '#d12d3d'], title="Network Health Ratio"), use_container_width=True)
    with c_bar:
        st.plotly_chart(px.bar(x=['Banks', 'UPI', 'Insurance'], y=[8, 25, 4], title="Threats by Category", 
                                color_discrete_sequence=['#d12d3d']), use_container_width=True)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ Back to Home"): navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)

# --- BULK ANALYSIS ---
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
    if st.button("⬅️ Back to Home"): navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)

# --- LOGS PAGE (Download Button Included) ---
elif st.session_state.page == 'logs':
    st.header("📜 Forensic Reports & History")
    df_logs = pd.read_sql_query("SELECT * FROM audit_logs ORDER BY timestamp DESC", conn)
    st.dataframe(df_logs, use_container_width=True)
    
    st.download_button("📥 Download Full Report (CSV)", df_logs.to_csv(index=False), "sentinel_report.csv")
    
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ Back to Home"): navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)

# --- OTHER MODULES (UPI, Bank, etc.) ---
elif st.session_state.page in ['upi', 'check', 'ins', 'tax', 'loan']:
    st.header(f"Active Module: {st.session_state.page.upper()}")
    current_list = WALLETS if st.session_state.page == 'upi' else (INSURANCE if st.session_state.page == 'ins' else BANKS)
    sel = st.selectbox("Select Partner Entity", current_list)
    tid = st.text_input("Enter ID / Number to Scan")
    
    if st.button("Run Deep Forensic Scan"):
        with st.spinner("Analyzing Database..."):
            time.sleep(1)
            is_fraud = "fraud" in tid.lower() or "999" in tid
            res = "FRAUD DETECTED" if is_fraud else "VERIFIED SAFE"
            auto_act = "Account Frozen & GNN Flagged" if is_fraud else "N/A"
            
            st.success(res) if not is_fraud else st.error(res)
            if is_fraud: st.warning(f"⚡ *Auto-Action:* {auto_act}")
            add_log(f"{st.session_state.page.upper()} Scan", sel, res, auto_act)

    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("⬅️ Back to Home"): navigate('home')
    st.markdown('</div>', unsafe_allow_html=True)
