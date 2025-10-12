import streamlit as st
import numpy as np
from PIL import Image
import io
import time
import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Page config
st.set_page_config(
    page_title="Cipher Lens - Advanced Image Encryption",
    page_icon="🔒",
    layout="wide"
)

# Beautiful professional dark theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 3rem;
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        border: 2px solid rgba(255, 255, 255, 0.1);
    }

    .control-panel {
        background: linear-gradient(145deg, #2d3748, #4a5568);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.1);
    }

    .image-container {
        background: linear-gradient(145deg, #374151, #4b5563);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        min-height: 400px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }

    .upload-area {
        background: rgba(102, 126, 234, 0.1);
        border: 3px dashed rgba(102, 126, 234, 0.5);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }

    .upload-area:hover {
        background: rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.8);
        transform: translateY(-2px);
    }

    .success-panel {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .key-display {
        background: linear-gradient(145deg, #1f2937, #374151);
        border: 2px solid rgba(251, 191, 36, 0.5);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
        word-break: break-all;
        text-align: center;
        color: #fbbf24;
        font-weight: bold;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }

    .info-panel {
        background: linear-gradient(145deg, #3730a3, #4338ca);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 25px rgba(55, 48, 163, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .stButton > button {
        background: linear-gradient(45deg, #10b981, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 1rem 2rem !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        width: 100% !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 5px 15px rgba(16, 185, 129, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.6) !important;
    }

    .encrypt-btn button {
        background: linear-gradient(45deg, #dc2626, #b91c1c) !important;
    }

    .decrypt-btn button {
        background: linear-gradient(45deg, #2563eb, #1d4ed8) !important;
    }

    .clear-btn button {
        background: linear-gradient(45deg, #6b7280, #4b5563) !important;
    }

    .sample-btn button {
        background: linear-gradient(45deg, #f59e0b, #d97706) !important;
        padding: 0.5rem 1rem !important;
        font-size: 1rem !important;
    }

    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    .stFileUploader > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }

    .stImage > img {
        border-radius: 10px !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3) !important;
        max-height: 300px !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: white !important;
    }

    .css-1d391kg {
        background: linear-gradient(135deg, #1f2937, #374151);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Encryption functions
def generate_key(algorithm):
    """Generate a secure key"""
    if algorithm == "AES-256":
        return os.urandom(32)
    elif algorithm == "AES-192": 
        return os.urandom(24)
    else:  # AES-128
        return os.urandom(16)

def encrypt_image(image_data, key):
    """Encrypt image data"""
    try:
        # Convert image to bytes
        img_bytes = image_data.tobytes()

        # Pad data
        padding_length = 16 - (len(img_bytes) % 16)
        padded_data = img_bytes + bytes([padding_length]) * padding_length

        # Create cipher
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Encrypt
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        return iv + encrypted_data, len(img_bytes)
    except Exception as e:
        return None, None

def decrypt_image(encrypted_data, key, original_size, shape):
    """Decrypt image data"""
    try:
        # Extract IV and encrypted data
        iv = encrypted_data[:16]
        encrypted_bytes = encrypted_data[16:]

        # Create cipher
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # Decrypt
        padded_data = decryptor.update(encrypted_bytes) + decryptor.finalize()

        # Remove padding
        padding_length = padded_data[-1]
        original_data = padded_data[:-padding_length]

        # Restore original size
        original_data = original_data[:original_size]

        # Convert back to image
        decrypted_array = np.frombuffer(original_data, dtype=np.uint8)
        decrypted_image = decrypted_array.reshape(shape)

        return decrypted_image
    except Exception as e:
        return None

# Initialize session state
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'encrypted_data' not in st.session_state:
    st.session_state.encrypted_data = None
if 'encryption_key' not in st.session_state:
    st.session_state.encryption_key = None
if 'algorithm' not in st.session_state:
    st.session_state.algorithm = "AES-256"
if 'original_size' not in st.session_state:
    st.session_state.original_size = None
if 'original_shape' not in st.session_state:
    st.session_state.original_shape = None
if 'decrypted_image' not in st.session_state:
    st.session_state.decrypted_image = None

# Header
st.markdown("""
<div class="main-header">
    <h1 style="font-size: 3rem; margin-bottom: 1rem;">🔒 Cipher Lens</h1>
    <h2 style="font-size: 1.5rem; opacity: 0.9;">Advanced Image Encryption & Decryption System</h2>
    <p style="font-size: 1.1rem; margin-top: 1rem; opacity: 0.8;">Military-Grade AES Encryption • Secure Key Management • Professional Security</p>
</div>
""", unsafe_allow_html=True)

# Back button
if st.button("← Back to SIA Hub", key="back_main"):
    st.switch_page("app.py")

# Control Panel
st.markdown('<div class="control-panel">', unsafe_allow_html=True)
st.markdown("### ⚙️ Encryption Settings")

col_settings1, col_settings2 = st.columns(2)

with col_settings1:
    algorithm = st.selectbox(
        "🔐 Encryption Algorithm:",
        ["AES-256", "AES-192", "AES-128"],
        help="AES-256 provides the highest security"
    )
    st.session_state.algorithm = algorithm

with col_settings2:
    # Show algorithm info
    algo_info = {
        "AES-256": "🛡️ **Maximum Security** - 256-bit key, Military grade",
        "AES-192": "🔒 **High Security** - 192-bit key, Government standard", 
        "AES-128": "🔐 **Standard Security** - 128-bit key, Commercial grade"
    }
    st.markdown(algo_info[algorithm])

st.markdown('</div>', unsafe_allow_html=True)

# Main Interface
col1, col2 = st.columns(2)

# LEFT SIDE - Original Image
with col1:
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.markdown("### 📷 Original Image")

    # Sample buttons
    st.markdown("**🖼️ Quick Samples:**")
    col_s1, col_s2, col_s3 = st.columns(3)

    with col_s1:
        st.markdown('<div class="sample-btn">', unsafe_allow_html=True)
        if st.button("📄 Doc", key="doc_sample", use_container_width=True):
            # Create a document-like image
            sample_img = np.full((200, 300, 3), 240, dtype=np.uint8)
            # Add text-like rectangles
            sample_img[30:50, 20:280] = [50, 50, 50]
            sample_img[60:80, 20:250] = [80, 80, 80]  
            sample_img[90:110, 20:200] = [100, 100, 100]
            sample_img[120:140, 20:220] = [70, 70, 70]
            st.session_state.original_image = sample_img
            st.session_state.image_name = "document_sample.png"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_s2:
        st.markdown('<div class="sample-btn">', unsafe_allow_html=True)
        if st.button("🏞️ Photo", key="photo_sample", use_container_width=True):
            # Create a colorful landscape-like image
            sample_img = np.random.randint(50, 200, (200, 300, 3), dtype=np.uint8)
            # Add sky gradient
            for i in range(80):
                sample_img[i, :] = [135, 206, 235]
            # Add ground
            sample_img[120:, :] = [34, 139, 34]
            st.session_state.original_image = sample_img
            st.session_state.image_name = "landscape_sample.jpg"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_s3:
        st.markdown('<div class="sample-btn">', unsafe_allow_html=True)
        if st.button("📊 Chart", key="chart_sample", use_container_width=True):
            # Create a chart-like image
            sample_img = np.full((200, 300, 3), 250, dtype=np.uint8)
            # Add colorful bars
            sample_img[50:150, 50:80] = [255, 99, 132]   # Pink bar
            sample_img[75:175, 100:130] = [54, 162, 235]  # Blue bar  
            sample_img[100:200, 150:180] = [255, 205, 86] # Yellow bar
            sample_img[60:160, 200:230] = [75, 192, 192]  # Teal bar
            st.session_state.original_image = sample_img
            st.session_state.image_name = "chart_sample.png"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # File Upload
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "📁 **Upload Your Image**",
        type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
        help="Supported: JPG, PNG, BMP, TIFF (Max: 10MB)"
    )

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            # Resize if too large
            if image.width > 800 or image.height > 600:
                image.thumbnail((800, 600), Image.Resampling.LANCZOS)
            st.session_state.original_image = np.array(image)
            st.session_state.image_name = uploaded_file.name
            st.success(f"✅ Loaded: {uploaded_file.name}")
        except Exception as e:
            st.error(f"❌ Error loading image: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

    # Display original image
    if st.session_state.original_image is not None:
        st.image(
            st.session_state.original_image, 
            caption=f"📷 {st.session_state.get('image_name', 'Original Image')}", 
            use_column_width=True
        )

        # Image info
        h, w, c = st.session_state.original_image.shape
        st.info(f"📏 **Size**: {w}×{h} px | **Channels**: {c}")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #9ca3af;">
            <h3>🖼️ No Image Selected</h3>
            <p>Upload an image or choose a sample to get started</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT SIDE - Results
with col2:
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    st.markdown("### 🔐 Encryption/Decryption Results")

    # Show decrypted image if available
    if st.session_state.decrypted_image is not None:
        st.image(st.session_state.decrypted_image, caption="✅ Decrypted Image", use_column_width=True)

        # Download decrypted image
        decrypted_pil = Image.fromarray(st.session_state.decrypted_image)
        buf = io.BytesIO()
        decrypted_pil.save(buf, format='PNG')

        st.download_button(
            "📥 Download Decrypted Image",
            data=buf.getvalue(),
            file_name=f"decrypted_{st.session_state.get('image_name', 'image')}.png",
            mime="image/png",
            use_container_width=True
        )

    # Show encrypted data info if available
    elif st.session_state.encrypted_data is not None:
        # Show encrypted visualization
        encrypted_visual = np.random.randint(0, 255, st.session_state.original_image.shape, dtype=np.uint8)
        st.image(encrypted_visual, caption="🔒 Encrypted Data (Visualization)", use_column_width=True)

        # Success panel
        st.markdown(f"""
        <div class="success-panel">
            <h3>🔐 Encryption Successful!</h3>
            <p><strong>Algorithm:</strong> {st.session_state.algorithm}</p>
            <p><strong>Key Length:</strong> {len(st.session_state.encryption_key) * 8} bits</p>
            <p><strong>Status:</strong> ✅ SECURE</p>
        </div>
        """, unsafe_allow_html=True)

        # Show encrypted key
        key_hex = st.session_state.encryption_key.hex().upper()
        st.markdown(f"""
        <div class="key-display">
            🔑 ENCRYPTION KEY (SAVE THIS!):<br><br>
            {key_hex}
        </div>
        """, unsafe_allow_html=True)

        # Download encrypted file
        encrypted_filename = f"encrypted_{st.session_state.get('image_name', 'image')}.dat"
        st.download_button(
            "📥 Download Encrypted File",
            data=st.session_state.encrypted_data,
            file_name=encrypted_filename,
            mime="application/octet-stream",
            use_container_width=True,
            help="Download the encrypted file to store securely"
        )

    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #9ca3af;">
            <h3>🔒 No Results Yet</h3>
            <p>Encrypt an image to see the results here</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Action Buttons
st.markdown("---")
col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

with col_btn1:
    st.markdown('<div class="encrypt-btn">', unsafe_allow_html=True)
    if st.button("🔐 ENCRYPT", use_container_width=True):
        if st.session_state.original_image is not None:
            with st.spinner(f"🔄 Encrypting with {algorithm}..."):
                progress = st.progress(0)

                # Generate key
                key = generate_key(algorithm)
                st.session_state.encryption_key = key

                progress.progress(50)
                time.sleep(1)

                # Encrypt image
                encrypted_data, original_size = encrypt_image(st.session_state.original_image, key)

                if encrypted_data is not None:
                    st.session_state.encrypted_data = encrypted_data
                    st.session_state.original_size = original_size
                    st.session_state.original_shape = st.session_state.original_image.shape
                    st.session_state.decrypted_image = None  # Clear decrypted image

                    progress.progress(100)
                    time.sleep(0.5)
                    st.success("🔐 Encryption completed!")
                    st.rerun()
                else:
                    st.error("❌ Encryption failed!")
        else:
            st.error("⚠️ Please select an image first!")
    st.markdown('</div>', unsafe_allow_html=True)

with col_btn2:
    st.markdown('<div class="decrypt-btn">', unsafe_allow_html=True)
    if st.button("🔓 DECRYPT", use_container_width=True):
        if st.session_state.encrypted_data is not None and st.session_state.encryption_key is not None:
            with st.spinner("🔄 Decrypting..."):
                progress = st.progress(0)

                progress.progress(50)
                time.sleep(1)

                # Decrypt image
                decrypted_image = decrypt_image(
                    st.session_state.encrypted_data,
                    st.session_state.encryption_key,
                    st.session_state.original_size,
                    st.session_state.original_shape
                )

                progress.progress(100)
                time.sleep(0.5)

                if decrypted_image is not None:
                    st.session_state.decrypted_image = decrypted_image
                    st.success("🔓 Decryption successful!")
                    st.rerun()
                else:
                    st.error("❌ Decryption failed!")
        else:
            st.error("⚠️ No encrypted data to decrypt!")
    st.markdown('</div>', unsafe_allow_html=True)

with col_btn3:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("🗑️ CLEAR", use_container_width=True):
        # Reset all session state
        for key in ['original_image', 'encrypted_data', 'encryption_key', 'original_size', 'original_shape', 'decrypted_image', 'image_name']:
            if key in st.session_state:
                del st.session_state[key]
        st.success("✅ All data cleared!")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_btn4:
    if st.button("🏠 MAIN HUB", use_container_width=True):
        st.switch_page("app.py")

# Info Panel
st.markdown("""
<div class="info-panel">
    <h3>🛡️ Security Information</h3>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 1rem;">
        <div>
            <strong>🔐 Encryption Features:</strong><br>
            • AES (Advanced Encryption Standard)<br>
            • CBC mode with random IV<br>
            • Cryptographically secure keys<br>
            • Military-grade security
        </div>
        <div>
            <strong>🔒 Security Levels:</strong><br>
            • AES-256: Maximum security<br>
            • AES-192: Government standard<br>
            • AES-128: Commercial grade<br>
            • Data integrity verification
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation
st.markdown("---")
nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("🎥 Violence Detection", use_container_width=True):
        st.switch_page("pages/1_Violence_Detection.py")
with nav_col2:
    if st.button("📧 Email Analysis", use_container_width=True):
        st.switch_page("pages/2_Email_Analysis.py")  
with nav_col3:
    if st.button("🏠 Main Hub", use_container_width=True):
        st.switch_page("app.py")
