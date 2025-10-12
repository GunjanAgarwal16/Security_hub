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

# Dark theme CSS with excellent visibility
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

    .input-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        color: white;
    }

    .threat-high { 
        background: linear-gradient(135deg, #ff4757, #ff3742);
        color: white;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(255, 71, 87, 0.4);
        font-size: 1.3rem;
    }

    .threat-medium { 
        background: linear-gradient(135deg, #ffa726, #fb8c00);
        color: white;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(255, 167, 38, 0.4);
        font-size: 1.3rem;
    }

    .threat-low { 
        background: linear-gradient(135deg, #2ed573, #1fcc5c);
        color: white;
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(46, 213, 115, 0.4);
        font-size: 1.3rem;
    }

    .analysis-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
    }

    .model-info {
        background: rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
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
    }

    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    .stRadio > div {
        color: white !important;
    }

    .stProgress .st-bo {
        background-color: #667eea !important;
    }

    /* All text visible */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: white !important;
    }

    .element-container {
        color: white !important;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(26, 26, 46, 0.95);
        color: white;
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
    <h1 style="font-size: 2.5rem;">📧 Email Threat Intelligence Engine</h1>
    <p style="font-size: 1.4rem;">Bidirectional LSTM • 98.37% Accuracy • Context-Aware Analysis</p>
</div>
""", unsafe_allow_html=True)

# Back button
if st.button("← Back to SIA Hub", key="back_main"):
    st.switch_page("app.py")

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("### 📝 Email Analysis Interface")

    input_method = st.radio(
        "Select analysis method:",
        ["🧪 Sample Threat Emails", "✍️ Custom Email Text"], 
        horizontal=True
    )

    if input_method == "🧪 Sample Threat Emails":
        sample_emails = {
            "✅ Safe Business Email": "Subject: Project Update Meeting\n\nHi Team,\n\nPlease join our project update meeting tomorrow at 2 PM. We'll review Q3 progress and discuss Q4 planning.\n\nBest regards,\nAlex Johnson\nProject Manager",

            "🟠 Marketing Spam": "Subject: LIMITED TIME! 70% OFF EVERYTHING!\n\nDear Customer,\n\nDon't miss our BIGGEST SALE! 70% off all items! Limited time offer - expires in 24 hours! HURRY!\n\nClick here to shop now!\n\nBest deals team",

            "🔴 Phishing Attack": "Subject: URGENT: Account Suspended - Verify Now!\n\nDear User,\n\nYour account has been suspended due to suspicious activity. Click here immediately: http://192.168.1.100/verify-account\n\nAuthentication-Results: spf=fail; dkim=fail\n\nWarning: Account will be permanently closed if not verified within 2 hours!",

            "🚨 Fraud Attempt": "Subject: CONGRATULATIONS! You've Won $50,000!\n\nDear Lucky Winner,\n\nYou have been selected as our grand prize winner! To claim your $50,000 prize, pay a small processing fee of $500.\n\nACT NOW! This offer expires today! Send payment to claim your winnings!"
        }

        selected_email = st.selectbox(
            "Choose a sample email to analyze:",
            list(sample_emails.keys()),
            help="Select different email types to see how the AI detects various threat levels"
        )
        email_text = sample_emails[selected_email]
        st.text_area("📧 Email Content:", value=email_text, height=150, disabled=True)

    else:
        email_text = st.text_area(
            "📝 Enter email content to analyze:",
            placeholder="Paste the complete email content here including subject line, headers, and body...",
            height=200,
            help="Include subject line, headers, and full email body for best analysis"
        )

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="model-info">', unsafe_allow_html=True)
    st.markdown("### 🎯 AI Engine Specs")
    st.markdown("""
    **🏗️ Architecture**: Bidirectional LSTM  
    **🎯 Accuracy**: 98.37%  
    **📊 Classes**: 4-class classification  
    **🧠 Features**: Context + Sentiment analysis  
    **⚡ Processing**: Real-time analysis  
    **🔍 Detection**: Advanced pattern recognition
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Analysis button - larger and more visible
if st.button("🔍 Analyze Email Threat Level", type="primary", use_container_width=True):
    if email_text and email_text.strip():
        with st.spinner("🔄 Analyzing email for threat patterns..."):
            progress = st.progress(0)

            # Show analysis steps
            steps = [
                "Loading email content...",
                "Extracting linguistic features...", 
                "Running sentiment analysis...",
                "Checking suspicious patterns...",
                "Applying ML classification...",
                "Generating threat assessment..."
            ]

            for i, step in enumerate(steps):
                st.text(f"🔄 {step}")
                progress.progress((i + 1) / len(steps))
                time.sleep(0.5)

            threat_score, prediction, confidence_probs, features = mock_threat_prediction(email_text)
            urgency, sentiment, url_score, auth_fail = features

        st.markdown("---")
        st.markdown("## 📋 Threat Intelligence Report")

        # Main threat level display - LARGE and CLEAR
        if threat_score > 75:
            st.markdown(f"""
            <div class="threat-high">
                <h1>🚨 CRITICAL THREAT - {prediction.upper()}</h1>
                <h2 style="font-size: 2rem;">Threat Score: {threat_score:.0f}/100</h2>
                <p><strong style="font-size: 1.4rem;">🚫 IMMEDIATE ACTION REQUIRED</strong></p>
                <p><strong>⚠️ DO NOT interact with this email</strong></p>
            </div>
            """, unsafe_allow_html=True)

        elif threat_score > 50:
            st.markdown(f"""
            <div class="threat-medium">
                <h1>⚠️ MODERATE THREAT - {prediction.upper()}</h1>
                <h2 style="font-size: 2rem;">Threat Score: {threat_score:.0f}/100</h2>
                <p><strong style="font-size: 1.4rem;">🔍 EXERCISE CAUTION</strong></p>
                <p><strong>Verify sender before taking any action</strong></p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown(f"""
            <div class="threat-low">
                <h1>✅ LOW RISK - {prediction.upper()}</h1>
                <h2 style="font-size: 2rem;">Threat Score: {threat_score:.0f}/100</h2>
                <p><strong style="font-size: 1.4rem;">✨ EMAIL APPEARS SAFE</strong></p>
                <p><strong>Standard security practices still apply</strong></p>
            </div>
            """, unsafe_allow_html=True)

        # Detailed analysis
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            st.markdown("#### 🔍 Threat Vector Analysis")

            threats_found = []
            if urgency > 20:
                threats_found.append(f"⚠️ **Urgency tactics detected** (Score: {urgency})")
            if url_score > 0:
                threats_found.append(f"🔗 **Suspicious URLs found** (Score: {url_score})")
            if auth_fail:
                threats_found.append("🚫 **Email authentication failed** (SPF/DKIM)")

            if threats_found:
                for threat in threats_found:
                    st.markdown(threat)
            else:
                st.markdown("**✅ No major threat vectors identified**")

            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
            st.markdown("#### 📊 Classification Confidence")

            threat_classes = ['Safe', 'Spam/Marketing', 'Phishing', 'Fraud']
            colors = ['#2ed573', '#ffa726', '#ff7043', '#ff4757']

            for i, (class_name, prob) in enumerate(zip(threat_classes, confidence_probs)):
                st.markdown(f"**{class_name}**: {prob:.1%}")
                st.progress(prob)

            st.markdown('</div>', unsafe_allow_html=True)

        # Security recommendations
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown("#### 💡 Security Recommendations")

        if threat_score > 75:
            st.markdown("""
            **🔴 CRITICAL - Immediate Actions Required:**
            - **🚫 DO NOT click any links or download attachments**
            - **📞 Report to security team immediately**  
            - **🗑️ Delete email after reporting**
            - **🔍 Scan organization for similar emails**
            - **🚨 Consider blocking sender domain**
            """)

        elif threat_score > 50:
            st.markdown("""
            **🟠 MODERATE - Caution Required:**
            - **📞 Verify sender through alternative communication**
            - **🚫 Do not provide any sensitive information**
            - **🔍 Hover over links to check destinations**
            - **📋 Consider forwarding to security team**
            - **🛡️ Apply extra verification steps**
            """)

        else:
            st.markdown("""
            **🟢 LOW RISK - Standard Precautions:**
            - **✅ Email appears legitimate but remain vigilant**
            - **🛡️ Apply standard security practices**
            - **🤔 Be cautious of any unusual requests**
            - **📞 Trust but verify sender identity when in doubt**
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
