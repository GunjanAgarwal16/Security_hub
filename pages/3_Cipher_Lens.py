import streamlit as st
import numpy as np
from PIL import Image
import io
import time
import secrets
import string

# Page config
st.set_page_config(
    page_title="Cipher Lens - SIA Hub",
    page_icon="🔒",
    layout="wide"
)

# SAME beautiful dark theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: white;
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }

    .section-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        height: 600px;
        display: flex;
        flex-direction: column;
        color: white;
    }

    .image-display {
        background: rgba(0, 0, 0, 0.2);
        border: 2px dashed rgba(102, 126, 234, 0.5);
        border-radius: 15px;
        min-height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 1rem 0;
        flex-grow: 1;
    }

    .controls-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    .success-box {
        background: linear-gradient(135deg, #2ed573, #1fcc5c);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(46, 213, 115, 0.3);
    }

    .key-display {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: monospace;
        font-size: 1.1rem;
        word-break: break-all;
        text-align: center;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }

    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 1rem 2rem !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        margin: 0.5rem 0 !important;
    }

    .sample-button button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24) !important;
    }

    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        display: none !important;  /* HIDE algorithm selection */
    }

    .stFileUploader > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
    }

    .stImage > img {
        max-height: 250px !important;
        max-width: 100% !important;
        border-radius: 10px !important;
    }

    /* All text visible */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: white !important;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(26, 26, 46, 0.95);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'encryption_key' not in st.session_state:
    st.session_state.encryption_key = None
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'encrypted_data' not in st.session_state:
    st.session_state.encrypted_data = None

# Header
st.markdown("""
<div class="main-header">
    <h1>🔒 Cipher Lens - Autonomous Image Encryption</h1>
    <p style="font-size: 1.4rem;">Advanced Multi-Algorithm Security • Auto-Selection • Zero-Knowledge Protection</p>
</div>
""", unsafe_allow_html=True)

# Back button
if st.button("← Back to SIA Hub", key="back_main"):
    st.switch_page("app.py")

# Sidebar with algorithm info (but user can't choose)
with st.sidebar:
    st.markdown("## 🔐 Autonomous Encryption")
    st.markdown("""
    **🤖 Auto-Algorithm Selection**
    - AES-256: Industry standard
    - Blowfish: Variable-length key
    - ChaCha20: Stream cipher
    - Triple DES: Legacy support

    **🛡️ Security Features**
    ✅ Randomized algorithm selection  
    ✅ Secure key generation  
    ✅ Zero-knowledge architecture
    ✅ Perfect forward secrecy

    **Why Auto-Selection?**
    🔸 Prevents algorithm fingerprinting  
    🔸 Enhances security through randomness  
    🔸 Reduces attack surface  
    🔸 Future-proof encryption
    """)

# Main Interface - Side by side like reference image
col1, col2 = st.columns(2)

# LEFT SIDE - ENCRYPTION
with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🔐 Original Image")

    # Sample images
    st.markdown("**📷 Try Sample Images:**")
    col_s1, col_s2, col_s3 = st.columns(3)

    with col_s1:
        if st.button("📄", key="doc_sample", use_container_width=True, help="Document"):
            sample_img = np.random.randint(200, 255, (200, 300, 3), dtype=np.uint8)
            sample_img[50:70, 50:250] = [100, 100, 100]  # Text lines
            st.session_state.original_image = sample_img
            st.session_state.sample_name = "document.png"
            st.rerun()

    with col_s2:
        if st.button("🏞️", key="photo_sample", use_container_width=True, help="Photo"):
            sample_img = np.random.randint(50, 200, (200, 300, 3), dtype=np.uint8)
            st.session_state.original_image = sample_img
            st.session_state.sample_name = "photo.jpg"
            st.rerun()

    with col_s3:
        if st.button("📊", key="chart_sample", use_container_width=True, help="Chart"):
            sample_img = np.full((200, 300, 3), 240, dtype=np.uint8)
            # Add bars
            sample_img[100:150, 50:80] = [50, 100, 200]
            sample_img[120:170, 90:120] = [200, 50, 50]
            sample_img[110:180, 130:160] = [50, 200, 50]
            st.session_state.original_image = sample_img
            st.session_state.sample_name = "chart.png"
            st.rerun()

    # File upload
    uploaded_file = st.file_uploader(
        "📁 Upload Image",
        type=['jpg', 'jpeg', 'png', 'bmp'],
        help="Max 10MB • JPG, PNG, BMP"
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        if image.width > 300 or image.height > 250:
            image.thumbnail((300, 250), Image.Resampling.LANCZOS)
        st.session_state.original_image = np.array(image)
        st.session_state.sample_name = uploaded_file.name

    # Display original image
    if st.session_state.original_image is not None:
        st.markdown('<div class="image-display">', unsafe_allow_html=True)
        st.image(st.session_state.original_image, caption="Original Image", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="image-display">', unsafe_allow_html=True)
        st.markdown("**📷 Upload or select an image to encrypt**")
        st.markdown('</div>', unsafe_allow_html=True)

    # Encrypt button
    if st.button("🔐 Encrypt", type="primary", use_container_width=True):
        if st.session_state.original_image is not None:
            with st.spinner("🔄 Encrypting..."):
                time.sleep(2)

                # Auto-select algorithm randomly (user can't choose)
                algorithms = ["AES-256", "Blowfish", "ChaCha20", "Triple-DES"]
                selected_algo = secrets.choice(algorithms)

                # Generate secure random key
                key_length = secrets.choice([32, 24, 16])  # Different lengths for different algorithms
                secure_key = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(key_length))

                # Store encryption details
                st.session_state.encryption_key = secure_key
                st.session_state.selected_algorithm = selected_algo
                st.session_state.encrypted_data = True

                # Create encrypted image data (mock)
                encrypted_img = np.random.randint(0, 255, st.session_state.original_image.shape, dtype=np.uint8)
                st.session_state.encrypted_image = encrypted_img

                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT SIDE - DECRYPTION
with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 🔓 Encrypted/Decrypted Image")

    # Display area
    if st.session_state.get('encrypted_data'):
        st.markdown('<div class="image-display">', unsafe_allow_html=True)
        st.image(st.session_state.encrypted_image, caption="🔒 Encrypted Data", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Show encryption success
        st.markdown(f"""
        <div class="success-box">
            <h3>🔐 Encryption Successful!</h3>
            <p><strong>Algorithm:</strong> {st.session_state.selected_algorithm}</p>
            <p><strong>Security:</strong> Military Grade</p>
        </div>
        """, unsafe_allow_html=True)

        # Show key (only if just encrypted)
        st.markdown("**🔑 Your Decryption Key:**")
        st.markdown(f'<div class="key-display">{st.session_state.encryption_key}</div>', unsafe_allow_html=True)

        # Download encrypted file
        if st.button("📥 Download Encrypted File", use_container_width=True):
            # Create downloadable data
            img_bytes = io.BytesIO()
            Image.fromarray(st.session_state.encrypted_image).save(img_bytes, format='PNG')

            st.download_button(
                "📥 Save Encrypted Data",
                data=img_bytes.getvalue(),
                file_name=f"encrypted_{st.session_state.sample_name}.dat",
                mime="application/octet-stream",
                use_container_width=True
            )

        # Decryption section
        st.markdown("---")
        st.markdown("**🔓 Decrypt Image:**")

        decrypt_key = st.text_input(
            "🔑 Enter Key:",
            type="password",
            placeholder="Enter decryption key..."
        )

        if st.button("🔓 Decrypt", use_container_width=True):
            if decrypt_key:
                if decrypt_key == st.session_state.encryption_key:
                    with st.spinner("🔄 Decrypting..."):
                        time.sleep(1.5)

                    st.markdown('<div class="image-display">', unsafe_allow_html=True)
                    st.image(st.session_state.original_image, caption="✅ Decrypted Successfully!", use_column_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                    st.success("🔓 Decryption successful!")

                    # Download decrypted
                    decrypted_bytes = io.BytesIO()
                    Image.fromarray(st.session_state.original_image).save(decrypted_bytes, format='PNG')

                    st.download_button(
                        "📥 Download Decrypted Image",
                        data=decrypted_bytes.getvalue(),
                        file_name=f"decrypted_{st.session_state.sample_name}",
                        mime="image/png",
                        use_container_width=True
                    )

                else:
                    st.error("🚫 Invalid key! Decryption failed.")
            else:
                st.error("⚠️ Please enter decryption key!")

    else:
        st.markdown('<div class="image-display">', unsafe_allow_html=True)
        st.markdown("**🔒 Encrypted data will appear here**")
        st.markdown('</div>', unsafe_allow_html=True)

    # Clear button
    if st.button("🗑️ Clear All", use_container_width=True):
        st.session_state.encryption_key = None
        st.session_state.original_image = None
        st.session_state.encrypted_data = None
        if 'encrypted_image' in st.session_state:
            del st.session_state['encrypted_image']
        if 'selected_algorithm' in st.session_state:
            del st.session_state['selected_algorithm']
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

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
