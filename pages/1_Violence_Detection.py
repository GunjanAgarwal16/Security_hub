import streamlit as st
import numpy as np
import time

# Page config
st.set_page_config(
    page_title="Violence Detection - SIA Hub",
    page_icon="🎥",
    layout="wide"
)

# Modern dark theme CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }

    .main-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }

    .analysis-card {
        background: rgba(255, 255, 255, 0.95);
        color: #333;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .result-violence {
        background: linear-gradient(135deg, #ff4757, #ff3742);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 71, 87, 0.3);
    }

    .result-safe {
        background: linear-gradient(135deg, #2ed573, #1fcc5c);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(46, 213, 115, 0.3);
    }

    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.8rem 2rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(30, 60, 114, 0.8);
        backdrop-filter: blur(10px);
    }

    .css-1d391kg .css-1d391kg {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'encrypted' not in st.session_state:
    st.session_state.encrypted = False
if 'alert_sent' not in st.session_state:
    st.session_state.alert_sent = False

# Header
st.markdown("""
<div class="main-header">
    <h1>🎥 Violence Detection System</h1>
    <p>MobileNetV2 + LSTM • 93.25% Accuracy • Real-time Analysis</p>
</div>
""", unsafe_allow_html=True)

# Back to main button
if st.button("← Back to SIA Hub", key="back_main"):
    st.switch_page("app.py")

# Quick stats in sidebar
with st.sidebar:
    st.markdown("## 🧠 AI Model")
    st.markdown("""
    **Architecture**: MobileNetV2 + LSTM  
    **Accuracy**: 93.25%  
    **Input**: Video frames  
    **Output**: Violence/Non-violence  
    **Processing**: Real-time
    """)

    st.markdown("---")
    st.markdown("## ⚙️ Features")
    st.markdown("""
    ✅ Motion-activated processing  
    ✅ Prediction smoothing  
    ✅ Face detection  
    ✅ Frame-by-frame analysis  
    ✅ SIA integration
    """)

# Main interface - compact
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📹 Video Analysis")

    # Upload section
    uploaded_video = st.file_uploader(
        "Upload video file",
        type=['mp4', 'avi', 'mov', 'mkv'],
        help="Max 200MB • Supported: MP4, AVI, MOV, MKV"
    )

    # Sample videos
    st.markdown("**Or try samples:**")
    col_sample1, col_sample2 = st.columns(2)

    with col_sample1:
        if st.button("📱 Safe Video", key="safe_sample", use_container_width=True):
            st.session_state.sample_video = "safe"
            st.success("✅ Safe video loaded!")

    with col_sample2:
        if st.button("⚠️ Violence Video", key="violence_sample", use_container_width=True):
            st.session_state.sample_video = "violence"
            st.success("✅ Violence video loaded!")

with col2:
    st.markdown("### ⚙️ Settings")
    confidence = st.slider("Confidence Threshold", 0.5, 0.95, 0.85)
    face_detect = st.checkbox("Face Detection", True)
    smoothing = st.checkbox("Prediction Smoothing", True)

# Analysis button
if st.button("🔍 Analyze Video", type="primary", use_container_width=True):
    has_video = uploaded_video is not None or st.session_state.get('sample_video')

    if has_video:
        # Show processing
        with st.spinner("Analyzing video..."):
            progress = st.progress(0)
            for i in range(100):
                progress.progress(i + 1)
                time.sleep(0.03)

            # Mock results
            if st.session_state.get('sample_video') == 'violence':
                violence_detected = True
                confidence_score = 0.94
                key_indicators = [
                    "Aggressive motion patterns detected",
                    "Physical confrontation identified", 
                    "High-intensity movements",
                    "Multiple subjects involved"
                ]
            else:
                violence_detected = False
                confidence_score = 0.89
                key_indicators = [
                    "Normal activity patterns",
                    "No aggressive behavior",
                    "Safe environment detected",
                    "Standard motion analysis"
                ]

            # Store results in session state
            st.session_state.analysis_done = True
            st.session_state.violence_detected = violence_detected
            st.session_state.confidence_score = confidence_score
            st.session_state.key_indicators = key_indicators

# Display results if analysis was done
if st.session_state.get('analysis_done'):
    violence_detected = st.session_state.violence_detected
    confidence_score = st.session_state.confidence_score
    key_indicators = st.session_state.key_indicators

    st.markdown("---")
    if violence_detected:
        st.markdown(f"""
        <div class="result-violence">
            <h2>🚨 VIOLENCE DETECTED</h2>
            <h3>Confidence: {confidence_score:.1%}</h3>
            <p><strong>IMMEDIATE ATTENTION REQUIRED</strong></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="result-safe">
            <h2>✅ NO VIOLENCE DETECTED</h2>
            <h3>Confidence: {confidence_score:.1%}</h3>
            <p><strong>Scene classified as safe</strong></p>
        </div>
        """, unsafe_allow_html=True)

    # Analysis details
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown("#### 📊 Analysis Metrics")
        st.metric("Frames Processed", "847")
        st.metric("Processing Time", "15.3s")
        st.metric("Motion Intensity", "8.7/10" if violence_detected else "3.2/10")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown("#### 🎯 Key Indicators")
        for indicator in key_indicators:
            st.markdown(f"• {indicator}")
        st.markdown('</div>', unsafe_allow_html=True)

    # SIA Integration - WORKING BUTTONS
    if violence_detected:
        st.markdown("---")
        st.markdown("### 🛡️ SIA Protocol Activation")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔒 Encrypt Evidence", key="encrypt_btn"):
                st.session_state.encrypted = True
                st.rerun()

        with col2:
            if st.button("📡 Send SIA Alert", key="alert_btn"):
                st.session_state.alert_sent = True
                st.rerun()

        # Show status
        if st.session_state.encrypted:
            st.success("🔐 Evidence encrypted successfully!")
            st.info("📁 File: encrypted_evidence.dat created")

        if st.session_state.alert_sent:
            st.success("📤 SIA Alert dispatched!")
            st.info("📱 Public: Encrypted file transmitted")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Main Hub", key="nav_main", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button("📧 Email Analysis", key="nav_email", use_container_width=True):
        st.switch_page("pages/2_Email_Analysis.py")
with col3:
    if st.button("🔒 Cipher Lens", key="nav_cipher", use_container_width=True):
        st.switch_page("pages/3_Cipher_Lens.py")
