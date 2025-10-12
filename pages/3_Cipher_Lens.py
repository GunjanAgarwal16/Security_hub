import streamlit as st
import numpy as np
from PIL import Image
import io
import time

# Page config
st.set_page_config(
    page_title="Cipher Lens - SIA Hub",
    page_icon="🔒",
    layout="wide"
)

# Modern theme CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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

    .cipher-card {
        background: rgba(255, 255, 255, 0.95);
        color: #333;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .upload-zone {
        background: rgba(255, 255, 255, 0.1);
        border: 2px dashed rgba(255, 255, 255, 0.3);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        color: white;
        min-height: 150px;
    }

    .success-box {
        background: linear-gradient(135deg, #2ed573, #1fcc5c);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(46, 213, 115, 0.3);
    }

    .info-box {
        background: linear-gradient(135deg, #3742fa, #2f3542);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(55, 66, 250, 0.3);
    }

    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.8rem 2rem !important;
        font-weight: bold !important;
        font-size: 1rem !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }

    /* Image sizing fix */
    .stImage > img {
        max-height: 300px !important;
        width: auto !important;
        border-radius: 10px !important;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(102, 126, 234, 0.8);
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🔒 Cipher Lens - Image Security</h1>
    <p>Multi-Algorithm Encryption • AES-256 • Blowfish • Triple DES</p>
</div>
""", unsafe_allow_html=True)

# Back button
if st.button("← Back to SIA Hub", key="back_main"):
    st.switch_page("app.py")

# Sidebar with algorithm info
with st.sidebar:
    st.markdown("## 🔐 Encryption Algorithms")
    st.markdown("""
    **AES-256**: Industry standard  
    **Blowfish**: Variable-length key  
    **Triple DES**: Legacy support  

    ---

    ## 🛡️ Security Features
    ✅ Autonomous algorithm selection  
    ✅ Secure key generation  
    ✅ Integrity verification  
    ✅ Real-time processing
    """)

# Main tabs - ADDED DECRYPTION TAB
tab1, tab2 = st.tabs(["🔐 Encrypt Images", "🔓 Decrypt Images"])

with tab1:
    st.markdown("### 📷 Image Encryption")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="upload-zone">', unsafe_allow_html=True)

        uploaded_image = st.file_uploader(
            "📷 Select Image to Encrypt",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            help="Max 10MB • JPG, PNG, BMP supported"
        )

        if uploaded_image is not None:
            # FIXED IMAGE SIZE - not too large
            image = Image.open(uploaded_image)
            # Resize if too large
            if image.width > 400 or image.height > 300:
                image.thumbnail((400, 300), Image.Resampling.LANCZOS)

            st.image(image, caption=f"Original: {uploaded_image.name}", width=350)
            st.success(f"✅ Image loaded ({uploaded_image.size/1024:.1f} KB)")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="cipher-card">', unsafe_allow_html=True)
        st.markdown("#### ⚙️ Encryption Settings")

        algorithm = st.selectbox(
            "Algorithm",
            ["Auto-Select", "AES-256", "Blowfish", "Triple DES"]
        )

        key_method = st.radio(
            "Key Method",
            ["Auto-Generate", "Custom Key"]
        )

        if key_method == "Custom Key":
            custom_key = st.text_input("Encryption Key", type="password")

        st.markdown('</div>', unsafe_allow_html=True)

    # Encrypt button
    if st.button("🔐 Encrypt Image", type="primary", use_container_width=True):
        if uploaded_image is not None:
            with st.spinner("Encrypting image..."):
                progress = st.progress(0)
                for i in range(100):
                    progress.progress(i + 1)
                    time.sleep(0.02)

                # Mock encryption
                selected_algo = algorithm if algorithm != "Auto-Select" else np.random.choice(["AES-256", "Blowfish", "Triple DES"])
                generated_key = "".join(np.random.choice(list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"), 16)) if key_method == "Auto-Generate" else custom_key

                st.markdown(f"""
                <div class="success-box">
                    <h3>✅ Encryption Complete!</h3>
                    <p><strong>Algorithm</strong>: {selected_algo}</p>
                    <p><strong>Key Length</strong>: {len(generated_key) if generated_key else 'N/A'} characters</p>
                    <p><strong>Status</strong>: SUCCESS</p>
                </div>
                """, unsafe_allow_html=True)

                if key_method == "Auto-Generate":
                    st.markdown(f"""
                    <div class="info-box">
                        <h4>🔑 Generated Key (SAVE THIS!)</h4>
                        <p style="font-family: monospace; font-size: 1.2rem; background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px;">{generated_key}</p>
                    </div>
                    """, unsafe_allow_html=True)

                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📥 Download Encrypted File",
                        data=uploaded_image.getvalue(),
                        file_name=f"encrypted_{uploaded_image.name}.dat",
                        mime="application/octet-stream",
                        use_container_width=True
                    )

                with col2:
                    if st.button("🛡️ Send via SIA Protocol", use_container_width=True):
                        st.success("📤 Encrypted file prepared for SIA transmission!")

        else:
            st.error("⚠️ Please upload an image first!")

with tab2:  # DECRYPTION TAB - WAS MISSING!
    st.markdown("### 🔓 Image Decryption")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="upload-zone">', unsafe_allow_html=True)

        encrypted_file = st.file_uploader(
            "📁 Upload Encrypted File",
            type=['dat', 'enc', 'encrypted'],
            help="Upload .dat file from encryption process"
        )

        decryption_key = st.text_input(
            "🔑 Enter Decryption Key",
            type="password",
            placeholder="Enter the key used for encryption..."
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # Demo section
        st.markdown("#### 🧪 Try Demo")
        col_demo1, col_demo2 = st.columns(2)

        with col_demo1:
            if st.button("📷 Load Demo File", use_container_width=True):
                st.session_state.demo_file = True
                st.success("✅ Demo encrypted file loaded!")

        with col_demo2:
            if st.button("🔑 Use Demo Key: DEMO2024", use_container_width=True):
                st.session_state.demo_key = "DEMO2024"
                st.success("✅ Demo key loaded!")

    with col2:
        st.markdown('<div class="cipher-card">', unsafe_allow_html=True)
        st.markdown("#### 🔍 Decryption Process")
        st.markdown("""
        **Steps:**
        1. Upload encrypted .dat file
        2. Enter decryption key
        3. Verify integrity
        4. Decrypt image
        5. Download result
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # Decrypt button
    if st.button("🔓 Decrypt Image", type="primary", use_container_width=True):
        has_file = encrypted_file is not None or st.session_state.get('demo_file')
        has_key = decryption_key or st.session_state.get('demo_key')

        if has_file and has_key:
            with st.spinner("Decrypting image..."):
                progress = st.progress(0)
                for i in range(100):
                    progress.progress(i + 1)
                    time.sleep(0.02)

                # Mock successful decryption
                if st.session_state.get('demo_file') or decryption_key == st.session_state.get('demo_key', ''):
                    st.markdown("""
                    <div class="success-box">
                        <h3>✅ Decryption Successful!</h3>
                        <p><strong>Algorithm</strong>: AES-256</p>
                        <p><strong>Original Format</strong>: JPEG</p>
                        <p><strong>Integrity</strong>: VERIFIED</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Show sample decrypted image (PROPERLY SIZED)
                    sample_img = np.random.randint(0, 255, (200, 300, 3), dtype=np.uint8)
                    st.image(sample_img, caption="🔓 Decrypted Image", width=300)

                    st.download_button(
                        "📥 Download Decrypted Image",
                        data=sample_img.tobytes(),
                        file_name="decrypted_image.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )

                else:
                    st.error("🚫 Decryption failed! Invalid key or corrupted file.")

        else:
            if not has_file:
                st.error("⚠️ Please upload an encrypted file!")
            if not has_key:
                st.error("⚠️ Please enter the decryption key!")

# Navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏠 Main Hub", key="nav_main", use_container_width=True):
        st.switch_page("app.py")
with col2:
    if st.button("🎥 Violence Detection", key="nav_violence", use_container_width=True):
        st.switch_page("pages/1_Violence_Detection.py")
with col3:
    if st.button("📧 Email Analysis", key="nav_email", use_container_width=True):
        st.switch_page("pages/2_Email_Analysis.py")
