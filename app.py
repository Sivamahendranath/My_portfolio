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
from streamlit.components.v1 import html

# Page configuration
st.set_page_config(
    page_title="Sivamahendranath Ragimanu | AI Portfolio",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# NEW: Enhanced session state initialization
if 'theme' not in st.session_state:
    st.session_state.theme = "light"
if 'animations_enabled' not in st.session_state:
    st.session_state.animations_enabled = True
if 'particles_loaded' not in st.session_state:
    st.session_state.particles_loaded = False

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

# Generate placeholder images programmatically
def get_placeholder_image(width, height, color="#5846f6"):
    """Generate a placeholder image using PIL"""
    img = Image.new('RGB', (width, height), color=color)
    return img

# Function to save message to database
def save_message_to_db(name, email, message):
    """Save contact message to a JSON file"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    message_data = {
        "name": name,
        "email": email,
        "message": message,
        "timestamp": timestamp,
        "read": False
    }
    
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
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        recipient_email = os.getenv("RECIPIENT_EMAIL", "mahendraragimanu2@gmail.com")
        
        if not all([sender_email, sender_password, recipient_email]):
            st.warning("Email credentials not configured properly. Email notification not sent.")
            return False
        
        subject = f"New Portfolio Contact from {name}"
        email_message = MIMEMultipart()
        email_message["From"] = sender_email
        email_message["To"] = recipient_email
        email_message["Subject"] = subject
        
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
        
        email_message.attach(MIMEText(html_content, "html"))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
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

# NEW: Advanced Particle Animation with Three.js
def create_threejs_particles():
    """Create advanced 3D particle animation using Three.js"""
    threejs_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            #three-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: -1;
                background: linear-gradient(135deg, #0a192f 0%, #1a365d 100%);
            }
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="three-container"></div>
        <script>
            // Three.js Particle System
            const scene = new THREE.Scene();
            const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            const renderer = new THREE.WebGLRenderer({ alpha: true });
            
            renderer.setSize(window.innerWidth, window.innerHeight);
            renderer.setClearColor(0x000000, 0);
            document.getElementById('three-container').appendChild(renderer.domElement);
            
            // Create particles
            const particlesGeometry = new THREE.BufferGeometry();
            const particlesCount = 1500;
            
            const posArray = new Float32Array(particlesCount * 3);
            const colorsArray = new Float32Array(particlesCount * 3);
            
            for(let i = 0; i < particlesCount * 3; i++) {
                posArray[i] = (Math.random() - 0.5) * 10;
                colorsArray[i] = Math.random();
            }
            
            particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));
            particlesGeometry.setAttribute('color', new THREE.BufferAttribute(colorsArray, 3));
            
            const particlesMaterial = new THREE.PointsMaterial({
                size: 0.02,
                vertexColors: true,
                transparent: true,
                opacity: 0.8
            });
            
            const particlesMesh = new THREE.Points(particlesGeometry, particlesMaterial);
            scene.add(particlesMesh);
            
            camera.position.z = 5;
            
            // Mouse interaction
            let mouseX = 0;
            let mouseY = 0;
            
            document.addEventListener('mousemove', (event) => {
                mouseX = (event.clientX / window.innerWidth) * 2 - 1;
                mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
            });
            
            // Animation
            function animate() {
                requestAnimationFrame(animate);
                
                particlesMesh.rotation.x += 0.001;
                particlesMesh.rotation.y += 0.002;
                
                // Mouse interaction
                particlesMesh.rotation.x += mouseY * 0.0005;
                particlesMesh.rotation.y += mouseX * 0.0005;
                
                renderer.render(scene, camera);
            }
            
            animate();
            
            // Handle resize
            window.addEventListener('resize', () => {
                camera.aspect = window.innerWidth / window.innerHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(window.innerWidth, window.innerHeight);
            });
        </script>
    </body>
    </html>
    """
    return threejs_html

# NEW: Advanced Gradient Animation
def create_advanced_gradient():
    """Create multi-layered gradient animation"""
    gradient_css = """
    <style>
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab, #5846f6);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        position: relative;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
        animation: float 20s ease-in-out infinite;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """
    return gradient_css

# NEW: Advanced Animation System
def create_advanced_animations():
    """Create comprehensive animation system"""
    animations_css = """
    <style>
    /* Advanced Keyframe Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translate3d(0, 40px, 0);
        }
        to {
            opacity: 1;
            transform: translate3d(0, 0, 0);
        }
    }
    
    @keyframes fadeInLeft {
        from {
            opacity: 0;
            transform: translate3d(-40px, 0, 0);
        }
        to {
            opacity: 1;
            transform: translate3d(0, 0, 0);
        }
    }
    
    @keyframes fadeInRight {
        from {
            opacity: 0;
            transform: translate3d(40px, 0, 0);
        }
        to {
            opacity: 1;
            transform: translate3d(0, 0, 0);
        }
    }
    
    @keyframes bounceIn {
        from, 20%, 40%, 60%, 80%, to {
            animation-timing-function: cubic-bezier(0.215, 0.610, 0.355, 1.000);
        }
        0% {
            opacity: 0;
            transform: scale3d(.3, .3, .3);
        }
        20% {
            transform: scale3d(1.1, 1.1, 1.1);
        }
        40% {
            transform: scale3d(.9, .9, .9);
        }
        60% {
            opacity: 1;
            transform: scale3d(1.03, 1.03, 1.03);
        }
        80% {
            transform: scale3d(.97, .97, .97);
        }
        to {
            opacity: 1;
            transform: scale3d(1, 1, 1);
        }
    }
    
    @keyframes slideInUp {
        from {
            transform: translate3d(0, 100%, 0);
            visibility: visible;
            opacity: 0;
        }
        to {
            transform: translate3d(0, 0, 0);
            opacity: 1;
        }
    }
    
    @keyframes pulseGlow {
        0% {
            box-shadow: 0 0 5px rgba(88, 70, 246, 0.5);
        }
        50% {
            box-shadow: 0 0 20px rgba(88, 70, 246, 0.8);
        }
        100% {
            box-shadow: 0 0 5px rgba(88, 70, 246, 0.5);
        }
    }
    
    @keyframes typewriter {
        from { width: 0; }
        to { width: 100%; }
    }
    
    @keyframes blinkCursor {
        from, to { border-color: transparent; }
        50% { border-color: #5846f6; }
    }
    
    /* Animation Classes */
    .animate-fadeInUp {
        animation: fadeInUp 0.8s ease-out;
    }
    
    .animate-fadeInLeft {
        animation: fadeInLeft 0.8s ease-out;
    }
    
    .animate-fadeInRight {
        animation: fadeInRight 0.8s ease-out;
    }
    
    .animate-bounceIn {
        animation: bounceIn 1s ease-out;
    }
    
    .animate-slideInUp {
        animation: slideInUp 0.8s ease-out;
    }
    
    .animate-pulseGlow {
        animation: pulseGlow 2s infinite;
    }
    
    .typewriter {
        overflow: hidden;
        border-right: 3px solid #5846f6;
        white-space: nowrap;
        margin: 0 auto;
        animation: typewriter 3.5s steps(40, end), blinkCursor 0.75s step-end infinite;
    }
    
    /* Staggered Animations */
    .stagger-item {
        opacity: 0;
    }
    
    .stagger-visible .stagger-item {
        animation: fadeInUp 0.6s ease forwards;
    }
    
    /* Hover Effects */
    .hover-lift {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .hover-lift:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .hover-glow:hover {
        box-shadow: 0 0 20px rgba(88, 70, 246, 0.4);
    }
    
    .hover-scale {
        transition: all 0.3s ease;
    }
    
    .hover-scale:hover {
        transform: scale(1.05);
    }
    
    /* Glass Morphism */
    .glass-effect {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(45deg, #5846f6, #e73c7e, #23a6d5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 200% 200%;
        animation: gradient 3s ease infinite;
    }
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Parallax Scrolling Effect */
    .parallax {
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
    }
    </style>
    """
    return animations_css

# NEW: Interactive Background Selector
def create_background_selector():
    """Create interactive background selection system"""
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🎨 Visual Effects")
        
        background_options = {
            "Particle Universe": "particle",
            "Gradient Flow": "gradient", 
            "Cyber Grid": "cyber",
            "Minimal Light": "minimal"
        }
        
        selected_bg = st.selectbox(
            "Choose Background",
            list(background_options.keys()),
            index=1
        )
        
        # Animation intensity
        animation_intensity = st.slider("Animation Intensity", 0, 100, 50)
        
        # Color scheme
        color_scheme = st.selectbox("Color Scheme", ["Purple Blue", "Sunset", "Ocean", "Forest"])
        
        return background_options[selected_bg], animation_intensity, color_scheme

# NEW: Advanced Navigation System
def create_advanced_navigation():
    """Create sticky navigation with smooth scrolling"""
    nav_html = """
    <style>
    .sticky-nav {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        z-index: 1000;
        padding: 1rem 0;
        box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .nav-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 2rem;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
    }
    
    .nav-link {
        color: #333;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .nav-link:hover {
        color: #5846f6;
    }
    
    .nav-link::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 0;
        width: 0;
        height: 2px;
        background: #5846f6;
        transition: width 0.3s ease;
    }
    
    .nav-link:hover::after {
        width: 100%;
    }
    
    .nav-scrolled {
        padding: 0.5rem 0;
        background: rgba(255, 255, 255, 0.98);
    }
    </style>
    
    <nav class="sticky-nav" id="mainNav">
        <div class="nav-container">
            <div class="nav-brand">
                <strong>Sivamahendranath</strong>
            </div>
            <div class="nav-links">
                <a href="#home" class="nav-link">Home</a>
                <a href="#skills" class="nav-link">Skills</a>
                <a href="#projects" class="nav-link">Projects</a>
                <a href="#education" class="nav-link">Education</a>
                <a href="#contact" class="nav-link">Contact</a>
            </div>
        </div>
    </nav>
    
    <script>
    window.addEventListener('scroll', function() {
        const nav = document.getElementById('mainNav');
        if (window.scrollY > 100) {
            nav.classList.add('nav-scrolled');
        } else {
            nav.classList.remove('nav-scrolled');
        }
    });
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    </script>
    """
    return nav_html

# NEW: Enhanced Progress Indicator
def create_enhanced_progress():
    """Create enhanced scroll progress indicator"""
    progress_html = """
    <style>
    .progress-container {
        width: 100%;
        height: 6px;
        background: linear-gradient(90deg, rgba(88, 70, 246, 0.1) 0%, rgba(231, 60, 126, 0.1) 100%);
        position: fixed;
        top: 0;
        left: 0;
        z-index: 9999;
    }
    
    .progress-bar {
        height: 6px;
        background: linear-gradient(90deg, #5846f6, #e73c7e, #23a6d5);
        width: 0%;
        transition: width 0.1s ease;
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    </style>
    
    <div class="progress-container">
        <div class="progress-bar" id="progressBar"></div>
    </div>
    
    <script>
    window.addEventListener('scroll', function() {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        document.getElementById("progressBar").style.width = scrolled + "%";
    });
    </script>
    """
    return progress_html

# NEW: Interactive Skill Visualization
def create_skill_visualization():
    """Create interactive 3D skill visualization"""
    skill_viz_html = """
    <div style="background: linear-gradient(135deg, rgba(88, 70, 246, 0.1) 0%, rgba(231, 60, 126, 0.1) 100%); 
                padding: 2rem; border-radius: 15px; margin: 2rem 0;">
        <h3 style="text-align: center; margin-bottom: 2rem;">🚀 Skill Radar</h3>
        <div id="skill-chart" style="height: 400px;"></div>
    </div>
    
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script>
    const skillsData = {
        type: 'scatterpolar',
        r: [90, 85, 88, 82, 80, 75, 70, 78],
        theta: ['Python', 'ML', 'Data Analysis', 'Streamlit', 'SQL', 'NLP', 'Java', 'JavaScript'],
        fill: 'toself',
        fillcolor: 'rgba(88, 70, 246, 0.3)',
        line: {
            color: 'rgba(88, 70, 246, 0.8)'
        }
    };
    
    const layout = {
        polar: {
            radialaxis: {
                visible: true,
                range: [0, 100]
            }
        },
        showlegend: false,
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)'
    };
    
    Plotly.newPlot('skill-chart', [skillsData], layout, {displayModeBar: false});
    </script>
    """
    return skill_viz_html

# Apply all enhanced styles and components
st.markdown(create_advanced_animations(), unsafe_allow_html=True)
st.markdown(create_advanced_navigation(), unsafe_allow_html=True)
st.markdown(create_enhanced_progress(), unsafe_allow_html=True)

# Include Font Awesome and other libraries
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Enhanced Sidebar with Theme Controls
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2>🎨 Design Studio</h2>
        <p>Customize your viewing experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Background selection
    bg_type, intensity, color_scheme = create_background_selector()
    
    # Animation controls
    st.markdown("### ⚡ Animations")
    enable_animations = st.checkbox("Enable All Animations", value=True)
    animation_speed = st.select_slider("Animation Speed", options=["Slow", "Normal", "Fast"], value="Normal")
    
    # Theme selection
    st.markdown("### 🌙 Theme")
    theme = st.radio("Select Theme", ["Light Mode", "Dark Mode", "Auto"], horizontal=True)
    
    # Social links
    st.markdown("---")
    st.markdown("### 🔗 Connect")
    social_cols = st.columns(4)
    with social_cols[0]:
        st.markdown('<a href="https://www.linkedin.com/in/sivamahendranath-ragimanu-68a94823b/" target="_blank"><i class="fab fa-linkedin fa-lg"></i></a>', unsafe_allow_html=True)
    with social_cols[1]:
        st.markdown('<a href="https://github.com/Sivamahendranath" target="_blank"><i class="fab fa-github fa-lg"></i></a>', unsafe_allow_html=True)
    with social_cols[2]:
        st.markdown('<a href="mailto:mahendraragimanu2@gmail.com" target="_blank"><i class="fas fa-envelope fa-lg"></i></a>', unsafe_allow_html=True)
    with social_cols[3]:
        st.markdown('<a href="#contact" onclick="document.querySelector(\'[href=\\\"#contact\\\"]\').click()"><i class="fas fa-comment fa-lg"></i></a>', unsafe_allow_html=True)

# Apply selected background
if bg_type == "particle":
    html(create_threejs_particles(), height=0, width=0)
elif bg_type == "gradient":
    st.markdown(create_advanced_gradient(), unsafe_allow_html=True)
elif bg_type == "cyber":
    st.markdown("""
    <style>
    .stApp {
        background: 
            radial-gradient(circle at 20% 80%, rgba(88, 70, 246, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(231, 60, 126, 0.1) 0%, transparent 50%),
            linear-gradient(45deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        background-attachment: fixed;
    }
    </style>
    """, unsafe_allow_html=True)

# Enhanced CSS with all animations and effects
st.markdown(f"""
<style>
    /* Enhanced Base Styles */
    .stApp {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Hero Section with Advanced Effects */
    .hero-section {{
        position: relative;
        padding: 4rem 0;
        background: linear-gradient(135deg, rgba(88, 70, 246, 0.1) 0%, rgba(231, 60, 126, 0.1) 50%, rgba(35, 166, 213, 0.1) 100%);
        border-radius: 20px;
        margin: 2rem 0;
        overflow: hidden;
    }}
    
    .hero-section::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(88, 70, 246, 0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }}
    
    @keyframes rotate {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}
    
    .hero-content {{
        position: relative;
        z-index: 2;
    }}
    
    .hero-title {{
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(45deg, #5846f6, #e73c7e, #23a6d5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        line-height: 1.1;
    }}
    
    .hero-subtitle {{
        font-size: 1.5rem;
        color: #666;
        margin-bottom: 2rem;
        font-weight: 300;
    }}
    
    /* Enhanced Cards */
    .enhanced-card {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.6);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .enhanced-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.5s;
    }}
    
    .enhanced-card:hover::before {{
        left: 100%;
    }}
    
    .enhanced-card:hover {{
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.15),
            0 0 80px rgba(88, 70, 246, 0.1);
    }}
    
    /* Skill Bars with Animation */
    .skill-container {{
        margin: 1.5rem 0;
    }}
    
    .skill-header {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }}
    
    .skill-bar {{
        height: 12px;
        background: rgba(88, 70, 246, 0.1);
        border-radius: 10px;
        overflow: hidden;
        position: relative;
    }}
    
    .skill-progress {{
        height: 100%;
        background: linear-gradient(90deg, #5846f6, #e73c7e);
        border-radius: 10px;
        transform: scaleX(0);
        transform-origin: left;
        animation: growSkill 1.5s ease-out forwards;
        position: relative;
    }}
    
    .skill-progress::after {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        animation: shimmer 2s infinite;
    }}
    
    @keyframes growSkill {{
        to {{ transform: scaleX(1); }}
    }}
    
    /* Project Grid */
    .project-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }}
    
    .project-card {{
        background: white;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 0, 0, 0.05);
    }}
    
    .project-card:hover {{
        transform: translateY(-10px);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.15);
    }}
    
    .project-image {{
        width: 100%;
        height: 200px;
        object-fit: cover;
        transition: transform 0.3s ease;
    }}
    
    .project-card:hover .project-image {{
        transform: scale(1.05);
    }}
    
    .project-content {{
        padding: 1.5rem;
    }}
    
    .project-tech {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 1rem 0;
    }}
    
    .tech-tag {{
        background: linear-gradient(135deg, #5846f6, #e73c7e);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
    }}
    
    /* Contact Form Enhancements */
    .contact-form {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }}
    
    .form-group {{
        margin-bottom: 1.5rem;
    }}
    
    .form-input {{
        width: 100%;
        padding: 1rem;
        border: 2px solid rgba(88, 70, 246, 0.1);
        border-radius: 10px;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.8);
    }}
    
    .form-input:focus {{
        outline: none;
        border-color: #5846f6;
        box-shadow: 0 0 0 3px rgba(88, 70, 246, 0.1);
        transform: translateY(-2px);
    }}
    
    .submit-btn {{
        background: linear-gradient(135deg, #5846f6, #e73c7e);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
    }}
    
    .submit-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(88, 70, 246, 0.3);
    }}
    
    /* Section Headers */
    .section-header {{
        text-align: center;
        margin: 4rem 0 2rem 0;
        position: relative;
    }}
    
    .section-title {{
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(45deg, #5846f6, #e73c7e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: inline-block;
    }}
    
    .section-subtitle {{
        color: #666;
        font-size: 1.2rem;
        margin-top: 0.5rem;
    }}
    
    /* Achievement Badges */
    .achievement-badge {{
        display: inline-flex;
        align-items: center;
        background: linear-gradient(135deg, rgba(88, 70, 246, 0.1), rgba(231, 60, 126, 0.1));
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.5rem;
        font-weight: 500;
        border: 1px solid rgba(88, 70, 246, 0.2);
    }}
    
    /* Responsive Design */
    @media (max-width: 768px) {{
        .hero-title {{
            font-size: 2.5rem;
        }}
        
        .project-grid {{
            grid-template-columns: 1fr;
        }}
        
        .section-title {{
            font-size: 2rem;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# MAIN CONTENT WITH ENHANCED SECTIONS

# SECTION 1: Enhanced Hero Section
st.markdown("""
<div class="hero-section animate-fadeInUp">
    <div class="hero-content">
        <div style="max-width: 1200px; margin: 0 auto; padding: 0 2rem;">
            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 4rem; align-items: center;">
                <div>
                    <h1 class="hero-title">Sivamahendranath Ragimanu</h1>
                    <h2 class="hero-subtitle">🎓 Computer Science Graduate | AI Engineer | Data Scientist</h2>
                    <p style="font-size: 1.2rem; line-height: 1.6; color: #555; margin-bottom: 2rem;">
                        Passionate about building intelligent systems that transform data into actionable insights. 
                        Specialized in AI, Machine Learning, and creating scalable data solutions.
                    </p>
                    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                        <button onclick="document.querySelector('[href=\\'#projects\\']').click()" 
                                style="background: linear-gradient(135deg, #5846f6, #e73c7e); color: white; border: none; padding: 1rem 2rem; border-radius: 10px; font-weight: 600; cursor: pointer; transition: all 0.3s ease;">
                            🚀 View My Work
                        </button>
                        <button onclick="document.querySelector('[href=\\'#contact\\']').click()" 
                                style="background: transparent; color: #5846f6; border: 2px solid #5846f6; padding: 1rem 2rem; border-radius: 10px; font-weight: 600; cursor: pointer; transition: all 0.3s ease;">
                            📞 Get In Touch
                        </button>
                    </div>
                </div>
                <div style="text-align: center;">
                    <div style="width: 300px; height: 300px; border-radius: 50%; overflow: hidden; margin: 0 auto; border: 4px solid #5846f6; box-shadow: 0 20px 40px rgba(88, 70, 246, 0.3);" class="floating">
""", unsafe_allow_html=True)

# Profile Image
profile_image_path = get_image_path("profile.jpeg")
if os.path.exists(profile_image_path):
    profile_img = load_image(profile_image_path)
else:
    profile_img = get_placeholder_image(300, 300, color="#5846f6")
st.image(profile_img, use_container_width=True, output_format="PNG")

st.markdown("""
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# SECTION 2: Enhanced Skills Section
st.markdown("""
<div id="skills" class="section-header animate-fadeInUp" style="animation-delay: 0.2s">
    <h1 class="section-title">Technical Excellence</h1>
    <p class="section-subtitle">Technologies I work with to bring ideas to life</p>
</div>
""", unsafe_allow_html=True)

# Skills Visualization
html(create_skill_visualization(), height=450)

# Skills in enhanced cards
skills_data = {
    "AI & Machine Learning": ["Python", "TensorFlow", "PyTorch", "Scikit-learn", "LLMs", "RAG Pipelines"],
    "Data Science": ["Pandas", "NumPy", "Data Visualization", "Statistical Analysis", "SQL"],
    "Web Development": ["Streamlit", "HTML/CSS", "JavaScript", "Flask"],
    "Tools & Technologies": ["Git", "Docker", "SQLite", "OpenCV", "BeautifulSoup"]
}

cols = st.columns(2)
for i, (category, skills) in enumerate(skills_data.items()):
    with cols[i % 2]:
        st.markdown(f"""
        <div class="enhanced-card hover-lift">
            <h3 style="color: #5846f6; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
                <i class="fas fa-star"></i> {category}
            </h3>
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
        """, unsafe_allow_html=True)
        
        for skill in skills:
            st.markdown(f'<span class="achievement-badge">{skill}</span>', unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

# SECTION 3: Enhanced Projects Section
st.markdown("""
<div id="projects" class="section-header animate-fadeInUp" style="animation-delay: 0.4s">
    <h1 class="section-title">Innovative Projects</h1>
    <p class="section-subtitle">Showcasing my technical expertise and creative solutions</p>
</div>
""", unsafe_allow_html=True)

# Projects data
projects = [
    {
        "title": "AI-Powered Knowledge Graph Explorer",
        "description": "Advanced knowledge graph generation using LLMs with interactive visualization",
        "image": "knowledge_graph.png",
        "technologies": ["Python", "Streamlit", "Google Gemini API", "SQLite3", "NetworkX"],
        "github": "https://github.com/Sivamahendranath/Gemini_Knowledge_Graph"
    },
    {
        "title": "DocuGenius Pro", 
        "description": "AI-powered document processing and analysis platform",
        "image": "docugenius.png",
        "technologies": ["Python", "Streamlit", "Google Gemini API", "NLP", "Plotly"],
        "github": "https://github.com/Sivamahendranath/Gemini-Document-RAG"
    },
    {
        "title": "Student Performance Dashboard",
        "description": "Comprehensive data visualization for educational analytics",
        "image": "student_dashboard.png", 
        "technologies": ["Python", "Pandas", "Matplotlib", "Seaborn", "Data Analysis"],
        "github": "https://github.com/Sivamahendranath/Student-Performance-Dashboard"
    }
]

# Display projects in enhanced grid
st.markdown('<div class="project-grid">', unsafe_allow_html=True)
for project in projects:
    st.markdown(f"""
    <div class="project-card hover-lift">
        <div style="height: 200px; background: linear-gradient(135deg, #5846f6, #e73c7e); display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem;">
            <i class="fas fa-project-diagram"></i>
        </div>
        <div class="project-content">
            <h3 style="color: #333; margin-bottom: 1rem;">{project['title']}</h3>
            <p style="color: #666; line-height: 1.6; margin-bottom: 1.5rem;">{project['description']}</p>
            <div class="project-tech">
                {"".join([f'<span class="tech-tag">{tech}</span>' for tech in project['technologies']])}
            </div>
            <div style="margin-top: 1.5rem;">
                <a href="{project['github']}" target="_blank" 
                   style="display: inline-flex; align-items: center; gap: 0.5rem; color: #5846f6; text-decoration: none; font-weight: 600;">
                    <i class="fab fa-github"></i> View Code
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# SECTION 4: Enhanced Contact Section
st.markdown("""
<div id="contact" class="section-header animate-fadeInUp" style="animation-delay: 0.6s">
    <h1 class="section-title">Let's Connect</h1>
    <p class="section-subtitle">Ready to bring your ideas to life? Get in touch!</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="contact-form animate-fadeInLeft">
        <h3 style="color: #333; margin-bottom: 2rem;">Send me a message</h3>
    """, unsafe_allow_html=True)
    
    # Enhanced contact form
    with st.form("enhanced_contact_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Your Name", placeholder="Enter your full name")
        with col2:
            email = st.text_input("📧 Email Address", placeholder="your.email@example.com")
        
        message = st.text_area("💬 Your Message", 
                             placeholder="Tell me about your project or how I can help you...", 
                             height=150)
        
        submitted = st.form_submit_button("🚀 Send Message", use_container_width=True)
        
        if submitted:
            if name and email and message:
                if is_valid_email(email):
                    save_message_to_db(name, email, message)
                    try:
                        send_email_notification(name, email, message)
                    except Exception as e:
                        st.warning(f"Message saved but email notification failed: {e}")
                    
                    st.success("🎉 Message sent successfully! I'll get back to you soon.")
                else:
                    st.error("📧 Please enter a valid email address.")
            else:
                st.error("❌ Please fill in all required fields.")

with col2:
    st.markdown("""
    <div class="enhanced-card" style="text-align: center;">
        <h3 style="color: #5846f6; margin-bottom: 2rem;">Quick Connect</h3>
        
        <div style="display: flex; flex-direction: column; gap: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: rgba(88, 70, 246, 0.05); border-radius: 10px;">
                <i class="fas fa-map-marker-alt" style="color: #5846f6; font-size: 1.5rem;"></i>
                <div style="text-align: left;">
                    <strong>Location</strong>
                    <div style="color: #666;">Anantapur, AP</div>
                </div>
            </div>
            
            <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: rgba(88, 70, 246, 0.05); border-radius: 10px;">
                <i class="fas fa-envelope" style="color: #5846f6; font-size: 1.5rem;"></i>
                <div style="text-align: left;">
                    <strong>Email</strong>
                    <div style="color: #666;">mahendraragimanu2@gmail.com</div>
                </div>
            </div>
            
            <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: rgba(88, 70, 246, 0.05); border-radius: 10px;">
                <i class="fas fa-phone" style="color: #5846f6; font-size: 1.5rem;"></i>
                <div style="text-align: left;">
                    <strong>Phone</strong>
                    <div style="color: #666;">+91 8106442744</div>
                </div>
            </div>
        </div>
        
        <div style="margin-top: 2rem; display: flex; justify-content: center; gap: 1rem;">
            <a href="https://www.linkedin.com/in/sivamahendranath-ragimanu-68a94823b/" target="_blank" 
               style="color: #5846f6; font-size: 1.5rem; transition: all 0.3s ease;" class="hover-scale">
                <i class="fab fa-linkedin"></i>
            </a>
            <a href="https://github.com/Sivamahendranath" target="_blank" 
               style="color: #5846f6; font-size: 1.5rem; transition: all 0.3s ease;" class="hover-scale">
                <i class="fab fa-github"></i>
            </a>
            <a href="mailto:mahendraragimanu2@gmail.com" 
               style="color: #5846f6; font-size: 1.5rem; transition: all 0.3s ease;" class="hover-scale">
                <i class="fas fa-envelope"></i>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Enhanced Footer
st.markdown("""
<div style="text-align: center; padding: 4rem 0 2rem 0; color: #666; margin-top: 4rem;">
    <div style="font-size: 3rem; margin-bottom: 1rem;">🚀</div>
    <h3 style="color: #333; margin-bottom: 1rem;">Ready to Build Something Amazing?</h3>
    <p style="margin-bottom: 2rem;">Let's collaborate to turn your ideas into reality</p>
    <div style="height: 1px; background: linear-gradient(90deg, transparent, #5846f6, transparent); margin: 2rem 0;"></div>
    <p>© 2025 Sivamahendranath Ragimanu. Crafted with ❤️ using Streamlit & Advanced AI</p>
</div>
""", unsafe_allow_html=True)

# NEW: Performance optimization and production readiness
st.markdown("""
<script>
// Performance optimization
document.addEventListener('DOMContentLoaded', function() {
    // Lazy loading for images
    const images = document.querySelectorAll('img');
    const imageOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px 50px 0px'
    };
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                imageObserver.unobserve(img);
            }
        });
    }, imageOptions);
    
    images.forEach(img => imageObserver.observe(img));
    
    // Smooth scrolling polyfill
    if (!('scrollBehavior' in document.documentElement.style)) {
        const smoothScroll = function(target) {
            const element = document.querySelector(target);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        };
        
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();
                smoothScroll(this.getAttribute('href'));
            });
        });
    }
});
</script>
""", unsafe_allow_html=True)
