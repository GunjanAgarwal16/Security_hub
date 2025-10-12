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

# Simple dark theme
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
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }

    .side-frame {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem;
        min-height: 500px;
        text-align: center;
        color: white;
    }

    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 1rem 2rem !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        width: 100% !important;
        margin: 0.5rem 0 !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
    }

    .encrypt-btn button {
        background: linear-gradient(45deg, #e74c3c, #c0392b) !important;
    }

    .decrypt-btn button {
        background: linear-gradient(45deg, #3498db, #2980b9) !important;
    }

    .download-btn button {
        background: linear-gradient(45deg, #27ae60, #219653) !important;
    }

    .clear-btn button {
        background: linear-gradient(45deg, #95a5a6, #7f8c8d) !important;
    }

    .key-box {
        background: rgba(0, 0, 0, 0.3);
        border: 2px solid #f39c12;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: monospace;
        font-size: 1.1rem;
        color: #f39c12;
        word-break: break-all;
    }

    .success-box {
        background: linear-gradient(135deg, #27ae60, #219653);
        color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }

    .stFileUploader > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 2px dashed rgba(102, 126, 234, 0.5) !important;
        border-radius: 10px !important;
        padding: 2rem !important;
    }

    .stImage > img {
        border-radius: 10px !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3) !important;
        max-height: 300px !important;
        max-width: 100% !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: white !important;
    }

    .css-1d391kg {
        background: rgba(26, 26, 46, 0.95);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Simple encryption functions
def auto_encrypt_image(image_data):
    """Auto encrypt with AES-256 - no user choice needed"""
    try:
        # Auto-select AES-256 for maximum security
        key = os.urandom(32)  # 256-bit key

        # Convert to bytes
        img_bytes = image_data.tobytes()

        # Pad data
        padding_length = 16 - (len(img_bytes) % 16)
        padded_data = img_bytes + bytes([padding_length]) * padding_length

        # Encrypt with random IV
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        return key, iv + encrypted_data, len(img_bytes)
    except Exception as e:
        return None, None, None

def auto_decrypt_image(key, encrypted_data, original_size, shape):
    """Auto decrypt the image"""
    try:
        # Extract IV and data
        iv = encrypted_data[:16]
        encrypted_bytes = encrypted_data[16:]

        # Decrypt
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_bytes) + decryptor.finalize()

        # Remove padding
        padding_length = padded_data[-1]
        original_data = padded_data[:-padding_length]
        original_data = original_data[:original_size]

        # Convert back to image
        decrypted_array = np.frombuffer(original_data, dtype=np.uint8)
        return decrypted_array.reshape(shape)
    except Exception as e:
        return None

# Initialize simple session state
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'encrypted_data' not in st.session_state:
    st.session_state.encrypted_data = None
if 'encryption_key' not in st.session_state:
    st.session_state.encryption_key = None
if 'decrypted_image' not in st.session_state:
    st.session_state.decrypted_image = None
if 'image_info' not in st.session_state:
    st.session_state.image_info = {}

# Header
st.markdown("""
<div class="main-header">
    <h1>🔒 Cipher Lens - Simple Image Encryption</h1>
    <p>Automatic AES-256 Encryption • No Configuration Needed • Just Upload & Encrypt</p>
</div>
""", unsafe_allow_html=True)

# Back button
if st.button("← Back to SIA Hub", key="back_main"):
    st.switch_page("app.py")

# Two simple columns - exactly what you want
col1, col2 = st.columns(2)

# LEFT SIDE - Original Image
with col1:
    st.markdown('<div class="side-frame">', unsafe_allow_html=True)
    st.markdown("### 📷 Original Image")

    # Simple file upload - image shows IMMEDIATELY when uploaded
    uploaded_file = st.file_uploader(
        "📁 Upload Image Here",
        type=['jpg', 'jpeg', 'png', 'bmp'],
        help="Choose any image file"
    )

    # IMMEDIATELY show uploaded image
    if uploaded_file is not None:
        try:
            # Load and show image RIGHT AWAY
            image = Image.open(uploaded_file)
            # Resize if too big
            if image.width > 600 or image.height > 400:
                image.thumbnail((600, 400), Image.Resampling.LANCZOS)

            # Convert to numpy and store
            st.session_state.original_image = np.array(image)
            st.session_state.image_info = {
                'name': uploaded_file.name,
                'size': f"{image.width}×{image.height}",
                'original_size': len(np.array(image).tobytes()),
                'shape': np.array(image).shape
            }

            # SHOW IMAGE IMMEDIATELY
            st.image(image, caption=f"✅ {uploaded_file.name}", use_column_width=True)
            st.success(f"📷 Image loaded: {st.session_state.image_info['size']} pixels")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.session_state.original_image = None

    # Show sample buttons if no image
    elif st.session_state.original_image is None:
        st.markdown("**🎯 Quick Test Images:**")

        col_s1, col_s2 = st.columns(2)

        with col_s1:
            if st.button("📄 Test Document", use_container_width=True):
                # Create test document
                test_img = np.full((300, 400, 3), 240, dtype=np.uint8)
                test_img[50:80, 50:350] = [50, 50, 50]  # Title
                test_img[100:120, 50:300] = [100, 100, 100]  # Line 1
                test_img[140:160, 50:320] = [100, 100, 100]  # Line 2
                test_img[180:200, 50:280] = [100, 100, 100]  # Line 3

                st.session_state.original_image = test_img
                st.session_state.image_info = {
                    'name': 'test_document.png',
                    'size': '400×300',
                    'original_size': len(test_img.tobytes()),
                    'shape': test_img.shape
                }
                st.rerun()

        with col_s2:
            if st.button("🏞️ Test Photo", use_container_width=True):
                # Create test photo
                test_img = np.random.randint(50, 200, (300, 400, 3), dtype=np.uint8)
                # Add sky
                for i in range(100):
                    test_img[i, :] = [135, 206, 235]
                # Add ground
                test_img[150:, :] = [34, 139, 34]

                st.session_state.original_image = test_img
                st.session_state.image_info = {
                    'name': 'test_photo.jpg',
                    'size': '400×300',
                    'original_size': len(test_img.tobytes()),
                    'shape': test_img.shape
                }
                st.rerun()

        st.markdown("""
        <div style="text-align: center; margin: 2rem 0; color: #bbb;">
            <h4>No Image Selected</h4>
            <p>Upload an image file above or use a test image</p>
        </div>
        """, unsafe_allow_html=True)

    # Show the stored image if we have one
    elif st.session_state.original_image is not None:
        st.image(
            st.session_state.original_image, 
            caption=f"📷 {st.session_state.image_info['name']}", 
            use_column_width=True
        )
        st.info(f"📏 Size: {st.session_state.image_info['size']} pixels")

    st.markdown('</div>', unsafe_allow_html=True)

# RIGHT SIDE - Results
with col2:
    st.markdown('<div class="side-frame">', unsafe_allow_html=True)
    st.markdown("### 🔐 Encryption/Decryption Results")

    # Show decrypted image if available
    if st.session_state.decrypted_image is not None:
        st.image(st.session_state.decrypted_image, caption="✅ Decrypted Image", use_column_width=True)
        st.markdown("""
        <div class="success-box">
            <h3>🔓 Decryption Successful!</h3>
            <p>Your image has been restored perfectly!</p>
        </div>
        """, unsafe_allow_html=True)

        # Download decrypted image
        decrypted_pil = Image.fromarray(st.session_state.decrypted_image.astype(np.uint8))
        buf = io.BytesIO()
        decrypted_pil.save(buf, format='PNG')

        st.markdown('<div class="download-btn">', unsafe_allow_html=True)
        st.download_button(
            "📥 Download Decrypted Image",
            data=buf.getvalue(),
            file_name=f"decrypted_{st.session_state.image_info.get('name', 'image')}.png",
            mime="image/png",
            use_column_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Show encrypted data info if available
    elif st.session_state.encrypted_data is not None:
        # Show encrypted visualization (scrambled pixels)
        encrypted_visual = np.random.randint(0, 255, st.session_state.original_image.shape, dtype=np.uint8)
        st.image(encrypted_visual, caption="🔒 Encrypted Data (Scrambled)", use_column_width=True)

        st.markdown("""
        <div class="success-box">
            <h3>🔐 Encryption Successful!</h3>
            <p>Your image is now securely encrypted with AES-256!</p>
        </div>
        """, unsafe_allow_html=True)

        # Show encryption key
        if st.session_state.encryption_key:
            key_hex = st.session_state.encryption_key.hex().upper()
            st.markdown(f"""
            <div class="key-box">
                🔑 <strong>SAVE THIS KEY!</strong><br><br>
                {key_hex}
            </div>
            """, unsafe_allow_html=True)

        # Download encrypted file
        st.markdown('<div class="download-btn">', unsafe_allow_html=True)
        st.download_button(
            "📥 Download Encrypted File",
            data=st.session_state.encrypted_data,
            file_name=f"encrypted_{st.session_state.image_info.get('name', 'image')}.dat",
            mime="application/octet-stream",
            use_column_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align: center; margin: 3rem 0; color: #bbb;">
            <h4>🔒 No Results Yet</h4>
            <p>Encrypt an image to see the encrypted results here</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Simple action buttons at bottom
st.markdown("---")
st.markdown("### 🎯 Actions")

col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

with col_btn1:
    st.markdown('<div class="encrypt-btn">', unsafe_allow_html=True)
    if st.button("🔐 ENCRYPT", use_container_width=True):
        if st.session_state.original_image is not None:
            with st.spinner("🔄 Encrypting with AES-256..."):
                progress = st.progress(0)

                # Auto encrypt (no user input needed)
                key, encrypted_data, original_size = auto_encrypt_image(st.session_state.original_image)

                progress.progress(50)
                time.sleep(1)

                if key is not None and encrypted_data is not None:
                    st.session_state.encryption_key = key
                    st.session_state.encrypted_data = encrypted_data
                    st.session_state.image_info['original_size'] = original_size
                    st.session_state.decrypted_image = None  # Clear decrypted

                    progress.progress(100)
                    st.success("🔐 Encryption completed!")
                    st.rerun()
                else:
                    st.error("❌ Encryption failed!")
        else:
            st.error("⚠️ Please upload an image first!")
    st.markdown('</div>', unsafe_allow_html=True)

with col_btn2:
    st.markdown('<div class="decrypt-btn">', unsafe_allow_html=True)
    if st.button("🔓 DECRYPT", use_container_width=True):
        if st.session_state.encrypted_data is not None and st.session_state.encryption_key is not None:
            with st.spinner("🔄 Decrypting..."):
                progress = st.progress(0)

                # Auto decrypt
                decrypted_image = auto_decrypt_image(
                    st.session_state.encryption_key,
                    st.session_state.encrypted_data,
                    st.session_state.image_info['original_size'],
                    st.session_state.image_info['shape']
                )

                progress.progress(50)
                time.sleep(1)

                if decrypted_image is not None:
                    st.session_state.decrypted_image = decrypted_image
                    progress.progress(100)
                    st.success("🔓 Decryption successful!")
                    st.rerun()
                else:
                    st.error("❌ Decryption failed!")
        else:
            st.error("⚠️ No encrypted data to decrypt!")
    st.markdown('</div>', unsafe_allow_html=True)

with col_btn3:
    st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
    if st.button("🗑️ CLEAR ALL", use_container_width=True):
        # Reset everything
        st.session_state.original_image = None
        st.session_state.encrypted_data = None
        st.session_state.encryption_key = None
        st.session_state.decrypted_image = None
        st.session_state.image_info = {}
        st.success("✅ Everything cleared!")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col_btn4:
    if st.button("🏠 MAIN HUB", use_container_width=True):
        st.switch_page("app.py")

# Simple info
st.markdown("---")
st.info("🛡️ **Auto-Security**: AES-256 encryption with random keys • No configuration needed • Maximum security guaranteed")

# Navigation
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
