import streamlit as st

# Page configuration
st.set_page_config(
    page_title="SIA Hub - Security Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark theme CSS with excellent visibility and larger icons
st.markdown("""
<style>
    /* Dark theme for entire app */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #ffffff;
    }

    /* Remove default white spaces */
    .main > div {
        padding-top: 2rem;
        background: transparent;
    }

    /* Modern header with great contrast */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 3rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Service cards with dark theme and larger icons */
    .service-card {
        background: linear-gradient(145deg, #2d3748, #4a5568);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        text-align: center;
        min-height: 350px;
        color: white;
    }

    .service-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.4);
        border-color: #667eea;
    }

    /* Large, visible service icons */
    .service-icon {
        font-size: 4rem !important;
        margin-bottom: 1.5rem;
        display: block;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }

    /* Service titles - highly visible */
    .service-title {
        font-size: 1.8rem !important;
        font-weight: bold !important;
        color: #ffffff !important;
        margin: 1rem 0 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }

    /* Service descriptions */
    .service-desc {
        font-size: 1.1rem !important;
        color: #e2e8f0 !important;
        line-height: 1.6 !important;
        margin: 1rem 0 !important;
    }

    /* Launch buttons - highly visible */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 1rem 2rem !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        margin-top: 1rem !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }

    /* Stats cards with dark theme */
    .stat-card {
        background: linear-gradient(145deg, #4a5568, #2d3748);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        margin: 0.5rem;
        min-height: 140px;
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }

    .stat-number {
        font-size: 3rem !important;
        font-weight: bold !important;
        margin: 0 !important;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text;
        text-shadow: none !important;
    }

    .stat-label {
        font-size: 1.2rem !important;
        color: #e2e8f0 !important;
        margin: 1rem 0 0 0 !important;
        font-weight: 600 !important;
    }

    /* Architecture section */
    .arch-section {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 3rem 0;
        border: 2px solid rgba(255, 255, 255, 0.1);
        color: white;
    }

    .arch-step {
        background: rgba(102, 126, 234, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem;
        border: 1px solid rgba(102, 126, 234, 0.3);
        color: white;
        text-align: center;
    }

    .arch-arrow {
        font-size: 2rem;
        color: #667eea;
        text-shadow: 0 0 10px rgba(102, 126, 234, 0.8);
    }

    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Section headers */
    h1, h2, h3 {
        color: #ffffff !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 3.5rem; text-shadow: 0 4px 8px rgba(0,0,0,0.3);">🛡️ SIA Hub</h1>
    <p style="margin: 1rem 0 0 0; font-size: 1.8rem; opacity: 0.95; font-weight: 600;">Secure & Intelligent Alerting System</p>
    <p style="margin: 0.8rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">AI-Powered Security Services • Real-time Analysis • Advanced Encryption</p>
</div>
""", unsafe_allow_html=True)

# Quick stats with larger, more visible text
st.markdown('<h2 style="color: white; text-align: center; font-size: 2.2rem; margin-bottom: 2rem;">📊 System Performance</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">3</div>
        <div class="stat-label">AI Services</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">98.37%</div>
        <div class="stat-label">Email Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">93.25%</div>
        <div class="stat-label">Violence Detection</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">256-bit</div>
        <div class="stat-label">AES Encryption</div>
    </div>
    """, unsafe_allow_html=True)

# Launch Services section with large, visible icons and text
st.markdown('<h2 style="color: white; text-align: center; font-size: 2.5rem; margin: 3rem 0 2rem 0;">🚀 Launch Security Services</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="service-card">
        <div class="service-icon">🎥</div>
        <div class="service-title">Violence Detection</div>
        <div class="service-desc">
            <strong>MobileNetV2 + LSTM</strong><br>
            <strong>93.25% Accuracy</strong><br><br>
            Real-time video analysis for violence/non-violence classification with advanced AI processing and motion detection.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎥 Launch Violence Detection", key="violence", use_container_width=True):
        st.switch_page("pages/1_Violence_Detection.py")

with col2:
    st.markdown("""
    <div class="service-card">
        <div class="service-icon">📧</div>
        <div class="service-title">Email Threat Intelligence</div>
        <div class="service-desc">
            <strong>Bidirectional LSTM</strong><br>
            <strong>98.37% Accuracy</strong><br><br>
            Context-aware email threat classification with detailed analysis and comprehensive security reports.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📧 Launch Email Analysis", key="email", use_container_width=True):
        st.switch_page("pages/2_Email_Analysis.py")

with col3:
    st.markdown("""
    <div class="service-card">
        <div class="service-icon">🔒</div>
        <div class="service-title">Cipher Lens Security</div>
        <div class="service-desc">
            <strong>Multi-Algorithm Encryption</strong><br>
            <strong>AES-256 • Blowfish • 3DES</strong><br><br>
            Advanced image encryption/decryption with algorithm selection and secure key management.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔒 Launch Cipher Lens", key="cipher", use_container_width=True):
        st.switch_page("pages/3_Cipher_Lens.py")

# Compact architecture overview
st.markdown("""
<div class="arch-section">
    <h2 style="text-align: center; margin-bottom: 2rem; font-size: 2.2rem;">🏗️ SIA Architecture Overview</h2>
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div class="arch-step" style="flex: 1; min-width: 200px;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🎥</div>
            <strong style="font-size: 1.3rem;">1. Intelligent Detection</strong><br>
            <span style="font-size: 1rem; opacity: 0.9;">AI identifies security threats</span>
        </div>
        <div class="arch-arrow">→</div>
        <div class="arch-step" style="flex: 1; min-width: 200px;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔒</div>
            <strong style="font-size: 1.3rem;">2. Secure Encryption</strong><br>
            <span style="font-size: 1rem; opacity: 0.9;">Evidence protection</span>
        </div>
        <div class="arch-arrow">→</div>
        <div class="arch-step" style="flex: 1; min-width: 200px;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">📡</div>
            <strong style="font-size: 1.3rem;">3. Two-Factor Alert</strong><br>
            <span style="font-size: 1rem; opacity: 0.9;">Secure transmission</span>
        </div>
        <div class="arch-arrow">→</div>
        <div class="arch-step" style="flex: 1; min-width: 200px;">
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🛡️</div>
            <strong style="font-size: 1.3rem;">4. Authorized Access</strong><br>
            <span style="font-size: 1rem; opacity: 0.9;">Secure verification</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2.5rem; background: rgba(255,255,255,0.05); border-radius: 20px; margin-top: 3rem; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1);">
    <h3 style="margin: 0; color: #667eea; font-size: 1.8rem;">🎓 M.Tech Project - AI Security Intelligence Hub</h3>
    <p style="margin: 1rem 0; color: #e2e8f0; font-size: 1.1rem; font-weight: 500;">Database-free Security Architecture • Cryptographic Evidence Chain • Two-factor Authentication</p>
    <div style="margin-top: 1.5rem;">
        <span style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.7rem 1.5rem; border-radius: 25px; margin: 0 0.5rem; font-size: 1rem; font-weight: 600; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">Streamlit</span>
        <span style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.7rem 1.5rem; border-radius: 25px; margin: 0 0.5rem; font-size: 1rem; font-weight: 600; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">TensorFlow</span>
        <span style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.7rem 1.5rem; border-radius: 25px; margin: 0 0.5rem; font-size: 1rem; font-weight: 600; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">OpenCV</span>
        <span style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.7rem 1.5rem; border-radius: 25px; margin: 0 0.5rem; font-size: 1rem; font-weight: 600; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">Cryptography</span>
    </div>
</div>
""", unsafe_allow_html=True)
