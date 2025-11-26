import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
import io
from PIL import Image
import numpy as np
import os
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import json
import random
import logging
from datetime import datetime
import hashlib

# Configure logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Page config with enhanced settings
st.set_page_config(
    page_title="Sivamahendranath Ragimanu | AI Portfolio",
    page_icon="👨💻",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/yourusername',
        'Report a bug': 'mailto:mahendraragimanu2@gmail.com',
        'About': '# AI-Powered Portfolio\nVersion 2.0'
    }
)

# Security: Rate limiting storage
if 'form_submissions' not in st.session_state:
    st.session_state.form_submissions = []
if 'page_load_time' not in st.session_state:
    st.session_state.page_load_time = time.time()

def load_custom_css():
    """Enhanced CSS with proper Streamlit selectors"""
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=Poppins:wght@300;400;600;700&display=swap');
        
        /* ============ STREAMLIT APP BACKGROUND (FIXED) ============ */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #0f0c29);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }
        
        [data-testid="stApp"] {
            background: transparent;
        }
        
        [data-testid="stHeader"] {
            background: transparent;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* ============ MAIN CONTENT AREA ============ */
        [data-testid="stMainBlockContainer"] {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 100%;
        }
        
        section[data-testid="stMain"] {
            background: transparent;
            padding: 0rem 1rem;
        }
        
        /* ============ FLOATING PARTICLES EFFECT ============ */
        [data-testid="stAppViewContainer"]::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 107, 107, 0.12) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(78, 205, 196, 0.1) 0%, transparent 40%);
            animation: particleFloat 20s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes particleFloat {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(30px, -30px) scale(1.1); }
            66% { transform: translate(-20px, 20px) scale(0.9); }
        }
        
        /* ============ MORPHING BLOB ============ */
        [data-testid="stAppViewContainer"]::after {
            content: '';
            position: fixed;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(157, 78, 221, 0.08) 0%, transparent 70%);
            animation: blobMorph 25s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes blobMorph {
            0%, 100% { 
                border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%;
                transform: rotate(0deg) scale(1);
            }
            50% { 
                border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%;
                transform: rotate(180deg) scale(1.1);
            }
        }
        
        /* ============ ENSURE CONTENT IS VISIBLE ============ */
        [data-testid="stMainBlockContainer"] > div {
            position: relative;
            z-index: 1;
        }
        
        /* ============ TEXT COLOR ============ */
        .stMarkdown, p, h1, h2, h3, h4, h5, h6, span, div {
            color: #ffffff !important;
        }
        
        /* ============ GLASSMORPHISM TABS ============ */
        [data-testid="stTabs"] {
            position: relative;
            z-index: 10;
        }
        
        [data-testid="stTabs"] [data-baseweb="tab-list"] {
            gap: 1.5rem;
            animation: slideInDown 1s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            padding: 10px;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border-radius: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        @keyframes slideInDown {
            from {
                opacity: 0;
                transform: translateY(-100px) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        [data-testid="stTabs"] [data-baseweb="tab"] {
            height: 50px;
            padding: 14px 26px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 1.5px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            font-weight: 700;
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 1.05rem;
            letter-spacing: 0.5px;
            position: relative;
            overflow: hidden;
        }
        
        [data-testid="stTabs"] [data-baseweb="tab"]:hover {
            background: rgba(120, 119, 198, 0.2);
            transform: translateY(-5px) scale(1.05);
            box-shadow: 
                0 20px 40px rgba(120, 119, 198, 0.3),
                0 0 30px rgba(157, 78, 221, 0.2);
            border: 1.5px solid rgba(120, 119, 198, 0.6);
        }
        
        [data-testid="stTabs"] [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(120, 119, 198, 0.3), rgba(157, 78, 221, 0.3)) !important;
            border: 2px solid #7877c6 !important;
            box-shadow: 
                0 0 40px rgba(120, 119, 198, 0.6),
                inset 0 0 20px rgba(157, 78, 221, 0.3) !important;
            text-shadow: 0 0 20px rgba(120, 119, 198, 0.8);
            color: #fff !important;
            transform: scale(1.08);
        }
        
        /* Tab shimmer effect */
        [data-testid="stTabs"] [data-baseweb="tab"]::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -100%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent 30%,
                rgba(255, 255, 255, 0.2) 50%,
                transparent 70%
            );
            transform: rotate(45deg);
            animation: shimmerSlide 3s infinite;
        }
        
        @keyframes shimmerSlide {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        /* ============ ENHANCED GLASSMORPHISM CARDS ============ */
        .card-container {
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(25px) saturate(180%);
            -webkit-backdrop-filter: blur(25px) saturate(180%);
            border-radius: 25px;
            padding: 35px 25px;
            margin: 25px 0;
            box-shadow: 
                0 25px 60px rgba(0, 0, 0, 0.3),
                0 0 50px rgba(120, 119, 198, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
            overflow: hidden;
            border: 1.5px solid rgba(255, 255, 255, 0.15);
            position: relative;
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: cardSlideUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
        }
        
        @keyframes cardSlideUp {
            from {
                opacity: 0;
                transform: translateY(60px) scale(0.95);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        .card-container:hover {
            background: rgba(255, 255, 255, 0.12) !important;
            transform: translateY(-15px) scale(1.02);
            box-shadow: 
                0 35px 90px rgba(120, 119, 198, 0.3),
                0 0 60px rgba(157, 78, 221, 0.25),
                inset 0 2px 0 rgba(255, 255, 255, 0.3);
            border: 2px solid rgba(120, 119, 198, 0.4);
        }
        
        .card-container::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(157, 78, 221, 0.15) 0%, transparent 70%);
            transform: translate(-50%, -50%);
            animation: pulseGlow 4s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes pulseGlow {
            0%, 100% { opacity: 0.5; transform: translate(-50%, -50%) scale(1); }
            50% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
        }
        
        .card-container > * {
            position: relative;
            z-index: 1;
        }
        
        /* ============ GLOWING TEXT ============ */
        .glow-text {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #7877c6, #9d4edd, #4ecdc4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: textGlowPulse 3s ease-in-out infinite;
            font-weight: 900;
            display: inline-block;
        }
        
        @keyframes textGlowPulse {
            0%, 100% {
                filter: brightness(1) drop-shadow(0 0 20px rgba(120, 119, 198, 0.6));
            }
            50% {
                filter: brightness(1.3) drop-shadow(0 0 40px rgba(157, 78, 221, 0.8));
            }
        }
        
        /* ============ SKILL BADGES ============ */
        .skill-badge {
            display: inline-block;
            background: linear-gradient(135deg, rgba(120, 119, 198, 0.2), rgba(157, 78, 221, 0.2));
            border: 2px solid rgba(120, 119, 198, 0.4);
            padding: 12px 24px;
            border-radius: 30px;
            margin: 8px 10px;
            font-weight: 600;
            font-size: 1.05rem;
            color: #ffffff !important;
            box-shadow: 
                0 0 20px rgba(120, 119, 198, 0.3),
                inset 0 0 10px rgba(255, 255, 255, 0.1);
            transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
            animation: badgeFloat 3s ease-in-out infinite;
        }
        
        @keyframes badgeFloat {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-5px); }
        }
        
        .skill-badge:hover {
            background: linear-gradient(135deg, rgba(120, 119, 198, 0.4), rgba(157, 78, 221, 0.4));
            transform: scale(1.25) rotate(-3deg);
            box-shadow: 
                0 0 50px rgba(120, 119, 198, 0.8),
                inset 0 0 20px rgba(120, 119, 198, 0.3);
            border: 2px solid rgba(120, 119, 198, 0.9);
        }
        
        .skill-badge::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                45deg,
                transparent,
                rgba(255, 255, 255, 0.3),
                transparent
            );
            transform: rotate(45deg);
            transition: all 0.5s;
        }
        
        .skill-badge:hover::before {
            left: 100%;
        }
        
        /* ============ PROGRESS BARS ============ */
        .progress-bar-container {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            height: 15px;
            overflow: hidden;
            margin: 15px 0;
            border: 1px solid rgba(255, 255, 255, 0.15);
            position: relative;
            box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        
        .progress-bar-fill {
            background: linear-gradient(90deg, #7877c6, #9d4edd, #4ecdc4);
            height: 100%;
            border-radius: 15px;
            animation: progressFill 2s cubic-bezier(0.65, 0, 0.35, 1);
            box-shadow: 0 0 20px rgba(120, 119, 198, 0.6);
            position: relative;
            overflow: hidden;
        }
        
        @keyframes progressFill {
            from { width: 0; opacity: 0; }
            to { width: 90%; opacity: 1; }
        }
        
        /* ============ 3D IMAGE CONTAINERS ============ */
        .image-container {
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 
                0 20px 60px rgba(0, 0, 0, 0.5),
                0 0 40px rgba(120, 119, 198, 0.3);
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            max-width: 100%;
            height: auto;
            position: relative;
        }
        
        .image-container:hover {
            transform: translateY(-10px) scale(1.05);
            box-shadow: 
                0 30px 80px rgba(120, 119, 198, 0.5),
                0 0 60px rgba(157, 78, 221, 0.4);
        }
        
        .image-container img {
            width: 100%;
            height: auto;
            display: block;
            transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            filter: brightness(0.95);
        }
        
        .image-container:hover img {
            transform: scale(1.1);
            filter: brightness(1.1);
        }
        
        /* ============ ANIMATED DIVIDERS ============ */
        .animated-divider {
            height: 4px;
            background: linear-gradient(90deg, transparent, #7877c6, #9d4edd, #4ecdc4, transparent);
            margin: 2.5rem 0;
            animation: dividerPulse 3s ease-in-out infinite;
            box-shadow: 0 0 30px rgba(120, 119, 198, 0.5);
            border-radius: 2px;
        }
        
        @keyframes dividerPulse {
            0%, 100% {
                opacity: 0.5;
                box-shadow: 0 0 20px rgba(120, 119, 198, 0.3);
            }
            50% {
                opacity: 1;
                box-shadow: 0 0 40px rgba(120, 119, 198, 0.8);
            }
        }
        
        /* ============ FADE ANIMATIONS ============ */
        .fade-in {
            animation: fadeInUp 1s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
        }
        
        .fade-in-delay-1 { animation-delay: 0.2s; }
        .fade-in-delay-2 { animation-delay: 0.4s; }
        .fade-in-delay-3 { animation-delay: 0.6s; }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(50px) scale(0.9);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        /* ============ HEADER EFFECTS ============ */
        .header-glow {
            position: relative;
            z-index: 50;
            animation: headerFloat 4s ease-in-out infinite;
        }
        
        @keyframes headerFloat {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-10px);
            }
        }
        
        /* ============ FLOAT ANIMATION ============ */
        .float-animation {
            animation: floatUpDown 6s ease-in-out infinite;
        }
        
        @keyframes floatUpDown {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        /* ============ STREAMLIT FORM BUTTONS ============ */
        .stButton > button {
            background: linear-gradient(135deg, #7877c6, #9d4edd);
            color: white !important;
            padding: 15px 35px;
            border: none;
            border-radius: 15px;
            font-size: 1.1rem;
            font-weight: 700;
            box-shadow: 0 10px 30px rgba(120, 119, 198, 0.4);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            width: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-5px) scale(1.05);
            box-shadow: 0 15px 40px rgba(120, 119, 198, 0.7);
            background: linear-gradient(135deg, #9d4edd, #4ecdc4);
        }
        
        /* ============ FORM INPUTS ============ */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: rgba(255, 255, 255, 0.08) !important;
            border: 2px solid rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            padding: 18px 25px !important;
            border-radius: 15px !important;
            backdrop-filter: blur(15px);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            background: rgba(255, 255, 255, 0.15) !important;
            border: 2px solid #7877c6 !important;
            box-shadow: 
                0 0 40px rgba(120, 119, 198, 0.3),
                inset 0 0 15px rgba(120, 119, 198, 0.1) !important;
            transform: translateY(-2px);
        }
        
        /* ============ SCROLLBAR ============ */
        ::-webkit-scrollbar {
            width: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #7877c6, #9d4edd);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #9d4edd, #4ecdc4);
        }
        
        /* ============ RESPONSIVE DESIGN ============ */
        @media (max-width: 768px) {
            .card-container {
                padding: 20px 15px;
                margin: 15px 0;
            }
            
            [data-testid="stTabs"] [data-baseweb="tab-list"] {
                gap: 0.8rem;
            }
            
            [data-testid="stTabs"] [data-baseweb="tab"] {
                padding: 10px 15px;
                font-size: 0.9rem;
                height: 40px;
            }
            
            .glow-text {
                font-size: 1.8rem !important;
            }
            
            .skill-badge {
                padding: 8px 16px;
                font-size: 0.9rem;
                margin: 5px 7px;
            }
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def get_image_path(relative_path):
    """Secure image path resolution"""
    try:
        base_path = Path(__file__).parent / "images"
        full_path = base_path / relative_path
        if not full_path.is_file():
            logger.warning(f"Image not found: {relative_path}")
            return None
        return str(full_path)
    except Exception as e:
        logger.error(f"Error resolving image path: {e}")
        return None

def load_image(image_path):
    """Load image with error handling"""
    try:
        if image_path and os.path.exists(image_path):
            return Image.open(image_path)
        else:
            return get_placeholder_image(400, 400, color="#7877c6")
    except Exception as e:
        logger.error(f"Error loading image {image_path}: {e}")
        return get_placeholder_image(400, 400, color="#7877c6")

def get_placeholder_image(width, height, color="#7877c6"):
    """Generate placeholder image"""
    img = Image.new('RGB', (width, height), color=color)
    return img

def rate_limit_check():
    """Simple rate limiting for form submissions"""
    current_time = time.time()
    st.session_state.form_submissions = [
        t for t in st.session_state.form_submissions 
        if current_time - t < 3600
    ]
    if len(st.session_state.form_submissions) >= 5:
        return False
    return True

def save_message_to_db(name, email, message):
    """Save contact messages with enhanced security"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_id = hashlib.sha256(f"{name}{email}{timestamp}".encode()).hexdigest()[:16]
        
        message_data = {
            "id": message_id,
            "name": name,
            "email": email,
            "message": message,
            "timestamp": timestamp,
            "read": False
        }
        
        db_path = Path(__file__).parent / "data"
        db_path.mkdir(exist_ok=True)
        messages_file = db_path / "contact_messages.json"
        
        messages = []
        if messages_file.exists():
            try:
                with open(messages_file, "r") as f:
                    messages = json.load(f)
            except json.JSONDecodeError:
                logger.warning("Corrupted messages file, creating new one")
                messages = []
        
        messages.append(message_data)
        
        with open(messages_file, "w") as f:
            json.dump(messages, f, indent=4)
        
        logger.info(f"Message saved: {message_id}")
        return True
    except Exception as e:
        logger.error(f"Error saving message: {e}")
        return False

def send_email_notification(name, email, message):
    """Send email notification"""
    try:
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        recipient_email = os.getenv("RECIPIENT_EMAIL", "mahendraragimanu2@gmail.com")
        
        if not all([sender_email, sender_password]):
            logger.warning("Email credentials not configured")
            return False
        
        subject = f"🚀 New Portfolio Contact from {name}"
        email_message = MIMEMultipart()
        email_message["From"] = sender_email
        email_message["To"] = recipient_email
        email_message["Subject"] = subject
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: #0f0c29; padding: 40px;">
            <div style="max-width: 600px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 40px; border-radius: 20px;">
                <h2 style="color: #7877c6;">✨ New Contact Form Submission</h2>
                <p style="color: #fff;"><strong>Name:</strong> {name}</p>
                <p style="color: #fff;"><strong>Email:</strong> {email}</p>
                <p style="color: #fff;"><strong>Message:</strong></p>
                <p style="color: #ddd;">{message}</p>
                <hr style="border: 1px solid rgba(120,119,198,0.3);">
                <p style="color: #999; font-size: 12px;">🤖 Automated notification • {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
        </body>
        </html>
        """
        
        email_message.attach(MIMEText(html_content, "html"))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(email_message)
        
        logger.info(f"Email notification sent for: {name}")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

def is_valid_email(email):
    """Enhanced email validation"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

def sanitize_input(text):
    """Sanitize user input"""
    return text.strip()[:500]

# Portfolio data
ABOUT = """Aspiring AI & Data Professional with hands-on experience in Python, Machine Learning, LLMs (GPT-4), and RAG pipelines. Interned at C-DAC Hyderabad, where I built AI-powered knowledge graphs, semantic search tools, and document analysis apps using Streamlit, SQLite3, and NetworkX. Strong in data visualization, NLP, and automated data processing. Open to roles in AI Engineering, Data Science, or Python Development."""

WORK_EXPERIENCE = [
    {
        "company": "C-DAC Hyderabad",
        "position": "AI Engineering Intern",
        "duration": "June 2024 - August 2024",
        "details": [
            "Built AI-powered knowledge graphs using NetworkX and GPT-4",
            "Developed semantic search engine with LangChain and FAISS",
            "Created document analysis chatbot using Streamlit and Ollama",
            "Optimized data processing pipelines reducing latency by 40%"
        ],
        "image": "work_experience_cdac.png"
    },
    {
        "company": "Oppo Mobiles India",
        "position": "QA Testing Intern",
        "duration": "Feb 2024 - Apr 2024",
        "details": [
            "Conducted automated and manual testing for mobile applications",
            "Identified and documented 50+ software bugs with detailed reports",
            "Collaborated with development teams for issue resolution",
            "Improved test coverage by 30% using pytest"
        ],
        "image": "work_experience_oppo.jpg"
    }
]

PROJECTS = [
    {
        "title": "Knowledge Graph Visualizer",
        "description": "Interactive knowledge graph visualization system with semantic search capabilities",
        "tech": ["Python", "NetworkX", "Streamlit", "Neo4j", "LangChain"],
        "link": "#",
        "image": "knowledge_graph.png"
    },
    {
        "title": "DocuGenius - Document Chat",
        "description": "AI-powered document analysis and Q&A system using RAG pipelines",
        "tech": ["Python", "LangChain", "GPT-4", "FAISS", "Streamlit"],
        "link": "#",
        "image": "docugenius.png"
    },
    {
        "title": "Student Dashboard",
        "description": "Interactive analytics dashboard for student performance tracking",
        "tech": ["Python", "Plotly", "Pandas", "Streamlit", "SQLite3"],
        "link": "#",
        "image": "student_dashboard.png"
    },
    {
        "title": "APSPDCL Data Analysis",
        "description": "Power distribution data analysis and visualization system",
        "tech": ["Python", "Pandas", "Matplotlib", "Tableau"],
        "link": "#",
        "image": "apspdcl.jpg"
    }
]

SKILLS = {
    "Programming": ["Python", "JavaScript", "SQL", "C", "Go"],
    "AI/ML": ["GPT-4", "LangChain", "LLaMA2", "FAISS", "RAG", "Ollama"],
    "Data": ["Pandas", "NumPy", "Plotly", "SQLite3", "PostgreSQL"],
    "Tools": ["Streamlit", "Neo4j", "NetworkX", "VS Code", "Git", "Docker"],
    "Soft Skills": ["Problem Solving", "Communication", "Teamwork", "Leadership", "Documentation"]
}

EDUCATION = [
    {
        "institution": "KSRM College",
        "degree": "B.Tech Computer Science",
        "year": "2023",
        "gpa": "8.2/10",
        "image": "education.jpg"
    }
]

CERTIFICATIONS = [
    {"name": "Google AI Essentials", "issuer": "Google", "date": "2024"},
    {"name": "Python for Data Science", "issuer": "Coursera", "date": "2023"}
]

def animated_background_plot(tab_key):
    """Create animated background visualizations"""
    n = 600
    x = np.linspace(0, 15, n)
    noise = np.random.rand() * 2
    y = np.sin(x + noise) * np.cos(x * 0.5) * random.uniform(1.5, 3.0)
    
    color_schemes = {
        "about": px.colors.sequential.Purples,
        "exp": px.colors.sequential.Blues,
        "proj": px.colors.sequential.Teal,
        "skills": px.colors.sequential.Plasma,
        "edu": px.colors.sequential.Viridis,
        "contact": px.colors.sequential.Sunset
    }
    
    colors = color_schemes.get(tab_key, px.colors.sequential.Plasma)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        line=dict(
            color=colors[len(colors)//2],
            width=5
        ),
        fill='tonexty',
        fillcolor=f'rgba(120, 119, 198, 0.1)',
        opacity=0.4
    ))
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        template=None,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=200
    )
    
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def main():
    """Main application function"""
    load_custom_css()
    
    # Hero section
    st.markdown("""
    <div class="fade-in header-glow" style="text-align:center; padding:4rem 1.5rem;">
        <h1 class="glow-text" style="font-size:4rem; margin-bottom:1rem;">
            👨💻 Sivamahendranath Ragimanu
        </h1>
        <p style="font-size:1.4rem; opacity:0.95; margin-top:1.5rem; font-weight:300;">
            🚀 AI & Data Science Professional | Python Developer | ML Engineer
        </p>
        <div class="animated-divider"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "👤 About", 
        "💼 Experience", 
        "🚀 Projects", 
        "🎯 Skills", 
        "🎓 Education", 
        "📧 Contact"
    ])
    
    # About Tab
    with tab1:
        animated_background_plot("about")
        col1, col2 = st.columns([1, 1.4], gap="large")
        
        with col1:
            st.markdown('<div class="card-container float-animation">', unsafe_allow_html=True)
            profile_img = load_image(get_image_path("profile.jpeg"))
            st.image(profile_img, width=320)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card-container fade-in">', unsafe_allow_html=True)
            st.markdown("### 👋 About Me")
            st.write(ABOUT)
            
            st.markdown("### 🔗 Connect With Me")
            col_links = st.columns(4, gap="small")
            with col_links[0]:
                st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com)")
            with col_links[1]:
                st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com)")
            with col_links[2]:
                st.markdown("[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:mahendraragimanu2@gmail.com)")
            with col_links[3]:
                st.markdown("[![Resume](https://img.shields.io/badge/Resume-000000?style=for-the-badge&logo=adobe-acrobat&logoColor=white)](https://example.com)")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Experience Tab
    with tab2:
        animated_background_plot("exp")
        st.markdown("### 💼 Work Experience")
        
        for idx, exp in enumerate(WORK_EXPERIENCE):
            col1, col2 = st.columns([0.9, 1.1], gap="large")
            
            with col1:
                st.markdown('<div class="card-container fade-in">', unsafe_allow_html=True)
                exp_img = load_image(get_image_path(exp["image"]))
                st.image(exp_img, width=250)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="card-container fade-in-delay-1">', unsafe_allow_html=True)
                st.markdown(f"### {exp['company']}")
                st.markdown(f"**📍 {exp['position']}** | {exp['duration']}")
                for detail in exp['details']:
                    st.markdown(f"✅ {detail}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            if idx < len(WORK_EXPERIENCE) - 1:
                st.markdown('<div class="animated-divider"></div>', unsafe_allow_html=True)
    
    # Projects Tab
    with tab3:
        animated_background_plot("proj")
        st.markdown("### 🚀 Featured Projects")
        
        cols = st.columns(2, gap="large")
        for idx, project in enumerate(PROJECTS):
            with cols[idx % 2]:
                st.markdown('<div class="card-container fade-in">', unsafe_allow_html=True)
                proj_img = load_image(get_image_path(project["image"]))
                st.image(proj_img, width=350)
                st.markdown(f"#### {project['title']}")
                st.write(project['description'])
                st.markdown("**🛠️ Tech Stack:**")
                for tech in project['tech']:
                    st.markdown(f'<span class="skill-badge">{tech}</span>', unsafe_allow_html=True)
                st.markdown(f"[View Project →]({project['link']})")
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Skills Tab
    with tab4:
        animated_background_plot("skills")
        st.markdown("### 🎯 Technical Skills")
        
        cols = st.columns(2, gap="large")
        for idx, (category, skills) in enumerate(SKILLS.items()):
            with cols[idx % 2]:
                st.markdown('<div class="card-container fade-in">', unsafe_allow_html=True)
                st.markdown(f"#### {category}")
                for skill in skills:
                    st.markdown(f'<span class="skill-badge">{skill}</span>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Education Tab
    with tab5:
        animated_background_plot("edu")
        st.markdown("### 🎓 Education & Certifications")
        
        col1, col2 = st.columns([0.9, 1.1], gap="large")
        
        with col1:
            st.markdown('<div class="card-container float-animation">', unsafe_allow_html=True)
            edu_img = load_image(get_image_path(EDUCATION[0]["image"]))
            st.image(edu_img, width=280)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            for edu in EDUCATION:
                st.markdown('<div class="card-container fade-in">', unsafe_allow_html=True)
                st.markdown(f"### {edu['institution']}")
                st.write(f"**{edu['degree']}** | {edu['year']}")
                st.write(f"GPA: {edu['gpa']}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="animated-divider"></div>', unsafe_allow_html=True)
            
            st.markdown("#### 🏆 Certifications")
            for cert in CERTIFICATIONS:
                st.markdown('<div class="card-container fade-in-delay-1">', unsafe_allow_html=True)
                st.markdown(f"✨ **{cert['name']}** - {cert['issuer']} ({cert['date']})")
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Contact Tab
    with tab6:
        animated_background_plot("contact")
        st.markdown("### 📧 Get In Touch")
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown("#### 📍 Contact Information")
            st.markdown("""
            📍 **Location:** Anantapur, Andhra Pradesh, India  
            📧 **Email:** [mahendraragimanu2@gmail.com](mailto:mahendraragimanu2@gmail.com)  
            📱 **Phone:** +91 8106442744  
            🌐 **Portfolio:** https://example.com
            """)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown("#### ✉️ Send me a Message")
            
            with st.form("contact_form", clear_on_submit=True):
                name = st.text_input("Your Name", placeholder="John Doe")
                email = st.text_input("Your Email", placeholder="john@example.com")
                message = st.text_area("Message", placeholder="Your message here...", height=120)
                submit_button = st.form_submit_button("🚀 Send Message", use_container_width=True)
                
                if submit_button:
                    if not rate_limit_check():
                        st.error("❌ Too many submissions. Please try again later.")
                    elif not name or not email or not message:
                        st.error("❌ Please fill in all fields")
                    elif not is_valid_email(email):
                        st.error("❌ Please enter a valid email address")
                    elif len(message) < 10:
                        st.error("❌ Message must be at least 10 characters")
                    else:
                        name = sanitize_input(name)
                        email = sanitize_input(email)
                        message = sanitize_input(message)
                        
                        if save_message_to_db(name, email, message):
                            st.session_state.form_submissions.append(time.time())
                            send_email_notification(name, email, message)
                            st.success("✅ Message sent successfully! I'll get back to you soon.", icon="🎉")
                        else:
                            st.error("❌ Failed to send message. Please try again.")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="animated-divider" style="margin-top:5rem;"></div>
    <div style="text-align:center; padding:3rem 1.5rem; opacity:0.9;">
        <p style="font-size:1.05rem; margin-bottom:1rem;">
            © 2025 Sivamahendranath Ragimanu | Crafted with ❤️ using Streamlit
        </p>
        <p style="font-size:0.95rem; opacity:0.8; margin-top:1rem;">
            ✨ Enhanced with Advanced Animations, Glassmorphism & Production Features
        </p>
        <div class="fade-in" style="margin-top:1.5rem;">
            <span class="glow-text" style="font-size:1.2rem;">
                Let's build AI-powered solutions together! 🚀
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
