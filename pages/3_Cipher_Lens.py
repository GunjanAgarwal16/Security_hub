import streamlit as st
import numpy as np
from PIL import Image
import io
import time
import os
import secrets
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Page config
st.set_page_config(
    page_title="Cipher Lens - SIA Hub",
    page_icon="🔒",
    layout="wide"
)

# Clean, beautiful theme
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: white;
    }

    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }

    .upload-section {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
    }

    .result-section {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        min-height: 400px;
    }

    .action-buttons {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0 0.5rem 0;  /* Reduced bottom margin to remove blank space */
    }

    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        margin: 0.25rem 0 !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }

    .encrypt-button button {
        background: linear-gradient(45deg, #e74c3c, #c0392b) !important;
    }

    .decrypt-button button {
        background: linear-gradient(45deg, #3498db, #2980b9) !important;
    }

    .clear-button button {
        background: linear-gradient(45deg, #95a5a6, #7f8c8d) !important;
    }

    .success-alert {
        background: linear-gradient(135deg, #27ae60, #219653);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
    }

    .key-display {
        background: rgba(0, 0, 0, 0.4);
        border: 2px solid #f39c12;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        color: #f39c12;
        word-break: break-all;
        text-align: center;
    }

    .stFileUploader > div {
        background-color: rgba(102, 126, 234, 0.1) !important;
        border: 2px dashed rgba(102, 126, 234, 0.5) !important;
        border-radius: 10px !important;
        padding: 1.5rem !important;
    }

    .stImage > img {
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: white !important;
    }

    .css-1d391kg {
        background: rgba(26, 26, 46, 0.95);
        color: white;
    }

    /* Hide Streamlit warnings */
    .stAlert {
        display: none;
    }

    /* Fix file uploader styling */
    .uploadedFile {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# FIXED encryption/decryption functions
def encrypt_image_data(image_array):
    """FIXED AES-256 encryption with proper data handling"""
    try:
        key = os.urandom(32)
        img_bytes = image_array.tobytes()

        # Pad data
        padding = 16 - (len(img_bytes) % 16)
        padded = img_bytes + bytes([padding]) * padding

        # Encrypt
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted = encryptor.update(padded) + encryptor.finalize()

        # Return all needed info for decryption
        return {
            'key': key,
            'encrypted_data': iv + encrypted,
            'original_size': len(img_bytes),
            'original_shape': image_array.shape,
            'dtype': str(image_array.dtype)
        }
    except Exception as e:
        st.error(f"Encryption error: {str(e)}")
        return None

def decrypt_image_data(encryption_info):
    """FIXED AES-256 decryption with proper error handling"""
    try:
        key = encryption_info['key']
        encrypted_data = encryption_info['encrypted_data']
        original_size = encryption_info['original_size']
        original_shape = encryption_info['original_shape']

        # Extract IV and encrypted bytes
        iv = encrypted_data[:16]
        encrypted_bytes = encrypted_data[16:]

        # Decrypt
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_bytes) + decryptor.finalize()

        # Remove padding
        padding_length = padded_data[-1]
        original_data = padded_data[:-padding_length]

        # Ensure we have the exact original size
        original_data = original_data[:original_size]

        # Convert back to image array
        decrypted_array = np.frombuffer(original_data, dtype=np.uint8)
        decrypted_image = decrypted_array.reshape(original_shape)

        return decrypted_image
    except Exception as e:
        st.error(f"Decryption error: {str(e)}")
        return None

# Initialize session state with FIXED structure
if 'image' not in st.session_state:
    st.session_state.image = None
if 'encryption_info' not in st.session_state:
    st.session_state.encryption_info = None
if 'decrypted' not in st.session_state:
    st.session_state.decrypted = None
if 'image_name' not in st.session_state:
    st.session_state.image_name = ""

# Title
st.markdown("""
<div class="main-title">
    <h1>🔒 Cipher Lens</h1>
    <p>Secure Image Encryption • AES-256 • No Configuration Required</p>
</div>
""", unsafe_allow_html=True)

# Back button
if st.button("← Back to SIA Hub", key="back"):
    st.switch_page("app.py")

# Step 1: Upload Image
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown("## 📤 Step 1: Upload Your Image")

uploaded = st.file_uploader(
    "Choose an image file",
    type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'],
    help="Supported: JPG, PNG, BMP, TIFF"
)

if uploaded:
    try:
        image = Image.open(uploaded)
        if image.width > 800 or image.height > 600:
            image.thumbnail((800, 600), Image.Resampling.LANCZOS)

        st.session_state.image = np.array(image)
        st.session_state.image_name = uploaded.name

        st.image(image, caption=f"✅ Loaded: {uploaded.name}", width=400)
        st.success(f"Image ready: {image.width}×{image.height} pixels")

    except Exception as e:
        st.error(f"Error loading image: {str(e)}")

elif st.session_state.image is None:
    # Quick test buttons
    st.markdown("**Or try a sample:**")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📊 Sample Chart", use_container_width=True):
            # Create sample chart
            sample = np.full((200, 300, 3), 250, dtype=np.uint8)
            sample[50:100, 50:100] = [255, 100, 100]  # Red bar
            sample[60:140, 120:170] = [100, 255, 100]  # Green bar
            sample[80:180, 190:240] = [100, 100, 255]  # Blue bar

            st.session_state.image = sample
            st.session_state.image_name = 'sample_chart.png'
            st.rerun()

    with col2:
        if st.button("📄 Sample Document", use_container_width=True):
            # Create sample document
            sample = np.full((200, 300, 3), 240, dtype=np.uint8)
            sample[40:60, 40:260] = [50, 50, 50]  # Header
            sample[80:95, 40:200] = [100, 100, 100]  # Line 1
            sample[105:120, 40:220] = [100, 100, 100]  # Line 2
            sample[135:150, 40:180] = [100, 100, 100]  # Line 3

            st.session_state.image = sample
            st.session_state.image_name = 'sample_doc.png'
            st.rerun()

# Show currently loaded image
if st.session_state.image is not None and uploaded is None:
    st.image(
        st.session_state.image, 
        caption=f"Current: {st.session_state.image_name}", 
        width=400
    )

st.markdown('</div>', unsafe_allow_html=True)

# Step 2: Action Buttons - FIXED spacing
if st.session_state.image is not None:
    st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
    st.markdown("## ⚡ Step 2: Choose Action")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="encrypt-button">', unsafe_allow_html=True)
        if st.button("🔐 ENCRYPT", use_container_width=True):
            with st.spinner("Encrypting with AES-256..."):
                progress = st.progress(0)

                # FIXED encryption
                encryption_info = encrypt_image_data(st.session_state.image)

                progress.progress(50)
                time.sleep(0.5)

                if encryption_info:
                    st.session_state.encryption_info = encryption_info
                    st.session_state.decrypted = None  # Clear previous decryption

                    progress.progress(100)
                    st.success("🔐 Encryption completed!")
                    st.rerun()
                else:
                    st.error("Encryption failed!")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="decrypt-button">', unsafe_allow_html=True)
        if st.button("🔓 DECRYPT", use_container_width=True):
            if st.session_state.encryption_info:
                with st.spinner("Decrypting..."):
                    progress = st.progress(0)

                    progress.progress(50)
                    time.sleep(0.5)

                    # FIXED decryption
                    decrypted_image = decrypt_image_data(st.session_state.encryption_info)

                    progress.progress(100)

                    if decrypted_image is not None:
                        st.session_state.decrypted = decrypted_image
                        st.success("🔓 Decryption successful!")
                        st.rerun()
                    else:
                        st.error("Decryption failed!")
            else:
                st.error("No encrypted data to decrypt! Please encrypt an image first.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="clear-button">', unsafe_allow_html=True)
        if st.button("🗑️ CLEAR", use_container_width=True):
            st.session_state.image = None
            st.session_state.encryption_info = None
            st.session_state.decrypted = None
            st.session_state.image_name = ""
            st.success("Cleared all data!")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        if st.button("🏠 HOME", use_container_width=True):
            st.switch_page("app.py")

    st.markdown('</div>', unsafe_allow_html=True)

# Step 3: Results - FIXED spacing
st.markdown('<div class="result-section">', unsafe_allow_html=True)
st.markdown("## 📋 Step 3: Results")

# Show decrypted image
if st.session_state.decrypted is not None:
    st.image(st.session_state.decrypted, caption="✅ Decrypted Image", width=400)

    st.markdown("""
    <div class="success-alert">
        <h4>🔓 Decryption Successful!</h4>
        <p>Your original image has been perfectly restored!</p>
    </div>
    """, unsafe_allow_html=True)

    # Download decrypted
    img_pil = Image.fromarray(st.session_state.decrypted.astype(np.uint8))
    buf = io.BytesIO()
    img_pil.save(buf, format='PNG')

    st.download_button(
        "📥 Download Decrypted Image",
        data=buf.getvalue(),
        file_name=f"decrypted_{st.session_state.image_name}",
        mime="image/png",
        use_container_width=True
    )

# Show encrypted info
elif st.session_state.encryption_info is not None:
    # Show scrambled visualization
    if st.session_state.image is not None:
        scrambled = np.random.randint(0, 255, st.session_state.image.shape, dtype=np.uint8)
        st.image(scrambled, caption="🔒 Encrypted (Scrambled Visualization)", width=400)

    st.markdown("""
    <div class="success-alert">
        <h4>🔐 Encryption Successful!</h4>
        <p>Your image is now secured with military-grade AES-256 encryption!</p>
    </div>
    """, unsafe_allow_html=True)

    # Show key
    key_hex = st.session_state.encryption_info['key'].hex().upper()
    st.markdown(f"""
    <div class="key-display">
        <strong>🔑 ENCRYPTION KEY - SAVE THIS!</strong><br>
        {key_hex}
    </div>
    """, unsafe_allow_html=True)

    # Download encrypted file
    st.download_button(
        "📥 Download Encrypted File",
        data=st.session_state.encryption_info['encrypted_data'],
        file_name=f"encrypted_{st.session_state.image_name}.dat",
        mime="application/octet-stream",
        use_container_width=True
    )

else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; color: #888;">
        <h4>🔒 No Results Yet</h4>
        <p>Upload an image and encrypt it to see results here</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Info footer
st.markdown("---")
st.info("🛡️ **Security**: AES-256 encryption with CBC mode • Random keys • Military-grade protection")

# Navigation
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🎥 Violence Detection", use_container_width=True):
        st.switch_page("pages/1_Violence_Detection.py")
with col2:
    if st.button("📧 Email Analysis", use_container_width=True):
        st.switch_page("pages/2_Email_Analysis.py")
with col3:
    if st.button("🏠 Main Hub", use_container_width=True):
        st.switch_page("app.py")
