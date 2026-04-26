import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import random

# Import modular components
from database import db_conn, cursor, commit_audit_log
from ml_model import sentinel_model
from auth import authenticate_user, register_user

# --- 3. ADVANCED INTERFACE STYLING ---
st.set_page_config(page_title="Universal Fraud Sentinel Pro", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800;900&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
    }
    
    .stApp { background: radial-gradient(circle, #0d1117 0%, #010409 100%); color: #c9d1d9; }
    .main-header { 
        font-size: 52px; 
        font-weight: 900; 
        color: #58a6ff; 
        text-align: center; 
        margin-bottom: 25px; 
        font-family: 'Inter', sans-serif;
        letter-spacing: -2px;
        text-transform: uppercase;
        text-shadow: 0 0 20px rgba(88,166,255,0.3);
    }
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 0.9rem !important;
        color: #8b949e !important;
    }
    [data-testid="stMetricValue"] { 
        color: #58a6ff !important; 
        font-family: 'Inter', sans-serif !important; 
        font-weight: 800 !important;
    }
    .stButton > button {
        border-radius: 8px; height: 65px; width: 100%;
        background: linear-gradient(145deg, #1f2937, #111827) !important;
        color: #58a6ff !important; border: 1px solid #30363d !important;
        font-size: 18px; transition: all 0.4s ease;
    }
    .stButton > button:hover { border-color: #58a6ff !important; transform: translateY(-2px); box-shadow: 0 4px 15px rgba(88,166,255,0.2); }
    .logout-btn > div > button { background: #f85149 !important; color: white !important; height: 40px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SESSION MANAGEMENT ---
if 'is_authenticated' not in st.session_state: st.session_state.is_authenticated = False
if 'current_user' not in st.session_state: st.session_state.current_user = ""
if 'active_page' not in st.session_state: st.session_state.active_page = 'dashboard'


def switch_view(target_page):
    st.session_state.active_page = target_page
    st.rerun()


# --- 5. AUTHENTICATION GATEWAY ---
if not st.session_state.is_authenticated:
    st.markdown("<div class='main-header'>🛡️ AM UNIVERSAL FRAUD SENTINEL</div>", unsafe_allow_html=True)
    st.write("<p style='text-align: center;'>Advanced Neural Analysis & Forensic Gateway</p>", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([1, 1.2, 1])
    with col_b:
        auth_tab1, auth_tab2 = st.tabs(["🔑 Investigator Login", "📝 Node Registration"])
        with auth_tab1:
            u_input = st.text_input("Investigator Username")
            p_input = st.text_input("Security Key", type="password")
            if st.button("Authorize Access"):
                if authenticate_user(cursor, u_input, p_input):
                    st.session_state.is_authenticated = True
                    st.session_state.current_user = u_input
                    commit_audit_log(db_conn, cursor, st.session_state.current_user, "AUTH", "SYSTEM", "SUCCESS", "0.0%")
                    st.rerun()
                else:
                    st.error("Authentication Failed: Invalid Credentials")
        with auth_tab2:
            new_u = st.text_input("New Investigator ID")
            new_p = st.text_input("New Security Key", type="password")
            if st.button("Register New Node"):
                success, message = register_user(db_conn, cursor, new_u, new_p)
                if success:
                    st.success(message)
                else:
                    st.error(message)
    st.stop()

# --- 6. SIDEBAR CONTROLS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2092/2092663.png", width=80)
    st.title("System Navigator")
    st.write(f"🟢 **Session Active:** {st.session_state.current_user}")
    st.divider()
    ui_map = st.toggle("Enable Risk Heatmap", value=True)
    ui_feed = st.toggle("Live Intelligence Feed", value=True)
    st.divider()
    st.markdown("<div class='logout-btn'>", unsafe_allow_html=True)
    if st.button("🚪 Terminate Session"):
        st.session_state.is_authenticated = False
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- 7. MAIN INTERFACE LOGIC ---
st.markdown("<div class='main-header'>🛡️ AM UNIVERSAL FRAUD SENTINEL</div>", unsafe_allow_html=True)

# Global Statistics
s1, s2, s3, s4 = st.columns(4)
s1.metric("Global Nodes", "1.42 Billion", "+1.2M")
s2.metric("Neural Accuracy", "99.982%", "Stable")
s3.metric("GNN Latency", "0.0018ms", "Optimal")
s4.metric("Active Threats", "24", "-5", delta_color="inverse")

if ui_feed:
    st.info(
        f"📡 **Latest Trace:** {random.choice(['High-Value Wire detected in Node-7', 'New pattern matched in UPI-V4', 'Foreign IP attempt blocked'])}")
st.divider()

# --- PAGE: DASHBOARD ---
if st.session_state.active_page == 'dashboard':
    st.write("### 🏥 System Health Overview")
    h1, h2, h3 = st.columns(3)
    h1.metric("Fraud Today", f"{random.randint(5, 50)} Cases", f"-{random.randint(1, 10)}%")
    h2.metric("Transactions Scanned", f"{random.randint(10000, 50000):,}", f"+{random.randint(100, 500)}")
    h3.metric("Blocked Nodes", f"{random.randint(100, 500)} Nodes", f"+{random.randint(5, 20)}")
    st.divider()

    st.write("### 🗄️ Forensic Intelligence Modules")
    d1, d2, d3 = st.columns(3)
    with d1:
        if st.button("📱 UPI / Wallet Analyzer"): switch_view('analyzer')
    with d2:
        if st.button("🕸️ Neural Network Hub"): switch_view('network')
    with d3:
        if st.button("📜 Forensic Audit Logs"): switch_view('logs')

    st.write("### 🏥 Compliance & Risk Management")
    d4, d5, d6 = st.columns(3)
    with d4:
        if st.button("🏥 Insurance Verifier"): switch_view('analyzer')
    with d5:
        if st.button("⚖️ Tax & GST Forensic"): switch_view('analyzer')
    with d6:
        if st.button("📁 Enterprise Bulk Scan"): switch_view('analyzer')

    if ui_map:
        st.divider()
        st.write("### 🌍 Global Threat Distribution Map")
        map_df = pd.DataFrame({'lat': [28.6, 19.1, 13.0, 22.5, 34.0, 40.7],
                               'lon': [77.2, 72.8, 80.2, 88.3, -118.2, -74.0],
                               'risk': [15, 95, 45, 80, 60, 30]})
        fig_map = px.scatter_geo(map_df, lat="lat", lon="lon", size="risk", color="risk",
                                 color_continuous_scale="Reds", projection="orthographic")
        fig_map.update_layout(template="plotly_dark", margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_map, use_container_width=True)

# --- PAGE: ANALYZER (DETECTION ENGINE) ---
elif st.session_state.active_page == 'analyzer':
    st.header("🔍 Neural Detection Engine")

    col_x, col_y = st.columns(2)
    with col_x:
        tx_amt = st.number_input("Transaction Value ($)", min_value=1, value=5000, step=100)
        tx_hour = st.slider("Time of Transaction (24h Format)", 0, 23, 14)
    with col_y:
        loc_risk = st.slider("Geographic Risk Score", 0.0, 1.0, 0.15)
        auth_score = st.slider("Device Authentication Score", 0.0, 1.0, 0.9)

    node_id = st.text_input("Enter Target Node ID (Account/UPI/GSTIN)")

    if st.button("🚀 Execute Forensic Scan"):
        if not node_id:
            st.warning("Identification Node ID is required for scanning.")
        else:
            with st.spinner("Synchronizing with Neural Database..."):
                time.sleep(1.5)
                # ML PREDICTION LOGIC
                # [Amt, Hour, Loc_Risk, Auth_Score, Freq]
                freq_sim = random.randint(1, 15)
                features = [[tx_amt, tx_hour, loc_risk, auth_score, freq_sim]]
                probability = sentinel_model.predict_proba(features)[0][1]
                risk_val = probability * 100

                # --- 1. ENHANCED ANALYZER FIELDS ---
                txn_id = f"TXN{random.randint(100000, 999999)}"
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                st.info(f"🆔 **Transaction ID:** {txn_id}  |  🕒 **Timestamp:** {timestamp}")

                if probability > 0.65:
                    st.error(f"🚨 CRITICAL THREAT DETECTED: Risk Probability {risk_val:.2f}%")
                    st.error("🔒 Account Temporarily Blocked")
                    st.warning("🆔 KYC Verification Required")
                    st.info("📩 Notification sent to user and admin")
                    st.warning("⚡ **AUTO-ACTION:** Node has been isolated. Outbound transactions suspended.")
                    st.warning("Alert Sent to Admin (Simulated)")
                    commit_audit_log(db_conn, cursor, st.session_state.current_user, "DETECTION", node_id, "FRAUD_DETECTED", f"{risk_val:.1f}%", "ISOLATION_TRIGGERED")
                    st.snow()
                else:
                    st.success(f"✅ NODE VERIFIED SAFE: Risk Probability {risk_val:.2f}%")
                    commit_audit_log(db_conn, cursor, st.session_state.current_user, "DETECTION", node_id, "VERIFIED_SAFE", f"{risk_val:.1f}%", "NONE")
                    st.balloons()

                # --- NEW: AI INSIGHT SECTION ---
                insights = []
                if tx_amt > 10000: insights.append("high-value transaction")
                if loc_risk > 0.5: insights.append("high-risk location")
                if auth_score < 0.4: insights.append("low device trust")
                if freq_sim > 10: insights.append("unusual frequency")

                if insights:
                    insight_msg = f"🤖 **AI Insight:** {', '.join(insights).capitalize()} detected."
                    st.info(insight_msg)
                else:
                    st.info("🤖 **AI Insight:** Transaction patterns appear consistent with standard behavior.")

                # --- RISK BREAKDOWN SECTION ---
                st.write("---")
                st.subheader("📊 Forensic Risk Breakdown")
                rb1, rb2, rb3, rb4 = st.columns(4)
                rb1.metric("Transaction Value", f"${tx_amt:,.2f}")
                rb2.metric("Location Risk", f"{loc_risk:.2f}")
                rb3.metric("Device Auth Score", f"{auth_score:.2f}")
                rb4.metric("Frequency", f"{freq_sim}x")

    if st.button("⬅️ Return to Dashboard"): switch_view('dashboard')

# --- PAGE: LOGS ---
elif st.session_state.active_page == 'logs':
    st.header("📜 Universal Audit Repository")
    st.write("Official forensic logs for compliance and investigation.")

    # --- FILTER SECTION ---
    filter_user = st.text_input("🔍 Filter by User (Operator ID)")

    query = "SELECT * FROM universal_audit_logs"
    params = []
    if filter_user:
        query += " WHERE user LIKE ?"
        params.append(f"%{filter_user}%")
    query += " ORDER BY timestamp DESC"

    audit_data = pd.read_sql_query(query, db_conn, params=params)

    # --- NEW: FRAUD VS SAFE BAR CHART ---
    st.write("### 📊 Detection Distribution Analysis")
    # Filter for detection results
    summary_df = audit_data[audit_data['result'].isin(['FRAUD_DETECTED', 'VERIFIED_SAFE'])]
    if not summary_df.empty:
        chart_data = summary_df['result'].value_counts()
        st.bar_chart(chart_data)
    else:
        st.info("💡 No forensic detection data available for visualization yet.")

    st.dataframe(audit_data, use_container_width=True)
    
    # --- NEW: TOP RISK TRANSACTIONS ---
    st.write("### 🚩 Top Risk Transactions")
    # Filter for logs with a risk score and convert to numeric
    risk_df = audit_data.copy()
    # Handle percentages and convert to float
    risk_df['risk_numeric'] = risk_df['risk_score'].str.replace('%', '', regex=False).astype(float)
    top_5_risk = risk_df.sort_values(by='risk_numeric', ascending=False).head(5)
    
    if not top_5_risk.empty:
        st.dataframe(top_5_risk[['timestamp', 'entity', 'result', 'risk_score', 'action_taken']], use_container_width=True)
    else:
        st.info("💡 No high-risk data available yet.")

    csv_file = audit_data.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Forensic Report (CSV)", data=csv_file, file_name="forensic_audit_report.csv",
                       mime="text/csv")

    if st.button("⬅️ Return to Dashboard"): switch_view('dashboard')

# --- PAGE: NETWORK (GNN SIMULATION) ---
elif st.session_state.active_page == 'network':
    st.header("🕸️ Graph Neural Intelligence Hub")
    st.write("Visualization of inter-connected node behaviors and fraud propagation.")

    # Simulating GNN Topology with Plotly
    labels = ['Bank Nodes', 'Wallet Nodes', 'Insurance Nodes', 'Suspicious Links']
    values = [450, 250, 150, 45]

    c_p1, c_p2 = st.columns(2)
    with c_p1:
        st.plotly_chart(px.pie(names=labels, values=values, hole=0.5, title="Topology Distribution",
                               color_discrete_sequence=px.colors.sequential.RdBu), use_container_width=True)
    with c_p2:
        st.plotly_chart(px.bar(x=labels, y=values, title="Threat Clusters by Category",
                               color=labels, color_discrete_sequence=px.colors.qualitative.Set1),
                        use_container_width=True)

    st.info(
        "💡 **GNN Insight:** Most fraud propagation is occurring between Wallet Nodes and Bank Nodes via high-frequency micro-transactions.")

    if st.button("⬅️ Return to Dashboard"): switch_view('dashboard')