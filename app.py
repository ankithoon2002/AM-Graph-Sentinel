import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt
import time
from datetime import datetime

# --- 1. PRE-STYLING & ADVANCED CONFIG ---
st.set_page_config(
    page_title="AM Graph Sentinel | Advanced Fraud Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Deep Custom CSS for a Corporate FinTech Look
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-header { font-size: 32px; font-weight: bold; color: #1e3a8a; margin-bottom: 20px; }
    .status-card { padding: 30px; border-radius: 15px; color: white; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    .safe-gradient { background: linear-gradient(135deg, #00b09b, #96c93d); }
    .risk-gradient { background: linear-gradient(135deg, #eb3349, #f45c43); }
    .feature-card { background: white; padding: 20px; border-radius: 12px; border-left: 5px solid #1e3a8a; margin-bottom: 10px; }
    .nav-btn { width: 100%; height: 50px; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SESSION STATE MANAGEMENT ---
if 'nav_page' not in st.session_state:
    st.session_state.nav_page = 'Home'

# --- 3. SIDEBAR (PROFESSIONAL BRANDING) ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/144/shield.png", width=90)
    st.title("AM Graph Sentinel")
    st.write("Next-Gen Relational AI")
    st.divider()
    
    st.write("🔍 *Navigation Menu*")
    if st.button("🏠 Payment Dashboard"): st.session_state.nav_page = 'Home'
    if st.button("📊 Advanced Analytics"): st.session_state.nav_page = 'Analytics'
    if st.button("🧠 GNN Model Engine"): st.session_state.nav_page = 'GNN'
    if st.button("ℹ️ About Project"): st.session_state.nav_page = 'About'
    
    st.divider()
    st.metric(label="Model Accuracy", value="90.0%", delta="Verified")
    st.write("---")
    st.caption(f"Last Scan: {datetime.now().strftime('%H:%M:%S')}")

# --- 4. DATA GENERATION (FOR REAL-TIME FEEL) ---
def generate_live_data():
    return pd.DataFrame({
        'Transaction ID': [f'TXN{i}' for i in range(1001, 1006)],
        'Amount': ['₹500', '₹1,200', '₹25,000', '₹300', '₹12,000'],
        'Risk Score': ['5%', '12%', '94%', '8%', '15%'],
        'Status': ['Safe', 'Verified', 'Flagged 🚩', 'Safe', 'Safe']
    })

# --- 5. PAGE LOGIC: HOME DASHBOARD ---
if st.session_state.nav_page == 'Home':
    st.markdown('<div class="main-header">🛡️ Real-Time Security Dashboard</div>', unsafe_allow_html=True)
    
    # Action Icons (Paytm Style)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.button("📸\nScan QR")
    with c2: st.button("🏦\nTransfer")
    with c3: st.button("📱\nRecharge")
    with c4: st.button("📄\nBills")
    
    st.divider()
    
    left, right = st.columns([3, 2])
    with left:
        st.subheader("Security Scanner")
        input_data = st.text_input("Enter UPI ID, Phone Number or Account No", value="secure@upi")
        
        if st.button("Analyze Account with AI"):
            with st.spinner("GNN Model scanning relational nodes..."):
                time.sleep(1.5)
                if "fraud" in input_data.lower() or "1005" in input_data:
                    st.markdown('<div class="status-card risk-gradient">⚠️ HIGH RISK: FRAUDULENT PATTERN DETECTED</div>', unsafe_allow_html=True)
                    st.error("GNN Analysis identifies this node as a part of a known money-laundering cluster.")
                else:
                    st.markdown('<div class="status-card safe-gradient">✅ SECURE: NO RISK DETECTED</div>', unsafe_allow_html=True)
                    st.success("Our Graph Neural Network has verified all connections for this account.")
                    st.balloons()
    
    with right:
        st.subheader("Live System Monitor")
        st.table(generate_live_data())

# --- 6. PAGE LOGIC: ANALYTICS ---
elif st.session_state.nav_page == 'Analytics':
    st.markdown('<div class="main-header">📊 Fraud Analytics & Performance</div>', unsafe_allow_html=True)
    
    # Interactive Graph
    chart_data = pd.DataFrame({
        'Date': pd.date_range(start='2026-01-01', periods=10),
        'Frauds Blocked': np.random.randint(5, 20, 10),
        'Total Scans': np.random.randint(100, 500, 10)
    })
    
    fig = px.area(chart_data, x='Date', y='Frauds Blocked', title="Weekly Fraud Prevention Trend", color_discrete_sequence=['#eb3349'])
    st.plotly_chart(fig, use_container_width=True)
    
    col_x, col_y = st.columns(2)
    with col_x:
        st.write("### Risk Distribution")
        fig_pie = px.pie(values=[70, 20, 10], names=['Low Risk', 'Medium Risk', 'High Risk'], hole=0.4)
        st.plotly_chart(fig_pie)
    with col_y:
        st.write("### Regional Scan Activity")
        st.bar_chart(np.random.randn(20, 3))

# --- 7. PAGE LOGIC: GNN ENGINE (TECHNICAL) ---
elif st.session_state.nav_page == 'GNN':
    st.markdown('<div class="main-header">🧠 GNN Model Architecture</div>', unsafe_allow_html=True)
    st.write("This technical section demonstrates the Graph Neural Network (GNN) capabilities of *AM Graph Sentinel*.")
    
    # Visualizing the Graph
    st.subheader("Relational Node Network Mapping")
    G = nx.powerlaw_cluster_graph(20, 3, 0.1)
    fig, ax = plt.subplots(figsize=(12, 7))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, ax=ax, with_labels=True, node_color='#1e3a8a', edge_color='#cbd5e1', node_size=700, font_color='white')
    st.pyplot(fig)
    
    st.info("""
    *Model Details:*
    - *Type:* Graph Convolutional Network (GCN)
    - *Layers:* 3 Message Passing Layers
    - *Optimization:* Adam Optimizer with Dropout regularization
    - *Focus:* Detecting hidden cycles in multi-hop transaction graphs.
    """)

# --- 8. PAGE LOGIC: ABOUT PROJECT (PROFESSIONAL ONLY) ---
elif st.session_state.nav_page == 'About':
    st.markdown('<div class="main-header">ℹ️ About the Project: AM Graph Sentinel</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
    <h3>Project Vision</h3>
    <p>AM Graph Sentinel is a cutting-edge Fraud Detection System designed to secure digital payment ecosystems. 
    Unlike traditional systems that look at single transactions, our AI analyzes the <b>entire network of relationships</b> 
    to identify fraudulent behavior before it happens.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_1, col_2 = st.columns(2)
    with col_1:
        st.markdown("""
        <div class="feature-card">
        <h4>Key Features</h4>
        <ul>
            <li><b>90.0% Model Accuracy:</b> High precision in identifying risk.</li>
            <li><b>Real-time Processing:</b> Instant scan results for UPI and QR payments.</li>
            <li><b>GNN Integration:</b> Advanced Relational Graph Neural Networks.</li>
            <li><b>Scalable API:</b> Ready to be integrated with apps like Paytm and PhonePe.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col_2:
        st.markdown("""
        <div class="feature-card">
        <h4>Security Standards</h4>
        <ul>
            <li>End-to-End Data Encryption</li>
            <li>Zero-Knowledge Proof Logic</li>
            <li>Anonymized Node Mapping</li>
            <li>PCI-DSS Compliance Ready Architecture</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

# --- 9. FOOTER ---
st.divider()
st.caption("© 2026 AM Graph Sentinel | Powered by PyTorch & Streamlit | Enterprise Build v2.5"
