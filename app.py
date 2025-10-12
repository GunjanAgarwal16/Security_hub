import streamlit as st

# Page configuration
st.set_page_config(
    page_title="SIA Hub - Security Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS with dark theme and clean design
st.markdown("""
<style>
    /* Remove default padding and margins */
    .main > div {
        padding-top: 2rem;
    }

    /* Hide sidebar by default for cleaner look */
    .css-1d391kg {
        padding: 1rem;
    }

    /* Modern header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Service cards with modern design */
    .service-card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        text-align: center;
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .service-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15);
    }

    /* Modern buttons */
    .nav-button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 1rem;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }

    .nav-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    /* Stats cards */
    .stat-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 0.5rem;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .stat-number {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .stat-label {
        font-size: 1rem;
        color: #666;
        margin: 0.5rem 0 0 0;
    }

    /* Remove all white spaces */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }

    /* Clean spacing */
    .element-container {
        margin-bottom: 0 !important;
    }

    .stColumns {
        gap: 1rem;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Service icons */
    .service-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 3rem;">🛡️ SIA Hub</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.5rem; opacity: 0.9;">Secure & Intelligent Alerting System</p>
    <p style="margin: 0.5rem 0 0 0; opacity: 0.8;">AI-Powered Security Services • Real-time Analysis • Advanced Encryption</p>
</div>
""", unsafe_allow_html=True)

# Quick stats
st.markdown("### 📊 System Overview")
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

# Main services with direct navigation
st.markdown("### 🚀 Launch Services")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="service-card">
        <div>
            <div class="service-icon">🎥</div>
            <h3>Violence Detection</h3>
            <p>MobileNetV2 + LSTM<br><strong>93.25% Accuracy</strong></p>
            <p style="color: #666; font-size: 0.9rem;">Upload videos for real-time violence/non-violence classification with advanced AI processing.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🎥 Launch Violence Detection", key="violence", use_container_width=True):
        st.switch_page("pages/1_Violence_Detection.py")

with col2:
    st.markdown("""
    <div class="service-card">
        <div>
            <div class="service-icon">📧</div>
            <h3>Email Threat Intel</h3>
            <p>Bidirectional LSTM<br><strong>98.37% Accuracy</strong></p>
            <p style="color: #666; font-size: 0.9rem;">Advanced email threat classification with contextual analysis and detailed reports.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("📧 Launch Email Analysis", key="email", use_container_width=True):
        st.switch_page("pages/2_Email_Analysis.py")

with col3:
    st.markdown("""
    <div class="service-card">
        <div>
            <div class="service-icon">🔒</div>
            <h3>Cipher Lens</h3>
            <p>Multi-Algorithm<br><strong>AES-256 • Blowfish • 3DES</strong></p>
            <p style="color: #666; font-size: 0.9rem;">Advanced image encryption/decryption with secure key management and integrity verification.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔒 Launch Cipher Lens", key="cipher", use_container_width=True):
        st.switch_page("pages/3_Cipher_Lens.py")

# Quick architecture overview - compact
st.markdown("### 🏗️ SIA Architecture")
st.markdown("""
<div style="background: rgba(255,255,255,0.9); padding: 2rem; border-radius: 15px; margin: 2rem 0;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
        <div style="flex: 1; min-width: 200px; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🎥</div>
            <strong>1. Detect</strong><br>
            <small>AI identifies threats</small>
        </div>
        <div style="font-size: 1.5rem; color: #667eea;">→</div>
        <div style="flex: 1; min-width: 200px; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔒</div>
            <strong>2. Encrypt</strong><br>
            <small>Secure evidence</small>
        </div>
        <div style="font-size: 1.5rem; color: #667eea;">→</div>
        <div style="flex: 1; min-width: 200px; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">📡</div>
            <strong>3. Alert</strong><br>
            <small>Two-factor transmission</small>
        </div>
        <div style="font-size: 1.5rem; color: #667eea;">→</div>
        <div style="flex: 1; min-width: 200px; text-align: center;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🛡️</div>
            <strong>4. Verify</strong><br>
            <small>Secure access</small>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.8); border-radius: 15px; margin-top: 2rem;">
    <h4 style="margin: 0; color: #667eea;">🎓 M.Tech Project - AI Security Intelligence</h4>
    <p style="margin: 0.5rem 0; color: #666;">Database-free Security • Cryptographic Evidence • Two-factor Authentication</p>
    <div style="margin-top: 1rem;">
        <span style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem; font-size: 0.9rem;">Streamlit</span>
        <span style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem; font-size: 0.9rem;">TensorFlow</span>
        <span style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem; font-size: 0.9rem;">OpenCV</span>
        <span style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 0.5rem 1rem; border-radius: 25px; margin: 0 0.5rem; font-size: 0.9rem;">Cryptography</span>
    </div>
</div>
""", unsafe_allow_html=True)
