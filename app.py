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

# Page configuration
st.set_page_config(
    page_title="Sivamahendranath Ragimanu | Portfolio",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Function to get image path
def get_image_path(relative_path):
    """Get absolute path for an image based on relative path"""
    base_path = Path(__file__).parent / "images"
    return str(base_path / relative_path)

# Function to load an image safely
def load_image(image_path):
    """Load an image from path, with error handling"""
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        st.warning(f"Image not found: {image_path}")
        return get_placeholder_image(400, 300, color="#5846f6")
    except Exception as e:
        st.warning(f"Error loading image {image_path}: {str(e)}")
        return get_placeholder_image(400, 300, color="#5846f6")

# Function to verify image paths exist
def verify_image_paths():
    """Verify all image paths exist and are accessible"""
    image_paths = [
        "profile.jpeg",
        "about_me.jpeg",
        "work_experience_cdac.png",
        "work_experience_oppo.jpg",
        "knowledge_graph.png",
        "docugenius.png",
        "student_dashboard.png",
        "apspdcl.jpg",
        "exam_proctor.jpg",
        "smart_fan.jpg",
        "education.jpg",
    ]
    
    missing_images = []
    for path in image_paths:
        full_path = get_image_path(path)
        if not os.path.exists(full_path):
            missing_images.append(path)
    
    if missing_images:
        st.sidebar.warning("Missing images detected!")
        with st.sidebar.expander("Show missing images"):
            for img in missing_images:
                st.write(f"- {img}")
    else:
        st.sidebar.success("All image paths verified!")

# Generate placeholder images programmatically instead of using web URLs
def get_placeholder_image(width, height, color="#5846f6"):
    """Generate a placeholder image using PIL"""
    img = Image.new('RGB', (width, height), color=color)
    return img

# Function to save message to database (JSON file for simplicity)
def save_message_to_db(name, email, message):
    """Save contact message to a JSON file that acts as a simple database"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    message_data = {
        "name": name,
        "email": email,
        "message": message,
        "timestamp": timestamp,
        "read": False
    }
    
    # Check if database file exists, create if not
    db_path = Path(__file__).parent / "data"
    db_path.mkdir(exist_ok=True)
    
    messages_file = db_path / "contact_messages.json"
    
    if messages_file.exists():
        with open(messages_file, "r") as f:
            try:
                messages = json.load(f)
            except json.JSONDecodeError:
                messages = []
    else:
        messages = []
    
    messages.append(message_data)
    
    with open(messages_file, "w") as f:
        json.dump(messages, f, indent=4)
    
    return True

# Function to send email notification
def send_email_notification(name, email, message):
    """Send an email notification when a contact form is submitted"""
    try:
        # Get email credentials from environment variables
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        recipient_email = os.getenv("RECIPIENT_EMAIL", "mahendraragimanu2@gmail.com")
        
        # Check if credentials are available
        if not all([sender_email, sender_password, recipient_email]):
            st.warning("Email credentials not configured properly. Email notification not sent.")
            return False
        
        # Create email content
        subject = f"New Portfolio Contact from {name}"
        
        # Create a multipart message
        email_message = MIMEMultipart()
        email_message["From"] = sender_email
        email_message["To"] = recipient_email
        email_message["Subject"] = subject
        
        # Create HTML content for the email
        html_content = f"""
        <html>
            <body>
                <h2>New Contact Message from Your Portfolio</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Message:</strong></p>
                <p>{message}</p>
                <hr>
                <p><em>This is an automated notification from your portfolio website.</em></p>
            </body>
        </html>
        """
        
        # Attach HTML content
        email_message.attach(MIMEText(html_content, "html"))
        
        # Connect to SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.send_message(email_message)
        
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

# Email validation function
def is_valid_email(email):
    """Validate email format using regex"""
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(email_pattern, email))

# NEW: Particle animation background using Streamlit components
def create_particle_background():
    """Create an animated particle background using HTML/CSS/JS"""
    particle_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            #particles-js {
                position: fixed;
                width: 100%;
                height: 100%;
                top: 0;
                left: 0;
                z-index: -1;
            }
            .stApp {
                background: transparent;
            }
            .main .block-container {
                background: rgba(255, 255, 255, 0.9);
                border-radius: 10px;
                padding: 2rem;
                margin-top: 1rem;
                backdrop-filter: blur(5px);
            }
        </style>
    </head>
    <body>
        <div id="particles-js"></div>
        <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
        <script>
            particlesJS('particles-js', {
                "particles": {
                    "number": {
                        "value": 80,
                        "density": {
                            "enable": true,
                            "value_area": 800
                        }
                    },
                    "color": {
                        "value": "#5846f6"
                    },
                    "shape": {
                        "type": "circle",
                        "stroke": {
                            "width": 0,
                            "color": "#000000"
                        }
                    },
                    "opacity": {
                        "value": 0.5,
                        "random": false
                    },
                    "size": {
                        "value": 3,
                        "random": true
                    },
                    "line_linked": {
                        "enable": true,
                        "distance": 150,
                        "color": "#5846f6",
                        "opacity": 0.4,
                        "width": 1
                    },
                    "move": {
                        "enable": true,
                        "speed": 2,
                        "direction": "none",
                        "random": false,
                        "straight": false,
                        "out_mode": "out",
                        "bounce": false
                    }
                },
                "interactivity": {
                    "detect_on": "canvas",
                    "events": {
                        "onhover": {
                            "enable": true,
                            "mode": "grab"
                        },
                        "onclick": {
                            "enable": true,
                            "mode": "push"
                        }
                    }
                }
            });
        </script>
    </body>
    </html>
    """
    return particle_html

# NEW: Animated gradient background option
def create_gradient_background():
    """Create an animated gradient background using CSS"""
    gradient_css = """
    <style>
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    </style>
    """
    return gradient_css

# NEW: Floating animation for elements
def add_floating_animation():
    """Add floating animation to elements"""
    floating_css = """
    <style>
    @keyframes float {
        0% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
        100% {
            transform: translateY(0px);
        }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }
    
    .typewriter h1 {
        overflow: hidden;
        border-right: .15em solid #5846f6;
        white-space: nowrap;
        margin: 0 auto;
        animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #5846f6; }
    }
    </style>
    """
    return floating_css

# NEW: Interactive hover effects
def add_hover_effects():
    """Add interactive hover effects to cards and buttons"""
    hover_css = """
    <style>
    .hover-card {
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .hover-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .glow-on-hover {
        transition: all 0.3s ease;
    }
    
    .glow-on-hover:hover {
        box-shadow: 0 0 15px #5846f6;
    }
    
    .fade-in-section {
        opacity: 0;
        transform: translateY(20px);
        transition: opacity 0.6s ease, transform 0.6s ease;
    }
    
    .is-visible {
        opacity: 1;
        transform: translateY(0);
    }
    </style>
    """
    return hover_css

# NEW: Scroll progress indicator
def create_scroll_progress():
    """Create a scroll progress indicator"""
    progress_js = """
    <script>
    window.onscroll = function() {
        var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        var scrolled = (winScroll / height) * 100;
        document.getElementById("progressBar").style.width = scrolled + "%";
    };
    </script>
    <style>
    .progress-container {
        width: 100%;
        height: 4px;
        background: #f1f1f1;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 9999;
    }
    
    .progress-bar {
        height: 4px;
        background: #5846f6;
        width: 0%;
        transition: width 0.3s;
    }
    </style>
    <div class="progress-container">
        <div class="progress-bar" id="progressBar"></div>
    </div>
    """
    return progress_js

# Include Font Awesome for icons
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)

# NEW: Add all animation and effect styles
st.markdown(add_floating_animation(), unsafe_allow_html=True)
st.markdown(add_hover_effects(), unsafe_allow_html=True)

# Create a simple sidebar for theme selection
with st.sidebar:
    st.title("🎨 Theme & Effects")
    
    # Background selection
    background_choice = st.selectbox("Choose Background", ["Particle Animation", "Gradient Animation", "Simple White"])
    
    # Animation toggle
    enable_animations = st.checkbox("Enable Animations", value=True)
    
    # Apply theme via session state
    if 'background' not in st.session_state:
        st.session_state.background = background_choice
    
    if st.session_state.background != background_choice:
        st.session_state.background = background_choice
        st.rerun()
    
    # Add social links in sidebar
    st.markdown("---")
    st.markdown("### 🔗 Connect With Me")
    cols = st.columns(3)
    cols[0].markdown(f'<a href="https://www.linkedin.com/in/sivamahendranath-ragimanu-68a94823b/" target="_blank"><i class="fab fa-linkedin fa-2x" style="color: #5846f6;"></i></a>', unsafe_allow_html=True)
    cols[1].markdown(f'<a href="https://github.com/Sivamahendranath" target="_blank"><i class="fab fa-github fa-2x" style="color: #5846f6;"></i></a>', unsafe_allow_html=True)
    cols[2].markdown(f'<a href="mailto:mahendraragimanu2@gmail.com" target="_blank"><i class="fas fa-envelope fa-2x" style="color: #5846f6;"></i></a>', unsafe_allow_html=True)

# Apply selected background
if st.session_state.background == "Particle Animation":
    from streamlit.components.v1 import html
    particle_html = create_particle_background()
    html(particle_html, height=0, width=0)
elif st.session_state.background == "Gradient Animation":
    st.markdown(create_gradient_background(), unsafe_allow_html=True)

# Add scroll progress indicator
st.markdown(create_scroll_progress(), unsafe_allow_html=True)

# Enhanced CSS styling with animations
st.markdown(f"""
<style>
    /* Basic styling with enhanced animations */
    .hero-section h1 {{
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #5846f6, #e73c7e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .highlight {{
        color: #5846f6;
    }}
    .section-header h2 {{
        border-bottom: 2px solid #5846f6;
        padding-bottom: 10px;
        margin-top: 30px;
        position: relative;
        overflow: hidden;
    }}
    .section-header h2::after {{
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 0%;
        height: 2px;
        background: linear-gradient(90deg, #5846f6, #e73c7e);
        animation: expandLine 2s ease-in-out forwards;
    }}
    @keyframes expandLine {{
        from {{ width: 0%; }}
        to {{ width: 100%; }}
    }}
    .custom-card {{
        border-left: 4px solid #5846f6;
        padding: 20px;
        margin: 15px 0;
        background: linear-gradient(135deg, rgba(88, 70, 246, 0.05) 0%, rgba(231, 60, 126, 0.05) 100%);
        border-radius: 10px;
        transition: all 0.3s ease;
    }}
    .custom-card:hover {{
        transform: translateX(10px);
        box-shadow: 0 10px 30px rgba(88, 70, 246, 0.2);
    }}
    .fade-in {{
        animation: fadeIn 1s ease-in;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    .skill-container {{
        margin: 15px 0;
    }}
    .skill-bar-container {{
        background-color: #e0e0e0;
        border-radius: 10px;
        height: 10px;
        width: 100%;
        overflow: hidden;
    }}
    .skill-bar {{
        background: linear-gradient(90deg, #5846f6, #e73c7e);
        border-radius: 10px;
        height: 10px;
        transform: scaleX(0);
        transform-origin: left;
        animation: growBar 2s ease-in-out forwards;
    }}
    @keyframes growBar {{
        to {{ transform: scaleX(1); }}
    }}
    .timeline-item {{
        position: relative;
        padding-left: 30px;
        margin-bottom: 30px;
    }}
    .timeline-dot {{
        position: absolute;
        left: 0;
        top: 5px;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        background: linear-gradient(45deg, #5846f6, #e73c7e);
        animation: pulse 2s infinite;
    }}
    .timeline-date {{
        font-weight: bold;
        margin-bottom: 5px;
        color: #5846f6;
    }}
    .timeline-content {{
        margin-left: 10px;
    }}
    .footer {{
        margin-top: 50px;
        padding: 20px 0;
        text-align: center;
        border-top: 1px solid #e0e0e0;
    }}
    .key-points {{
        margin-top: 15px;
    }}
    .key-point {{
        margin-bottom: 8px;
        padding: 10px;
        border-radius: 5px;
        background: rgba(88, 70, 246, 0.1);
        transition: all 0.3s ease;
    }}
    .key-point:hover {{
        background: rgba(88, 70, 246, 0.2);
        transform: translateX(5px);
    }}
    .key-point i {{
        margin-right: 10px;
        color: #5846f6;
    }}
    .project-meta {{
        margin: 20px 0;
    }}
    .project-meta div {{
        margin-bottom: 10px;
        padding: 5px 10px;
        background: rgba(88, 70, 246, 0.1);
        border-radius: 5px;
        transition: all 0.3s ease;
    }}
    .project-meta div:hover {{
        background: rgba(88, 70, 246, 0.2);
        transform: translateX(5px);
    }}
    .project-meta i {{
        margin-right: 10px;
        color: #5846f6;
    }}
    .tech-stack {{
        margin-top: 20px;
    }}
    .tech-badge {{
        display: inline-block;
        background: linear-gradient(45deg, #5846f6, #e73c7e);
        color: white;
        padding: 5px 15px;
        margin: 5px;
        border-radius: 20px;
        font-size: 0.8rem;
        transition: all 0.3s ease;
    }}
    .tech-badge:hover {{
        transform: scale(1.1);
        box-shadow: 0 5px 15px rgba(88, 70, 246, 0.3);
    }}
    .project-icon {{
        text-align: center;
        color: #5846f6;
        margin: 20px 0;
    }}
    .project-details h3 {{
        margin-bottom: 15px;
        color: #5846f6;
        position: relative;
        display: inline-block;
    }}
    .project-details h3::after {{
        content: '';
        position: absolute;
        bottom: -5px;
        left: 0;
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, #5846f6, #e73c7e);
        transition: width 0.3s ease;
    }}
    .project-details:hover h3::after {{
        width: 100%;
    }}
    .project-description {{
        font-style: italic;
        margin-bottom: 20px;
        padding: 15px;
        background: rgba(88, 70, 246, 0.05);
        border-radius: 10px;
        border-left: 4px solid #5846f6;
    }}
    .feature-list li {{
        margin-bottom: 10px;
        padding-left: 10px;
        border-left: 2px solid transparent;
        transition: all 0.3s ease;
    }}
    .feature-list li:hover {{
        border-left: 2px solid #5846f6;
        background: rgba(88, 70, 246, 0.05);
        padding-left: 15px;
    }}
    .education-grade {{
        margin-top: 10px;
    }}
    .education-grade i {{
        color: gold;
    }}
    .language-card {{
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, rgba(88, 70, 246, 0.1) 0%, rgba(231, 60, 126, 0.1) 100%);
        border-radius: 15px;
        margin: 10px;
        transition: all 0.3s ease;
    }}
    .language-card:hover {{
        transform: translateY(-10px);
        box-shadow: 0 15px 30px rgba(88, 70, 246, 0.2);
    }}
    .language-icon {{
        font-size: 2rem;
        margin-bottom: 10px;
        color: #5846f6;
    }}
    .contact-info {{
        margin: 20px 0;
    }}
    .contact-item {{
        display: flex;
        align-items: flex-start;
        margin-bottom: 20px;
        padding: 15px;
        background: rgba(88, 70, 246, 0.05);
        border-radius: 10px;
        transition: all 0.3s ease;
    }}
    .contact-item:hover {{
        background: rgba(88, 70, 246, 0.1);
        transform: translateX(10px);
    }}
    .contact-item i {{
        font-size: 1.5rem;
        color: #5846f6;
        margin-right: 15px;
        margin-top: 5px;
    }}
    .social-links {{
        margin-top: 15px;
    }}
    .social-links a {{
        margin: 0 10px;
        color: #5846f6;
        text-decoration: none;
        transition: all 0.3s ease;
    }}
    .social-links a:hover {{
        color: #e73c7e;
        transform: scale(1.2);
    }}
    .accomplishment-card {{
        display: flex;
        align-items: flex-start;
        background: linear-gradient(135deg, rgba(88, 70, 246, 0.1) 0%, rgba(231, 60, 126, 0.1) 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }}
    .accomplishment-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(88, 70, 246, 0.2);
    }}
    .accomplishment-icon {{
        font-size: 1.5rem;
        color: #5846f6;
        margin-right: 15px;
    }}
    .soft-skill-card {{
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, rgba(88, 70, 246, 0.1) 0%, rgba(231, 60, 126, 0.1) 100%);
        border-radius: 15px;
        margin: 10px;
        transition: all 0.3s ease;
    }}
    .soft-skill-card:hover {{
        transform: scale(1.05);
        box-shadow: 0 10px 25px rgba(88, 70, 246, 0.2);
    }}
    .soft-skill-card i {{
        font-size: 1.5rem;
        color: #5846f6;
        margin-bottom: 10px;
    }}
    .profile-img {{
        border-radius: 50%;
        max-width: 100%;
        border: 3px solid #5846f6;
        transition: all 0.3s ease;
    }}
    .profile-img:hover {{
        border-color: #e73c7e;
        transform: scale(1.05);
    }}
    .contact-button {{
        background: linear-gradient(45deg, #5846f6, #e73c7e);
        color: white;
        padding: 12px 24px;
        border-radius: 25px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border: none;
        transition: all 0.3s ease;
    }}
    .contact-button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(88, 70, 246, 0.3);
    }}
    .section-divider {{
        height: 50px;
    }}
    .section {{
        padding: 30px 0;
        border-bottom: 1px solid #e0e0e0;
    }}
    .section:last-child {{
        border-bottom: none;
    }}
    .image-debug {{
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 5px;
        margin-bottom: 10px;
    }}
    .skill-category {{
        margin-bottom: 30px;
    }}
    .skill-category h3 {{
        color: #5846f6;
        border-bottom: 1px solid rgba(88, 70, 246, 0.3);
        padding-bottom: 8px;
        margin-bottom: 15px;
        position: relative;
    }}
    .skill-category h3::after {{
        content: '';
        position: absolute;
        bottom: -1px;
        left: 0;
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, #5846f6, #e73c7e);
        animation: expandLine 2s ease-in-out forwards;
        animation-delay: 0.5s;
    }}
    .skill-category-icon {{
        font-size: 1.8rem;
        margin-right: 10px;
        color: #5846f6;
        vertical-align: middle;
    }}
    .form-error {{
        color: #ff4444;
        font-size: 0.9rem;
        margin-top: 2px;
    }}
    .form-success {{
        color: #4CAF50;
        padding: 10px;
        border-radius: 5px;
        background-color: rgba(76, 175, 80, 0.1);
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
    }}
    .required-field:after {{
        content: " *";
        color: #ff4444;
    }}
    
    /* NEW: Staggered animations for list items */
    .stagger-item {{
        opacity: 0;
        transform: translateY(20px);
        animation: fadeInUp 0.6s ease forwards;
    }}
    
    @keyframes fadeInUp {{
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* NEW: Glitch effect for headers */
    .glitch {{
        position: relative;
        display: inline-block;
    }}
    
    .glitch::before,
    .glitch::after {{
        content: attr(data-text);
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }}
    
    .glitch::before {{
        left: 2px;
        text-shadow: -2px 0 #ff00c1;
        clip: rect(44px, 450px, 56px, 0);
        animation: glitch-anim 5s infinite linear alternate-reverse;
    }}
    
    .glitch::after {{
        left: -2px;
        text-shadow: -2px 0 #00fff9;
        clip: rect(44px, 450px, 56px, 0);
        animation: glitch-anim2 5s infinite linear alternate-reverse;
    }}
    
    @keyframes glitch-anim {{
        0% {{ clip: rect(31px, 9999px, 13px, 0); }}
        5% {{ clip: rect(64px, 9999px, 25px, 0); }}
        10% {{ clip: rect(9px, 9999px, 10px, 0); }}
        15% {{ clip: rect(42px, 9999px, 30px, 0); }}
        20% {{ clip: rect(97px, 9999px, 61px, 0); }}
        25% {{ clip: rect(80px, 9999px, 2px, 0); }}
        30% {{ clip: rect(47px, 9999px, 84px, 0); }}
        35% {{ clip: rect(48px, 9999px, 42px, 0); }}
        40% {{ clip: rect(23px, 9999px, 53px, 0); }}
        45% {{ clip: rect(38px, 9999px, 32px, 0); }}
        50% {{ clip: rect(40px, 9999px, 35px, 0); }}
        55% {{ clip: rect(43px, 9999px, 60px, 0); }}
        60% {{ clip: rect(89px, 9999px, 33px, 0); }}
        65% {{ clip: rect(20px, 9999px, 33px, 0); }}
        70% {{ clip: rect(34px, 9999px, 65px, 0); }}
        75% {{ clip: rect(44px, 9999px, 93px, 0); }}
        80% {{ clip: rect(56px, 9999px, 50px, 0); }}
        85% {{ clip: rect(64px, 9999px, 63px, 0); }}
        90% {{ clip: rect(59px, 9999px, 67px, 0); }}
        95% {{ clip: rect(22px, 9999px, 16px, 0); }}
        100% {{ clip: rect(66px, 9999px, 82px, 0); }}
    }}
</style>
""", unsafe_allow_html=True)

# Main content - Now in scrolling format with enhanced animations
# SECTION 1: Home
st.markdown('<div class="section" id="home">', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="hero-section fade-in">
        <h1 class="glitch" data-text="Sivamahendranath Ragimanu">Sivamahendranath Ragimanu</h1>
        <h3>🎓 Computer Science Graduate | Python Developer | Data Analyst | AI | Machine Learning Enthusiast</h3>
        <p class="lead-text">Aspiring AI & Data Professional with hands-on experience in Python, Machine Learning, LLMs (GPT-4), and RAG pipelines. Interned at C-DAC Hyderabad, where I built AI-powered knowledge graphs, semantic search tools, and document analysis apps using Streamlit, SQLite3, and NetworkX.
Strong in data visualization, NLP, and automated data processing. Prior internship at Oppo Mobiles enhanced my skills in testing, collaboration, and debugging.

I'm driven to build smart, scalable, and impactful AI solutions that turn raw data into insights. Open to roles in AI Engineering, Data Science, or Python Development.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Load profile image with floating animation
    profile_image_path = get_image_path("profile.jpeg")
    if os.path.exists(profile_image_path):
        profile_img = load_image(profile_image_path)
    else:
        profile_img = get_placeholder_image(300, 300, color="#5846f6")
    st.image(profile_img, use_container_width=True, output_format="PNG")

# About Section
st.markdown("<div class='section-header'><h2>About Me</h2></div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    # Load about image with hover effect
    about_image_path = get_image_path("about_me.jpeg")
    if os.path.exists(about_image_path):
        about_img = load_image(about_image_path)
    else:
        about_img = get_placeholder_image(400, 400, color="#4a3bf5")
    st.image(about_img, caption="Sivamahendranath Ragimanu", use_container_width=True)

with col2:
    st.markdown("""
    <div class="about-text fade-in">
        <p>Aspiring AI & Data Science professional skilled in Python, NLP, LLMs (GPT-4, LLaMA2), RAG pipelines, and Streamlit. Experienced in building offline-first AI applications, including document chatbots, knowledge graph visualizers, and semantic search tools.

Interned at C-DAC Hyderabad, developing AI-powered solutions focused on data privacy and interactive insights. Gained hands-on testing and debugging experience at Oppo Mobiles India.

Core skills: Python | GPT-4 | LangChain | Whisper | Ollama | NLP | SQLite3 | NetworkX | Data Visualization | OpenCV

Open to roles in AI Engineering, Data Science, and Python Development.
I am passionate about building scalable AI-powered solutions that emphasize data privacy, interactive user experience, and real-world impact.<br>
Seeking opportunities in: AI Engineering, Data Science, Python Development, NLP Research. </p>
</div>
    """, unsafe_allow_html=True)
    
    # Add key points separately with staggered animation
    st.markdown("""
    <div class="key-points">
        <div class="key-point stagger-item" style="animation-delay: 0.1s"><i class="fas fa-map-marker-alt"></i> Anantapur,  Andhra Pradesh</div>
        <div class="key-point stagger-item" style="animation-delay: 0.2s"><i class="fas fa-phone"></i> 8106442744</div>
        <div class="key-point stagger-item" style="animation-delay: 0.3s"><i class="fas fa-envelope"></i> mahendraragimanu2@gmail.com</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# SECTION 2: Skills & Experience
st.markdown('<div class="section" id="skills">', unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Technical Skills</h2></div>", unsafe_allow_html=True)

# Organized skills by category
skill_categories = {
    "Programming & Scripts": {
        "icon": "fas fa-code",
        "skills": [
            "Python",
            "Java"
        ]
    },
    "Web Development": {
        "icon": "fas fa-globe",
        "skills": [
            "HTML/CSS",
            "JavaScript",
            "Streamlit"
        ]
    },
    "Database": {
        "icon": "fas fa-database",
        "skills": [
            "SQL (Oracle)",
            "SQLite"
        ]
    },
    "Data Science & AI": {
        "icon": "fas fa-brain",
        "skills": [
            "Machine Learning",
            "Data Analysis",
            "LLMs & RAG",
            "Data Visualization"
        ]
    }
}

# Display skills by category with enhanced animations
for category, data in skill_categories.items():
    st.markdown(f"""
    <div class="skill-category">
        <h3><i class="{data['icon']} skill-category-icon"></i>{category}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    skills_list = data["skills"]
    half = len(skills_list) // 2 + len(skills_list) % 2
    
    with col1:
        for i, skill in enumerate(skills_list[:half]):
            st.markdown(f"""
            <div class="skill-container fade-in" style="animation-delay: {i * 0.2}s">
                <div class="skill-name">{skill}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        for i, skill in enumerate(skills_list[half:]):
            st.markdown(f"""
            <div class="skill-container fade-in" style="animation-delay: {(i + half) * 0.2}s">
                <div class="skill-name">{skill}</div>
            </div>
            """, unsafe_allow_html=True)

# Soft Skills with enhanced cards
st.markdown("<div class='section-header'><h2>Soft Skills</h2></div>", unsafe_allow_html=True)

soft_skills = ["Communication", "Team Work", "Leadership", "Problem Solving", "Analytical Thinking"]

col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

for i, skill in enumerate(soft_skills):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="soft-skill-card fade-in" style="animation-delay: {i * 0.2}s">
            <i class="fas fa-check-circle"></i>
            <h4>{skill}</h4>
        </div>
        """, unsafe_allow_html=True)

# Work Experience with enhanced timeline
st.markdown("<div class='section-header'><h2>Work Experience</h2></div>", unsafe_allow_html=True)

# Load work experience image for CDAC
cdac_img_path = get_image_path("work_experience_cdac.png")
if os.path.exists(cdac_img_path):
    exp_img = load_image(cdac_img_path)
else:
    exp_img = get_placeholder_image(800, 300, color="#3b2ff5")
st.image(exp_img, caption="Work Experience at CDAC", use_container_width=True)

# Experience 1 with enhanced animation
st.markdown("""
<div class="timeline fade-in">
    <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-date">October 2024 - April 2025</div>
        <div class="timeline-content custom-card">
            <h3>Data Analyst (Python), Intern</h3>
            <h4>C-DAC, Hyderabad</h4>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# List items for Experience 1 with staggered animation
st.markdown("""
<ul style="margin-top: -20px; margin-left: 40px;">
    <li class="stagger-item" style="animation-delay: 0.1s">Analyzed and visualized complex datasets using Python, Pandas, and Matplotlib to uncover actionable business insights.</li>
    <li class="stagger-item" style="animation-delay: 0.2s">Extracted structured information from unstructured text using LLMs (GPT-4) and applied NLP techniques for deeper analysis.</li>
    <li class="stagger-item" style="animation-delay: 0.3s">Designed and managed SQLite3 databases to efficiently store, query, and retrieve knowledge graph data.</li>
    <li class="stagger-item" style="animation-delay: 0.4s">Built interactive data visualizations and semantic graphs using NetworkX and Pyvis for intuitive insight communication.</li>
    <li class="stagger-item" style="animation-delay: 0.5s">Automated data collection and enrichment using web scraping (BeautifulSoup), enhancing analysis depth 
and accuracy.</li>
</ul>
""", unsafe_allow_html=True)

# Load work experience image for OPPO
oppo_img_path = get_image_path("work_experience_oppo.jpg")
if os.path.exists(oppo_img_path):
    oppo_img = load_image(oppo_img_path)
    st.image(oppo_img, caption="Work Experience at OPPO", use_container_width=True)

# Experience 2
st.markdown("""
<div class="timeline fade-in">
    <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-date">February 2023 - August 2023</div>
        <div class="timeline-content custom-card">
            <h3>Device Testing, Intern</h3>
            <h4>Oppo Mobiles India Ltd, Hyderabad (Remote)</h4>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# List items for Experience 2 with staggered animation
st.markdown("""
<ul style="margin-top: -20px; margin-left: 40px;">
    <li class="stagger-item" style="animation-delay: 0.1s">Worked as a device testing engineer role in intern position.</li>
    <li class="stagger-item" style="animation-delay: 0.2s">Testing and checking the mobile device performance.</li>
    <li class="stagger-item" style="animation-delay: 0.3s">Finding the bugs in the device and reporting them to the team leader.</li>
    <li class="stagger-item" style="animation-delay: 0.4s">Communicating with team members and Developers, Giving and sharing the ideas for solving the bug issues and improving the device performance.</li>
</ul>
""", unsafe_allow_html=True)

# Professional Accomplishments with enhanced cards
st.markdown("<div class='section-header'><h2>Professional Accomplishments</h2></div>", unsafe_allow_html=True)

accomplishments = [
    {"title": "Event Organizer", "icon": "fas fa-calendar-check", "detail": "Leading as an Event Organizer(Coding, Workshops) at KSRM College of Engineering."},
    {"title": "Team Leader", "icon": "fas fa-users", "detail": "Serving as Team Leader for both minor and major projects at KSRM College of Engineering."},
    {"title": "Coder", "icon": "fas fa-code", "detail": "Actively involved as a coder in the major project development."}
]

col1, col2 = st.columns(2)

for i, acc in enumerate(accomplishments):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"""
        <div class="accomplishment-card fade-in" style="animation-delay: {i * 0.2}s">
            <div class="accomplishment-icon"><i class="{acc['icon']}"></i></div>
            <div class="accomplishment-content">
                <h4>{acc['title']}</h4>
                <p>{acc['detail']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# SECTION 3: Projects
st.markdown('<div class="section" id="projects">', unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Personal Projects</h2></div>", unsafe_allow_html=True)

# Define project images mapping
project_images = {
    "AI-Powered Knowledge Graph Explorer": "knowledge_graph.png",
    "DocuGenius Pro": "docugenius.png",
    "Student Performance Dashboards for Exams": "student_dashboard.png",
    "Andhra Pradesh Southern Power Distribution Company Limited": "apspdcl.jpg",
    "Exam Proctoring System": "exam_proctor.jpg",
    "Smart Fan Energy System": "smart_fan.jpg"
}

col1, col2 = st.columns([1, 2])

with col1:
    # Project image placeholder with floating animation
    project_img_path = get_image_path("main_project.jpg")
    if os.path.exists(project_img_path):
        project_img = load_image(project_img_path)
    else:
        project_img = get_placeholder_image(400, 300, color="#6557f1")
    st.image(project_img, caption="Projects", use_container_width=True)

with col2:
    st.markdown("""
    <div class="project-intro fade-in">
        <p>I have worked on several projects that demonstrate my skills in Python, Machine Learning, 
        Data Analysis, and IoT. Below are some of my key projects:</p>
    </div>
    """, unsafe_allow_html=True)

# Individual Projects with GitHub links and enhanced animations
projects = [
    {
        "title": "AI-Powered Knowledge Graph Explorer",
         "date": "January 2025, March 2025",
         "org": "C-DAC, Hyderabad",
         "type": "Main Project",
         "description": "AI-Powered Knowledge Graph Generator using LLMs and Graph Visualization Application using Streamlit",
        "features": [
             "Multi-Format Input Handling: Ingested and parsed raw input from Text files and Web URLs for seamless data processing",
             "LLM-Based Entity Extraction: Leveraged Google Gemini API to extract entities, attributes, relationships, and contextual links.",
            "Structured Data Storage: Stored parsed information in SQLite3 using a scalable, query-ready schema.",
             "Interactive Graph Visualization: Built dynamic knowledge graphs with NetworkX and Pyvis,supporting node-click expansion.",
             "Semantic Relationship Exploration: Enabled deep relationship analysis with continuous graph expansion and case study generation."

        ],
        "tech_stack": ["Python", "Streamlit", "Google Gemini API", "Sqlite3","Plotly", "NLP", "NetworkX", "BeautifulSoup"],
        "github": "https://github.com/Sivamahendranath/Gemini_Knowledge_Graph/blob/main/backup.py"
    },
    {
        "title": "DocuGenius Pro",
         "date": "January 2025",
         "org": "C-DAC, Hyderabad",
         "type": "Personal Mini Project",
       "description": "AI-powered document processing application using Streamlit",
        "features": [
           "Multi-Format Document Processing: Extracts and processes Text, PDFs, CSVs, and Web URLs",
             "AI-Powered Analysis: Leverages Google Gemini API for insights, summaries, and answers",
             "Data Visualization: Creates interactive graphs and statistics for CSV data with Plotly",
            "Named Entity Recognition (NER): Identifies key entities from processed documents",
             "Query-Based Analysis: Allows users to ask questions based on document content",
             "Customizable Themes & Export Analysis History"

        ],
       "tech_stack": ["Python", "Streamlit", "Google Gemini API", "Plotly", "NLP"],
         "github": "https://github.com/Sivamahendranath/Gemini-Document-RAG/blob/main/code/main.py"
    },
    {
        "title": "Student Performance Dashboards for Exams",
         "date": "October 2024 - November 2024",
         "org": "C-DAC, Hyderabad",
        "type": "Mini Project",
        "description": "Data visualization dashboards for analyzing student performance",
        "features": [
            "Cleaned and processed datasets, converting columns to numeric and handling missing data",
             "Designed thresholds to classify performance into categories (Fail to Excellent)",
             "Aggregated and summarized student performance metrics across lab and theory scores",
             "Created diverse visualizations including pie charts, bar charts, stacked bars, heatmaps",
            "Implemented advanced visualization techniques for trend analysis and insights",
             "Optimized data workflows for decision-making"

        ],
        "tech_stack": ["Python", "Numpy", "Pandas", "Matplotlib", "Seaborn", "Data Visualization"],
         "github": "https://github.com/Sivamahendranath/Student-Performance-Dashboard"
    },
    {
        "title": "Andhra Pradesh Southern Power Distribution Company Limited",
         "date": "April 2024 - May 2024",
         "org": "KSRM College Of Engineering, Kadapa",
         "type": "Personal Mini Project",
         "description": "Electricity Bill Calculator – Streamlit Web Application",
        "features": [
           "Multi-Tariff Bill Calculation: Calculates electricity bills for domestic, commercial, and industrial users with tiered and time-of-use tariff logic.",
             "Interactive Visualizations: Uses Plotly to display consumption patterns and billing breakdown through dynamic charts and graphs.",
             "PDF Bill Generation: Generates downloadable and printable bills in PDF format using ReportLab for professional documentation.",
             "Usage History & Trends: Tracks historical electricity usage and visualizes spending trends to help users monitor and manage consumption.",
             "Responsive UI Design: Built with Streamlit for a mobile-friendly, intuitive interface that works seamlessly across all devices.",
            "Real-World Utility Integration: Tailored for APSPDCL with accurate tariff modeling, due date logic, and late fee calculations.",
             "Modular Architecture: Structured with scalable components and future-ready plans including authentication, payments, and multi-language support."

        ],
        "tech_stack": ["Python", "Streamlit", "Plotly", "Pandas", "ReportLab", "HTML/CSS"],
         "github": "https://github.com/Sivamahendranath/Electricity_Bill_App/blob/main/app.py",
    },
    {
        "title": "Exam Proctoring System",
         "date": "December 2023 - March 2024",
        "org": "KSRM College Of Engineering, Kadapa",
         "type": "Major Project",
         "description": "Machine learning application for online exam proctoring",
         "features": [
            "Led a team and developed a machine learning application for online exam proctoring",
             "Used OpenCV, Dlib, and Face Recognition Library for monitoring candidates",
             "Monitored candidates' movements and flagged suspicious activities during exams",
             "Implemented warning mechanisms and automatic termination for suspicious activities",
             "Generated detailed malpractice reports, including activity graphs, for authorities"
         ],
         "tech_stack": ["Python", "OpenCV", "Dlib", "Face Recognition", "Machine Learning"],
        "github": "https://github.com/Sivamahendranath/Exam-Proctoring-System",

    },
    {
         "title": "Smart Fan Energy System",
        "date": "July 2023 - September 2023",
         "org": "KSRM College Of Engineering, Kadapa",
         "type": "Minor Project",
         "description": "IoT-based solution for optimizing energy usage in fan systems",
         "features": [
             "Led as Team Leader, Circuit Designer, and Arduino Coder",
             "Combined hardware and software expertise using Arduino and sensors",
            "Designed a cost-effective, customizable system for automating fan speed and power control",
             "Created a system that increased energy efficiency by 25% compared to manual fan control",
             "Implemented automatic temperature-based fan speed adjustment for optimal comfort"
        ],
         "tech_stack": ["Arduino", "IoT", "Sensors"],
         "github": "https://github.com/Sivamahendranath/Smart-Fan-Energy-System",

    }
]

# Display projects in a nice format with enhanced animations
for i, project in enumerate(projects):
    # Create columns for each project
    if i % 2 == 0:
        col1, col2 = st.columns(2)
    
    with col1 if i % 2 == 0 else col2:
        # Get project image if available
        img_path = get_image_path(project_images.get(project["title"], "placeholder.jpg"))
        if os.path.exists(img_path):
            project_img = load_image(img_path)
        else:
            project_img = get_placeholder_image(400, 300, color="#5846f6")
        
        st.image(project_img, caption=project["title"], use_container_width=True)
        
        st.markdown(f"""
        <div class="project-details fade-in" style="animation-delay: {i * 0.1}s">
            <h3>{project["title"]}</h3>
            <div class="project-meta">
                <div><i class="far fa-calendar-alt"></i> {project["date"]}</div>
                <div><i class="fas fa-building"></i> {project["org"]}</div>
                <div><i class="fas fa-tag"></i> {project["type"]}</div>
            </div>
            <p class="project-description">{project["description"]}</p>
            <h4>Key Features:</h4>
            <ul class="feature-list">
                {"".join([f"<li>{feature}</li>" for feature in project["features"]])}
            </ul>
            <div class="tech-stack">
                <h4>Tech Stack:</h4>
                <div>
                    {"".join([f'<span class="tech-badge">{tech}</span>' for tech in project["tech_stack"]])}
                </div>
            </div>
            <div style="margin-top: 15px;">
                <a href="{project["github"]}" target="_blank" style="color: #5846f6;">
                    <i class="fab fa-github"></i> View on GitHub
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add separator after each row
    if i % 2 == 1 or i == len(projects) - 1:
        st.markdown("<hr>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# SECTION 4: Education
st.markdown('<div class="section" id="education">', unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Education</h2></div>", unsafe_allow_html=True)

# Education image
edu_img_path = get_image_path("education.jpg")
if os.path.exists(edu_img_path):
    edu_img = load_image(edu_img_path)
else:
    edu_img = get_placeholder_image(600, 400, color="#3527f5")
st.image(edu_img, caption="Education Journey", use_container_width=True)

# Education details with enhanced timeline
education = [
    {
        "degree": "Bachelor of Engineering in Computer Science",
        "institution": "KSRM College of Engineering, JNTUA",
        "location": "Kadapa, Andhra Pradesh",
        "duration": "2020 - 2024",
        "grade": "8.3/10 CGPA",
        "courses": ["programming and Scripting", "Data Structures", "Algorithms", "Database Management", "Web Development", "Machine Learning"]
    },
    {
        "degree": "Intermediate (12th Grade)",
        "institution": "JCDR Junior Junior College",
        "location": "Anantapur, Andhra Pradesh",
        "duration": "2018 - 2020",
        "grade": "6.21/10 CGPA",
        "courses": ["Mathematics", "Physics", "Chemistry"]
    },
    {
        "degree": "Secondary School Certificate (10th Grade)",
        "institution": "ZP High School",
        "location": "Anantapur, Andhra Pradesh",
        "duration": "2017 - 2018",
        "grade": "9.0/10 GPA",
        "courses": ["Mathematics", "Science", "Languages"]
    }
]

for i, edu in enumerate(education):
    st.markdown(f"""
    <div class="timeline-item fade-in" style="animation-delay: {i * 0.2}s">
        <div class="timeline-dot"></div>
        <div class="timeline-date">{edu["duration"]}</div>
        <div class="timeline-content custom-card">
            <h3>{edu["degree"]}</h3>
            <h4>{edu["institution"]}, {edu["location"]}</h4>
            <div class="education-grade">
                <span><i class="fas fa-star"></i> {edu["grade"]}</span>
            </div>
            <div class="key-courses" style="margin-top: 10px;">
                <h5>Key Courses:</h5>
                <p>{", ".join(edu["courses"])}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Certifications & Trainings with enhanced cards
st.markdown("<div class='section-header'><h2>Certifications & Trainings</h2></div>", unsafe_allow_html=True)

certifications = [
    {
        "title": "Certification of Completion Of WBL Internship [Data Analyst with Python]",
        "issuer": "C-DAC, Hyderabad",
        "date": "28-April-2025"
    },
    {
       "title": "Certification of Completion, Python 3.X-Programming Course (Hands-On)",
       "issuer": "Skill Rack",
       "date": "02-August-2022" 
    },
    {
       "title": "Certification of Completion Python-STARTER",
       "issuer": "SKill Rack", 
       "date": "03-August-2022"
    },
    {
       "title": "Certfifcation of Completion PYTHON3.X - 50 VERY-EASY CHALLENGES", 
       "issuer": "Skill Rack",
       "date": "03-August-2022"
    }
]

col1, col2 = st.columns(2)

for i, cert in enumerate(certifications):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"""
        <div class="custom-card fade-in" style="animation-delay: {i * 0.2}s">
            <h4>{cert["title"]}</h4>
            <p><i class="fas fa-certificate" style="color: #5846f6;"></i> {cert["issuer"]} | {cert["date"]}</p>
        </div>
        """, unsafe_allow_html=True)

# Languages with enhanced cards
st.markdown("<div class='section-header'><h2>Languages</h2></div>", unsafe_allow_html=True)

languages = [
    {"name": "English", "proficiency": "Professional", "icon": "fas fa-comment-dots"},
    {"name": "Telugu", "proficiency": "Native", "icon": "fas fa-comments"},
    {"name": "Hindi", "proficiency": "Intermediate", "icon": "fas fa-comment-alt"}
]

cols = st.columns(3)

for i, lang in enumerate(languages):
    with cols[i]:
        st.markdown(f"""
        <div class="language-card fade-in" style="animation-delay: {i * 0.2}s">
            <div class="language-icon">
                <i class="{lang['icon']}"></i>
            </div>
            <h4>{lang["name"]}</h4>
            <p>{lang["proficiency"]}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# SECTION 5: Contact Me
st.markdown('<div class="section" id="contact">', unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Contact Me</h2></div>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    # Enhanced contact form with validation
    st.markdown("<h3>Send me a message</h3>", unsafe_allow_html=True)
    
    # Initialize session state variables for form validation
    if 'name_error' not in st.session_state:
        st.session_state.name_error = ""
    if 'email_error' not in st.session_state:
        st.session_state.email_error = ""
    if 'message_error' not in st.session_state:
        st.session_state.message_error = ""
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    
    # Show success message if form has been submitted
    if st.session_state.form_submitted:
        st.markdown('<div class="form-success">Thank you for your message! I will get back to you soon.</div>', unsafe_allow_html=True)
        st.session_state.form_submitted = False
    
    # Create form
    with st.form("contact_form", clear_on_submit=True):
        # Name field with validation feedback
        st.markdown('<label class="required-field">Name</label>', unsafe_allow_html=True)
        name = st.text_input("", placeholder="Your name", key="name")
        if st.session_state.name_error:
            st.markdown(f'<div class="form-error">{st.session_state.name_error}</div>', unsafe_allow_html=True)
        
        # Email field with validation feedback
        st.markdown('<label class="required-field">Email</label>', unsafe_allow_html=True)
        email = st.text_input("", placeholder="Your email", key="email")
        if st.session_state.email_error:
            st.markdown(f'<div class="form-error">{st.session_state.email_error}</div>', unsafe_allow_html=True)
        
        # Message field with validation feedback
        st.markdown('<label class="required-field">Message</label>', unsafe_allow_html=True)
        message = st.text_area("", placeholder="Your message", height=150, key="message")
        if st.session_state.message_error:
            st.markdown(f'<div class="form-error">{st.session_state.message_error}</div>', unsafe_allow_html=True)
        
        # Enhanced submit button
        submitted = st.form_submit_button("🚀 Send Message")
        
        # Form validation
        if submitted:
            # Reset error messages
            st.session_state.name_error = ""
            st.session_state.email_error = ""
            st.session_state.message_error = ""
            
            # Validate fields
            valid_form = True
            if not name.strip():
                st.session_state.name_error = "Please enter your name."
                valid_form = False
            
            if not email.strip():
                st.session_state.email_error = "Please enter your email."
                valid_form = False
            elif not is_valid_email(email):
                st.session_state.email_error = "Please enter a valid email address."
                valid_form = False
            
            if not message.strip():
                st.session_state.message_error = "Please enter your message."
                valid_form = False
            
            # Process form if valid
            if valid_form:
                # Save message to database
                save_message_to_db(name, email, message)
                
                # Send email notification (optional)
                try:
                    send_email_notification(name, email, message)
                except Exception as e:
                    st.warning(f"Email notification could not be sent: {e}")
                
                # Set success message flag
                st.session_state.form_submitted = True
                
                # Rerun to show success message
                st.rerun()

with col2:
    st.markdown("### 📱 Contact Information")
   
    # Enhanced contact items
    st.markdown("""
    <div class="contact-item fade-in">
        <i class="fas fa-map-marker-alt"></i>
        <div>
            <h4>📍 Location</h4>
            <p>Anantapur, Andhra Pradesh, India</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="contact-item fade-in" style="animation-delay: 0.1s">
        <i class="fas fa-envelope"></i>
        <div>
            <h4>✉️ Email</h4>
            <p>mahendraragimanu2@gmail.com</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="contact-item fade-in" style="animation-delay: 0.2s">
        <i class="fas fa-phone"></i>
        <div>
            <h4>☎️ Phone</h4>
            <p>+91 8106442744</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
   
    # Enhanced social links
    st.markdown("### 🔗 Connect With Me")
    social_cols = st.columns(3)
   
    with social_cols[0]:
        st.markdown("""
        <div class="social-links">
            <a href="https://www.linkedin.com/in/sivamahendranath-ragimanu-68a94823b/" target="_blank">
                <i class="fab fa-linkedin fa-2x"></i>
            </a>
        </div>
        """, unsafe_allow_html=True)
   
    with social_cols[1]:
        st.markdown("""
        <div class="social-links">
            <a href="https://github.com/Sivamahendranath" target="_blank">
                <i class="fab fa-github fa-2x"></i>
            </a>
        </div>
        """, unsafe_allow_html=True)
   
    with social_cols[2]:
        st.markdown("""
        <div class="social-links">
            <a href="mailto:mahendraragimanu2@gmail.com" target="_blank">
                <i class="fas fa-envelope fa-2x"></i>
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Footer
st.markdown("""
<div class="footer fade-in">
    <p>© 2025 Sivamahendranath Ragimanu | Crafted with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)

# NEW: Add interactive elements
# Add a fun interactive element - Skill Level Visualization
with st.sidebar.expander("🎯 Skill Visualization"):
    skills_data = {
        'Python': 90,
        'Machine Learning': 85,
        'Data Analysis': 88,
        'Streamlit': 82,
        'SQL': 80,
        'NLP': 75
    }
    
    for skill, level in skills_data.items():
        st.markdown(f"""
        <div style="margin: 10px 0;">
            <div style="display: flex; justify-content: space-between;">
                <span>{skill}</span>
                <span>{level}%</span>
            </div>
            <div style="background: #e0e0e0; border-radius: 10px; height: 8px;">
                <div style="background: linear-gradient(90deg, #5846f6, #e73c7e); width: {level}%; height: 8px; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# NEW: Add a theme toggle for light/dark mode
with st.sidebar.expander("🌙 Theme Settings"):
    dark_mode = st.checkbox("Dark Mode", value=False)
    if dark_mode:
        st.markdown("""
        <style>
        .stApp {
            background: #0a192f;
            color: #e6f1ff;
        }
        </style>
        """, unsafe_allow_html=True)
