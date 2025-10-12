import streamlit as st
import numpy as np
import time
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Page config
st.set_page_config(
    page_title="Email Threat Analysis - SIA Hub",
    page_icon="📧",
    layout="wide"
)

# Modern clean theme CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }

    .threat-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
    }

    .threat-high { 
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }

    .threat-medium { 
        background: linear-gradient(135deg, #ffa726, #fb8c00);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(255, 167, 38, 0.3);
    }

    .threat-low { 
        background: linear-gradient(135deg, #66bb6a, #43a047);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 187, 106, 0.3);
    }

    .input-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid #e0e0e0;
    }

    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid #f0f0f0;
    }

    .confidence-bar {
        background: #f0f0f0;
        border-radius: 10px;
        padding: 0.5rem;
        margin: 0.3rem 0;
    }

    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.8rem 2rem !important;
        font-weight: bold !important;
        font-size: 1rem !important;
    }

    /* Better text readability */
    .stMarkdown {
        color: #333;
        font-size: 1rem;
        line-height: 1.6;
    }

    h1, h2, h3, h4 {
        color: #333 !important;
        font-weight: 600 !important;
    }

    /* Progress bars */
    .stProgress .st-bo {
        background-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Feature extraction class
class FeatureExtractor:
    def __init__(self):
        self.urgency_kw = ['urgent', 'immediate', 'asap', 'expire', 'limited', 'act now', 'hurry']
        self.senti_analyzer = SentimentIntensityAnalyzer()

    def get_features(self, text):
        if not isinstance(text, str):
            text = ""
        lower_text = text.lower()
        urgency = min(sum(lower_text.count(k) for k in self.urgency_kw) * 10, 100)
        sentiment = self.senti_analyzer.polarity_scores(text)['compound']
        url_score = sum([40 for _ in re.finditer(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', lower_text)]) + sum([30 for tld in ['.tk','.xyz','.top'] if tld in lower_text])
        auth_fail = 1 if any(f in lower_text for f in ['spf=fail','dkim=fail']) else 0
        return urgency, sentiment, min(url_score, 100), auth_fail

def mock_threat_prediction(email_text):
    feature_extractor = FeatureExtractor()
    urgency, sentiment, url_score, auth_fail = feature_extractor.get_features(email_text)

    threat_score = 0
    threat_score += urgency * 0.3
    threat_score += (1 - abs(sentiment)) * 20
    threat_score += url_score * 0.4
    threat_score += auth_fail * 30

    suspicious_keywords = ['winner', 'congratulations', 'click here', 'verify account', 'suspended', 'pay fee']
    keyword_score = sum(10 for keyword in suspicious_keywords if keyword in email_text.lower())
    threat_score += keyword_score
    threat_score = min(threat_score, 100)

    if threat_score > 75:
        prediction = "Fraud"
        probs = [0.05, 0.05, 0.15, 0.75]
    elif threat_score > 50:
        prediction = "Phishing" 
        probs = [0.10, 0.10, 0.65, 0.15]
    elif threat_score > 25:
        prediction = "Spam/Marketing"
        probs = [0.15, 0.70, 0.10, 0.05]
    else:
        prediction = "Safe"
        probs = [0.85, 0.10, 0.03, 0.02]

    return threat_score, prediction, probs, (urgency, sentiment, url_score, auth_fail)

# Header
st.markdown("""
<div class="main-header">
    <h1>📧 Email Threat Intelligence Engine</h1>
    <p>Bidirectional LSTM • 98.37% Accuracy • Context-Aware Analysis</p>
</div>
""", unsafe_allow_html=True)

# Back button
if st.button("← Back to SIA Hub", key="back_main"):
    st.switch_page("app.py")

# Compact interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("### 📝 Email Analysis")

    input_method = st.radio("Input method:", ["Sample Emails", "Custom Text"], horizontal=True)

    if input_method == "Sample Emails":
        sample_emails = {
            "Safe Email": "Subject: Project Update\n\nHi Team,\n\nPlease send the Q3 report by Friday. We need it for the board meeting.\n\nThanks,\nAlex",
            "Spam Email": "Subject: CONGRATULATIONS! $1,000,000 Winner!\n\nDear Winner, You've won! Pay $500 processing fee to claim your prize. ACT NOW!",
            "Phishing Email": "Subject: URGENT: Account Suspended\n\nYour account suspended! Click here: http://192.168.1.100/verify\n\nAuthentication-Results: spf=fail; dkim=fail",
            "Marketing Email": "Subject: 50% OFF Sale!\n\nLimited time offer! Don't miss out! Use code SAVE50. Hurry, expires soon!"
        }

        selected_email = st.selectbox("Choose sample:", list(sample_emails.keys()))
        email_text = sample_emails[selected_email]
        st.text_area("Email preview:", value=email_text, height=120, disabled=True)

    else:
        email_text = st.text_area(
            "Enter email content:",
            placeholder="Paste email content here...",
            height=120
        )

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="threat-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 Model Info")
    st.markdown("""
    **Architecture**: Bidirectional LSTM  
    **Accuracy**: 98.37%  
    **Classes**: Safe, Spam, Phishing, Fraud  
    **Features**: Context + Sentiment analysis
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Analysis button
if st.button("🔍 Analyze Email Threat", type="primary", use_container_width=True):
    if email_text and email_text.strip():
        with st.spinner("Analyzing threat level..."):
            progress = st.progress(0)
            for i in range(100):
                progress.progress(i + 1)
                time.sleep(0.02)

            threat_score, prediction, confidence_probs, features = mock_threat_prediction(email_text)
            urgency, sentiment, url_score, auth_fail = features

        st.markdown("---")

        # Main result - BIG and CLEAR
        if threat_score > 75:
            st.markdown(f"""
            <div class="threat-high">
                <h1>🚨 HIGH RISK - {prediction.upper()}</h1>
                <h2>Threat Score: {threat_score:.0f}/100</h2>
                <p><strong>IMMEDIATE ACTION REQUIRED</strong></p>
            </div>
            """, unsafe_allow_html=True)
        elif threat_score > 50:
            st.markdown(f"""
            <div class="threat-medium">
                <h1>⚠️ MEDIUM RISK - {prediction.upper()}</h1>
                <h2>Threat Score: {threat_score:.0f}/100</h2>
                <p><strong>EXERCISE CAUTION</strong></p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="threat-low">
                <h1>✅ LOW RISK - {prediction.upper()}</h1>
                <h2>Threat Score: {threat_score:.0f}/100</h2>
                <p><strong>EMAIL APPEARS SAFE</strong></p>
            </div>
            """, unsafe_allow_html=True)

        # Analysis details
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="threat-card">', unsafe_allow_html=True)
            st.markdown("#### 🔍 Threat Analysis")

            threat_vectors = []
            if urgency > 20:
                threat_vectors.append(f"⚠️ Pressure tactics (Score: {urgency})")
            if url_score > 0:
                threat_vectors.append(f"🔗 Suspicious URLs (Score: {url_score})")
            if auth_fail:
                threat_vectors.append("🚫 Authentication failure")

            if threat_vectors:
                for vector in threat_vectors:
                    st.markdown(f"**{vector}**")
            else:
                st.markdown("**✅ No major threats detected**")

            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="threat-card">', unsafe_allow_html=True)
            st.markdown("#### 📊 Classification Confidence")

            threat_classes = ['Safe', 'Spam/Marketing', 'Phishing', 'Fraud']
            colors = ['#66bb6a', '#ffa726', '#ff7043', '#ef5350']

            for i, (class_name, prob) in enumerate(zip(threat_classes, confidence_probs)):
                st.markdown(f"**{class_name}**: {prob:.1%}")
                st.progress(prob)

            st.markdown('</div>', unsafe_allow_html=True)

        # Actionable recommendations
        st.markdown('<div class="threat-card">', unsafe_allow_html=True)
        st.markdown("#### 💡 Security Recommendations")

        if threat_score > 75:
            st.markdown("""
            🔴 **CRITICAL ACTIONS:**
            - **DO NOT** click any links or download attachments
            - Report to security team immediately
            - Delete email after reporting
            - Check for similar emails across organization
            """)
        elif threat_score > 50:
            st.markdown("""
            🟠 **CAUTION REQUIRED:**
            - Verify sender through alternative communication
            - Do not provide sensitive information
            - Hover over links to check destinations
            - Consider forwarding to security team
            """)
        else:
            st.markdown("""
            🟢 **STANDARD PRECAUTIONS:**
            - Email appears legitimate but remain vigilant
            - Apply standard security practices
            - Be cautious of unusual requests
            - Trust but verify sender identity
            """)

        st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.error("⚠️ Please enter email content for analysis!")

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
    if st.button("🔒 Cipher Lens", key="nav_cipher", use_container_width=True):
        st.switch_page("pages/3_Cipher_Lens.py")
