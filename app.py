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

st.set_page_config(page_title="Sivamahendranath Ragimanu | Portfolio",page_icon="👨‍💻",layout="wide",initial_sidebar_state="expanded")

def get_image_path(relative_path):
    base_path = Path(__file__).parent / "images"
    return str(base_path / relative_path)

def load_image(image_path):
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        st.warning(f"Image not found: {image_path}")
        return get_placeholder_image(400, 300, color="#5846f6")
    except Exception as e:
        st.warning(f"Error loading image {image_path}: {str(e)}")
        return get_placeholder_image(400, 300, color="#5846f6")

def get_placeholder_image(width, height, color="#5846f6"):
    img = Image.new('RGB', (width, height), color=color)
    return img

def save_message_to_db(name, email, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    message_data = {"name": name,"email": email,"message": message,"timestamp": timestamp,"read": False}
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

def send_email_notification(name, email, message):
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
        html_content = f"""<html><body><h2>New Contact Message from Your Portfolio</h2><p><strong>Name:</strong> {name}</p><p><strong>Email:</strong> {email}</p><p><strong>Message:</strong></p><p>{message}</p><hr><p><em>This is an automated notification from your portfolio website.</em></p></body></html>"""
        email_message.attach(MIMEText(html_content, "html"))
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(email_message)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

def is_valid_email(email):
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(email_pattern, email))

st.markdown("""<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">""", unsafe_allow_html=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
*{font-family:'Poppins',sans-serif;scroll-behavior:smooth;}
.stApp{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);background-attachment:fixed;}
.hero-section{background:rgba(255,255,255,0.95);padding:60px 40px;border-radius:30px;box-shadow:0 20px 60px rgba(0,0,0,0.3);backdrop-filter:blur(10px);animation:slideInUp 1s ease-out;margin-bottom:40px;position:relative;overflow:hidden;}
.hero-section::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle,rgba(88,70,246,0.1) 0%,transparent 70%);animation:rotate 20s linear infinite;}
.hero-section h1{font-size:4rem;font-weight:700;background:linear-gradient(135deg,#667eea,#764ba2);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:20px;animation:fadeInDown 1.2s ease-out;position:relative;z-index:1;}
.hero-section h3{font-size:1.8rem;color:#555;margin-bottom:25px;animation:fadeInUp 1.4s ease-out;position:relative;z-index:1;}
.lead-text{font-size:1.15rem;line-height:1.8;color:#666;animation:fadeIn 1.6s ease-out;position:relative;z-index:1;}
.section-header h2{font-size:3rem;font-weight:700;color:#fff;border-bottom:4px solid #ffd700;padding-bottom:15px;margin:50px 0 30px 0;text-shadow:2px 2px 4px rgba(0,0,0,0.3);animation:slideInLeft 1s ease-out;display:inline-block;}
.custom-card{background:rgba(255,255,255,0.95);border-left:6px solid #ffd700;padding:25px;margin:20px 0;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.2);transition:all 0.4s ease;animation:fadeInUp 0.8s ease-out;}
.custom-card:hover{transform:translateY(-10px) scale(1.02);box-shadow:0 20px 50px rgba(0,0,0,0.3);border-left-color:#667eea;}
.skill-container{background:linear-gradient(135deg,rgba(255,255,255,0.9),rgba(240,240,255,0.9));padding:20px;margin:15px 0;border-radius:12px;box-shadow:0 5px 15px rgba(0,0,0,0.1);transition:all 0.3s ease;border:2px solid transparent;}
.skill-container:hover{transform:translateX(10px);border-color:#667eea;box-shadow:0 8px 25px rgba(102,126,234,0.3);}
.skill-name{font-size:1.1rem;font-weight:600;color:#333;display:flex;align-items:center;}
.skill-name::before{content:'▸';margin-right:10px;color:#667eea;font-size:1.5rem;}
.timeline-item{position:relative;padding-left:50px;margin-bottom:40px;animation:slideInRight 0.8s ease-out;}
.timeline-dot{position:absolute;left:0;top:5px;width:25px;height:25px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);box-shadow:0 0 20px rgba(102,126,234,0.6);animation:pulse 2s infinite;}
.timeline-date{font-weight:700;color:#fff;margin-bottom:10px;font-size:1.1rem;text-shadow:1px 1px 2px rgba(0,0,0,0.2);}
.soft-skill-card{text-align:center;padding:30px;background:linear-gradient(135deg,rgba(255,255,255,0.95),rgba(240,240,255,0.95));border-radius:20px;margin:15px;box-shadow:0 10px 30px rgba(0,0,0,0.2);transition:all 0.4s ease;position:relative;overflow:hidden;}
.soft-skill-card::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:radial-gradient(circle,rgba(102,126,234,0.2) 0%,transparent 70%);transform:scale(0);transition:transform 0.6s ease;}
.soft-skill-card:hover::before{transform:scale(1);}
.soft-skill-card:hover{transform:translateY(-15px) rotate(2deg);box-shadow:0 20px 50px rgba(102,126,234,0.4);}
.soft-skill-card i{font-size:3rem;color:#667eea;margin-bottom:15px;transition:all 0.3s ease;}
.soft-skill-card:hover i{transform:scale(1.3) rotate(360deg);}
.soft-skill-card h4{color:#333;font-weight:600;font-size:1.2rem;}
.accomplishment-card{display:flex;align-items:flex-start;background:linear-gradient(135deg,rgba(255,255,255,0.95),rgba(240,255,240,0.95));padding:25px;border-radius:15px;margin-bottom:20px;box-shadow:0 8px 25px rgba(0,0,0,0.15);transition:all 0.3s ease;border-left:5px solid #ffd700;}
.accomplishment-card:hover{transform:translateX(15px);box-shadow:0 15px 40px rgba(102,126,234,0.3);}
.accomplishment-icon{font-size:2.5rem;color:#667eea;margin-right:20px;transition:transform 0.3s ease;}
.accomplishment-card:hover .accomplishment-icon{transform:rotate(360deg) scale(1.2);}
.project-details{background:rgba(255,255,255,0.95);padding:30px;border-radius:20px;box-shadow:0 15px 40px rgba(0,0,0,0.2);transition:all 0.4s ease;margin-bottom:30px;}
.project-details:hover{transform:scale(1.02);box-shadow:0 25px 60px rgba(0,0,0,0.3);}
.project-details h3{color:#667eea;font-size:2rem;margin-bottom:15px;font-weight:700;}
.project-meta{margin:20px 0;padding:15px;background:rgba(102,126,234,0.1);border-radius:10px;}
.project-meta div{margin-bottom:12px;font-size:1.05rem;color:#555;}
.project-meta i{margin-right:12px;color:#667eea;font-size:1.2rem;}
.tech-badge{display:inline-block;background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:8px 18px;margin:6px;border-radius:25px;font-weight:600;box-shadow:0 4px 10px rgba(0,0,0,0.2);transition:all 0.3s ease;}
.tech-badge:hover{transform:translateY(-5px) scale(1.1);box-shadow:0 8px 20px rgba(102,126,234,0.4);}
.language-card{text-align:center;padding:30px;background:linear-gradient(135deg,rgba(255,255,255,0.95),rgba(255,240,240,0.95));border-radius:20px;margin:15px;box-shadow:0 10px 30px rgba(0,0,0,0.2);transition:all 0.4s ease;}
.language-card:hover{transform:translateY(-10px);box-shadow:0 20px 50px rgba(0,0,0,0.3);}
.language-icon{font-size:3rem;margin-bottom:15px;color:#667eea;}
.contact-button{background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:15px 35px;border-radius:30px;text-align:center;text-decoration:none;display:inline-block;font-size:1.1rem;font-weight:600;margin:10px;cursor:pointer;border:none;transition:all 0.4s ease;box-shadow:0 10px 30px rgba(0,0,0,0.3);}
.contact-button:hover{transform:translateY(-5px);box-shadow:0 20px 50px rgba(102,126,234,0.5);}
.form-error{color:#ff4444;font-size:0.95rem;margin-top:5px;animation:shake 0.5s;}
.form-success{color:#4CAF50;padding:15px;border-radius:10px;background:rgba(76,175,80,0.15);border-left:5px solid #4CAF50;margin:15px 0;animation:slideInDown 0.6s ease-out;}
.footer{margin-top:60px;padding:30px 0;text-align:center;background:rgba(0,0,0,0.7);color:#fff;border-top:3px solid #ffd700;font-size:1.1rem;}
.profile-img{border-radius:50%;max-width:100%;border:5px solid #ffd700;box-shadow:0 15px 40px rgba(0,0,0,0.4);transition:all 0.4s ease;animation:float 3s ease-in-out infinite;}
.profile-img:hover{transform:scale(1.1) rotate(5deg);box-shadow:0 25px 60px rgba(102,126,234,0.5);}
.key-point{color:#fff;font-size:1.1rem;margin-bottom:12px;padding:10px;background:rgba(0,0,0,0.3);border-radius:8px;transition:all 0.3s ease;}
.key-point:hover{background:rgba(102,126,234,0.5);transform:translateX(10px);}
.key-point i{margin-right:12px;color:#ffd700;}
.skill-category h3{color:#fff;border-bottom:3px solid #ffd700;padding-bottom:12px;margin-bottom:20px;font-size:1.8rem;text-shadow:2px 2px 4px rgba(0,0,0,0.3);}
.skill-category-icon{font-size:2rem;margin-right:15px;color:#ffd700;}
.education-grade{margin-top:15px;padding:10px;background:rgba(255,215,0,0.2);border-radius:8px;}
.education-grade i{color:gold;}
@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}
@keyframes fadeInUp{from{opacity:0;transform:translateY(30px);}to{opacity:1;transform:translateY(0);}}
@keyframes fadeInDown{from{opacity:0;transform:translateY(-30px);}to{opacity:1;transform:translateY(0);}}
@keyframes slideInUp{from{opacity:0;transform:translateY(60px);}to{opacity:1;transform:translateY(0);}}
@keyframes slideInLeft{from{opacity:0;transform:translateX(-60px);}to{opacity:1;transform:translateX(0);}}
@keyframes slideInRight{from{opacity:0;transform:translateX(60px);}to{opacity:1;transform:translateX(0);}}
@keyframes slideInDown{from{opacity:0;transform:translateY(-30px);}to{opacity:1;transform:translateY(0);}}
@keyframes pulse{0%,100%{transform:scale(1);opacity:1;}50%{transform:scale(1.2);opacity:0.8;}}
@keyframes rotate{from{transform:rotate(0deg);}to{transform:rotate(360deg);}}
@keyframes float{0%,100%{transform:translateY(0);}50%{transform:translateY(-20px);}}
@keyframes shake{0%,100%{transform:translateX(0);}25%{transform:translateX(-10px);}75%{transform:translateX(10px);}}
.section{padding:40px 0;animation:fadeIn 1s ease-out;}
img{border-radius:15px;transition:all 0.4s ease;}
img:hover{transform:scale(1.05);box-shadow:0 15px 40px rgba(0,0,0,0.3);}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🎨 Navigation")
    st.markdown("---")
    st.markdown("### Quick Links")
    st.markdown("🏠 [Home](#home)")
    st.markdown("💼 [Skills & Experience](#skills)")
    st.markdown("🚀 [Projects](#projects)")
    st.markdown("🎓 [Education](#education)")
    st.markdown("📧 [Contact](#contact)")
    st.markdown("---")
    st.markdown("### Connect With Me")
    cols = st.columns(3)
    cols[0].markdown('<a href="https://www.linkedin.com/in/sivamahendranath-ragimanu-68a94823b/" target="_blank"><i class="fab fa-linkedin fa-2x" style="color:#667eea;"></i></a>', unsafe_allow_html=True)
    cols[1].markdown('<a href="https://github.com/Sivamahendranath" target="_blank"><i class="fab fa-github fa-2x" style="color:#667eea;"></i></a>', unsafe_allow_html=True)
    cols[2].markdown('<a href="mailto:mahendraragimanu2@gmail.com" target="_blank"><i class="fas fa-envelope fa-2x" style="color:#667eea;"></i></a>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📊 Profile Stats")
    st.metric("Projects Completed", "6+")
    st.metric("Years Experience", "1+")
    st.metric("Technologies", "15+")

st.markdown('<div class="section" id="home">', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""<div class="hero-section fade-in"><h1>Sivamahendranath <span style="color:#ffd700;">Ragimanu</span></h1><h3>🎓 AI Engineer | Data Analyst | Python Developer | Machine Learning Specialist</h3><p class="lead-text">Aspiring AI & Data Professional with hands-on experience in Python, Machine Learning, LLMs (GPT-4, Gemini), and RAG pipelines. Currently pursuing HPC-AI Certification at C-DAC Bangalore. Interned at C-DAC Hyderabad, where I built AI-powered knowledge graphs, semantic search tools, and document analysis applications using Streamlit, SQLite3, and NetworkX. Strong expertise in data visualization, NLP, and automated data processing with proven ability to improve data processing accuracy by 30% through innovative AI solutions. Passionate about building smart, scalable, and impactful AI solutions that transform raw data into actionable insights.</p></div>""", unsafe_allow_html=True)
with col2:
    profile_image_path = get_image_path("profile.jpeg")
    if os.path.exists(profile_image_path):
        profile_img = load_image(profile_image_path)
    else:
        profile_img = get_placeholder_image(300, 300, color="#5846f6")
    st.image(profile_img, use_container_width=True)

st.markdown("<div class='section-header'><h2>About Me</h2></div>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])
with col1:
    about_image_path = get_image_path("about_me.jpeg")
    if os.path.exists(about_image_path):
        about_img = load_image(about_image_path)
    else:
        about_img = get_placeholder_image(400, 400, color="#4a3bf5")
    st.image(about_img, caption="Sivamahendranath Ragimanu", use_container_width=True)
with col2:
    st.markdown("""<div class="about-text fade-in"><p>Currently pursuing HPC-AI Certification at C-DAC Bangalore, specializing in High-Performance Computing, Cloud Infrastructure, and AI-Driven System Automation. Experienced AI & Data Science professional skilled in Python, NLP, LLMs (GPT-4, Gemini), RAG pipelines, and Streamlit. Expert in building offline-first AI applications, including document chatbots, knowledge graph visualizers, and semantic search tools. Demonstrated success at C-DAC Hyderabad internship, developing AI-powered solutions that improved data processing accuracy by 30%. Proven track record in creating data pipelines, implementing automation tools, and leading AI projects with focus on data privacy and interactive insights. Core Competencies: Python | GPT-4 | Gemini API | LangChain | RAG | NLP | SQLite3 | NetworkX | Data Visualization | Machine Learning | Pandas | Matplotlib | OpenCV | Streamlit</p></div>""", unsafe_allow_html=True)
    st.markdown("""<div class="key-points"><div class="key-point"><i class="fas fa-map-marker-alt"></i> Anantapur, Andhra Pradesh, India</div><div class="key-point"><i class="fas fa-phone"></i> +91 8106442744</div><div class="key-point"><i class="fas fa-envelope"></i> mahendraragimanu2@gmail.com</div><div class="key-point"><i class="fas fa-graduation-cap"></i> Currently: HPC-AI Certification @ C-DAC Bangalore</div></div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section" id="skills">', unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Technical Skills</h2></div>", unsafe_allow_html=True)

skill_categories = {"Operating Systems": {"icon": "fas fa-desktop","skills": ["Windows","Linux (Ubuntu)","Virtualization (VirtualBox)"]},"Programming & Tools": {"icon": "fas fa-code","skills": ["Python","C","SQL"]},"AI & Data Science": {"icon": "fas fa-brain","skills": ["LLMs (GPT-4, Gemini)","RAG Pipelines","Machine Learning","Artificial Intelligence","NLP","Data Analysis","Data Visualization"]},"Web Development": {"icon": "fas fa-globe","skills": ["Streamlit","HTML/CSS","JavaScript"]},"Database & Tools": {"icon": "fas fa-database","skills": ["SQLite3","SQL (Oracle)","Pandas","NetworkX","Matplotlib","Seaborn","Plotly"]}}

for category, data in skill_categories.items():
    st.markdown(f"""<div class="skill-category"><h3><i class="{data['icon']} skill-category-icon"></i>{category}</h3></div>""", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    skills_list = data["skills"]
    half = len(skills_list) // 2 + len(skills_list) % 2
    with col1:
        for skill in skills_list[:half]:
            st.markdown(f"""<div class="skill-container fade-in"><div class="skill-name">{skill}</div></div>""", unsafe_allow_html=True)
    with col2:
        for skill in skills_list[half:]:
            st.markdown(f"""<div class="skill-container fade-in"><div class="skill-name">{skill}</div></div>""", unsafe_allow_html=True)

st.markdown("<div class='section-header'><h2>Soft Skills</h2></div>", unsafe_allow_html=True)
soft_skills = ["Communication", "Team Work", "Leadership", "Problem Solving", "Analytical Thinking"]
col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]
for i, skill in enumerate(soft_skills):
    with cols[i % 3]:
        st.markdown(f"""<div class="soft-skill-card fade-in"><i class="fas fa-check-circle"></i><h4>{skill}</h4></div>""", unsafe_allow_html=True)

st.markdown("<div class='section-header'><h2>Work Experience</h2></div>", unsafe_allow_html=True)
cdac_img_path = get_image_path("work_experience_cdac.png")
if os.path.exists(cdac_img_path):
    exp_img = load_image(cdac_img_path)
else:
    exp_img = get_placeholder_image(800, 300, color="#3b2ff5")
st.image(exp_img, caption="Work Experience at C-DAC Hyderabad", use_container_width=True)

st.markdown("""<div class="timeline fade-in"><div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-date">October 2024 - April 2025</div><div class="timeline-content custom-card"><h3>Data Analyst (Python), Intern</h3><h4>C-DAC, Hyderabad</h4></div></div></div>""", unsafe_allow_html=True)
st.markdown("""<ul style="margin-top:-20px;margin-left:40px;color:#fff;font-size:1.05rem;"><li>Created data pipelines and visualized datasets with Pandas, Matplotlib, and Streamlit in Python for quick insights on data.</li><li>Used GPT-4, Gemini APIs, and NLP to extract structured data from raw text improved data processing accuracy by 30%.</li><li>Designed and optimized SQLite databases for storage of knowledge graph data that are scalable and helped with quick querying.</li><li>Built dynamic and interactive graph visualizations using NetworkX and Pyvis to help stakeholders understand the graphs and make better-informed decisions.</li><li>Built automation tools for collecting data using BeautifulSoup and led AI-powered projects that demonstrated my expertise in LLM integration, backend design, and Python scripting.</li></ul>""", unsafe_allow_html=True)

st.markdown("<div class='section-header'><h2>Professional Accomplishments</h2></div>", unsafe_allow_html=True)
accomplishments = [{"title": "Event Organizer", "icon": "fas fa-calendar-check", "detail": "Leading as an Event Organizer (Coding, Workshops) at KSRM College of Engineering."},{"title": "Team Leader", "icon": "fas fa-users", "detail": "Serving as Team Leader for both minor and major projects at KSRM College of Engineering."},{"title": "AI Developer", "icon": "fas fa-robot", "detail": "Actively involved in developing AI-powered solutions and knowledge graph applications."}]
col1, col2 = st.columns(2)
for i, acc in enumerate(accomplishments):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"""<div class="accomplishment-card fade-in"><div class="accomplishment-icon"><i class="{acc['icon']}"></i></div><div class="accomplishment-content"><h4>{acc['title']}</h4><p>{acc['detail']}</p></div></div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section" id="projects">', unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Personal Projects</h2></div>", unsafe_allow_html=True)

project_images = {"AI-Powered Knowledge Graph Generator": "knowledge_graph.png","DocuGenius Pro": "docugenius.png","Exam Proctoring System": "exam_proctor.jpg"}

projects = [{"title": "AI-Powered Knowledge Graph Generator","date": "January 2025 - March 2025","org": "C-DAC, Hyderabad","type": "Main Project","description": "LLM-based pipeline using Google Gemini for entity extraction and graph visualization","features": ["Implemented an LLM-based pipeline using Google Gemini to extract entities & relationships from text sources.","Built dynamic, expandable knowledge graphs with NetworkX & Pyvis, enabling semantic exploration.","Stored extracted data in a structured SQLite3 schema to support complex querying.","Multi-format input handling supporting text files and web URLs for seamless data processing.","Interactive graph visualization with node-click expansion and continuous relationship exploration."],"tech_stack": ["Python", "Streamlit", "Google Gemini API", "SQLite3", "NetworkX", "Pyvis", "NLP", "BeautifulSoup"],"github": "https://github.com/Sivamahendranath/Gemini_Knowledge_Graph/blob/main/backup.py"},{"title": "DocuGenius Pro","date": "January 2025","org": "C-DAC, Hyderabad","type": "Personal Mini Project","description": "Streamlit-based AI-powered document processing application with chatbot capabilities","features": ["Built an end-to-end document processing application with Streamlit and Google Gemini API.","Added support for Text, PDFs, CSVs, and URLs with smart analysis, summaries, and AI-powered Q&A.","Implemented Plotly visualizations and NER-based entity extraction for advanced analytics.","Enabled custom themes and exportable reports (CSV/JSON/PDF) for enhanced user experience.","Multi-format document processing with AI-powered insights and interactive visualizations."],"tech_stack": ["Python", "Streamlit", "Google Gemini API", "Plotly", "NLP", "Pandas", "ReportLab"],"github": "https://github.com/Sivamahendranath/Gemini-Document-RAG/blob/main/code/main.py"},{"title": "Exam Proctoring System","date": "December 2023 - March 2024","org": "KSRM College Of Engineering, Kadapa","type": "Major Project","description": "Machine learning-based live exam proctoring system with automated monitoring","features": ["Led a 4-member team to build a live exam proctoring system using OpenCV, Dlib, and facial recognition.","Automated activity monitoring with warning triggers and report generation, improving exam integrity.","Delivered a fully functional monitoring platform with alerts and analytics dashboards.","Real-time face detection and tracking with suspicious activity flagging.","Comprehensive malpractice reports with activity graphs for authorities."],"tech_stack": ["Python", "OpenCV", "Dlib", "Face Recognition", "Machine Learning"],"github": "https://github.com/Sivamahendranath/Exam-Proctoring-System"}]
for i, project in enumerate(projects):
    if i % 2 == 0:
        col1, col2 = st.columns(2)
    with col1 if i % 2 == 0 else col2:
        img_path = get_image_path(project_images.get(project["title"], "placeholder.jpg"))
        if os.path.exists(img_path):
            project_img = load_image(img_path)
        else:
            project_img = get_placeholder_image(400, 300, color="#5846f6")
        st.image(project_img, caption=project["title"], use_container_width=True)
        st.markdown(f"""<div class="project-details fade-in"><h3>{project["title"]}</h3><div class="project-meta"><div><i class="far fa-calendar-alt"></i> {project["date"]}</div><div><i class="fas fa-building"></i> {project["org"]}</div><div><i class="fas fa-tag"></i> {project["type"]}</div></div><p class="project-description">{project["description"]}</p><h4>Key Features:</h4><ul class="feature-list">{"".join([f"<li>{feature}</li>" for feature in project["features"]])}</ul><div class="tech-stack"><h4>Tech Stack:</h4><div>{"".join([f'<span class="tech-badge">{tech}</span>' for tech in project["tech_stack"]])}</div></div><div style="margin-top:15px;"><a href="{project["github"]}" target="_blank" style="color:#ffd700;font-weight:600;"><i class="fab fa-github"></i> View on GitHub</a></div></div>""", unsafe_allow_html=True)
    if i % 2 == 1 or i == len(projects) - 1:
        st.markdown("<hr style='border:2px solid rgba(255,215,0,0.3);margin:30px 0;'>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section" id="education">', unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Education</h2></div>", unsafe_allow_html=True)
edu_img_path = get_image_path("education.jpg")
if os.path.exists(edu_img_path):
    edu_img = load_image(edu_img_path)
else:
    edu_img = get_placeholder_image(600, 400, color="#3527f5")
st.image(edu_img, caption="Education Journey", use_container_width=True)

education = [{"degree": "HPC-AI Certification Course","institution": "Centre for Development of Advanced Computing (C-DAC)","location": "Bangalore, Karnataka","duration": "August 2025 - Present","grade": "In Progress","courses": ["High-Performance Computing", "Cloud Infrastructure", "AI-Driven System Automation", "Distributed Computing", "Advanced Machine Learning"]},{"degree": "Bachelor of Technology (B.Tech) in Computer Science and Engineering","institution": "KSRM College of Engineering, JNTUA","location": "Kadapa, Andhra Pradesh","duration": "December 2020 - April 2024","grade": "8.3/10 CGPA","courses": ["Programming and Scripting", "Data Structures", "Algorithms", "Database Management", "Web Development", "Machine Learning", "Artificial Intelligence"]},{"degree": "Higher Secondary School (MPC)","institution": "JCDR Junior College","location": "Anantapur, Andhra Pradesh","duration": "June 2018 - March 2020","grade": "6.21/10 CGPA","courses": ["Mathematics", "Physics", "Chemistry"]},{"degree": "Secondary School Certificate (10th Grade)","institution": "ZP High School","location": "Anantapur, Andhra Pradesh","duration": "June 2017 - March 2018","grade": "9.0/10 GPA","courses": ["Mathematics", "Science", "Languages"]}]

for i, edu in enumerate(education):
    st.markdown(f"""<div class="timeline-item fade-in"><div class="timeline-dot"></div><div class="timeline-date">{edu["duration"]}</div><div class="timeline-content custom-card"><h3>{edu["degree"]}</h3><h4>{edu["institution"]}, {edu["location"]}</h4><div class="education-grade"><span><i class="fas fa-star"></i> {edu["grade"]}</span></div><div class="key-courses" style="margin-top:10px;"><h5>Key Courses:</h5><p>{", ".join(edu["courses"])}</p></div></div></div>""", unsafe_allow_html=True)

st.markdown("<div class='section-header'><h2>Certifications & Trainings</h2></div>", unsafe_allow_html=True)
certifications = [{"title": "Certification of Completion Of WBL Internship [Data Analyst with Python]","issuer": "C-DAC, Hyderabad","date": "April 28, 2025"},{"title": "Certification of Completion, Python 3.X-Programming Course (Hands-On)","issuer": "Skill Rack","date": "August 2, 2022"},{"title": "Certification of Completion Python-STARTER","issuer": "Skill Rack","date": "August 3, 2022"},{"title": "Certification of Completion PYTHON3.X - 50 VERY-EASY CHALLENGES","issuer": "Skill Rack","date": "August 3, 2022"}]
col1, col2 = st.columns(2)
for i, cert in enumerate(certifications):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"""<div class="custom-card fade-in"><h4>{cert["title"]}</h4><p><i class="fas fa-certificate" style="color:#ffd700;"></i> {cert["issuer"]} | {cert["date"]}</p></div>""", unsafe_allow_html=True)

st.markdown("<div class='section-header'><h2>Languages</h2></div>", unsafe_allow_html=True)
languages = [{"name": "English", "proficiency": "Professional", "icon": "fas fa-comment-dots"},{"name": "Telugu", "proficiency": "Native", "icon": "fas fa-comments"},{"name": "Hindi", "proficiency": "Intermediate", "icon": "fas fa-comment-alt"}]
cols = st.columns(3)
for i, lang in enumerate(languages):
    with cols[i]:
        st.markdown(f"""<div class="language-card fade-in"><div class="language-icon"><i class="{lang['icon']}"></i></div><h4>{lang["name"]}</h4><p>{lang["proficiency"]}</p></div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section" id="contact">', unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Contact Me</h2></div>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("<h3 style='color:#fff;'>Send me a message</h3>", unsafe_allow_html=True)
    if 'name_error' not in st.session_state:
        st.session_state.name_error = ""
    if 'email_error' not in st.session_state:
        st.session_state.email_error = ""
    if 'message_error' not in st.session_state:
        st.session_state.message_error = ""
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    if st.session_state.form_submitted:
        st.markdown('<div class="form-success">✅ Thank you for your message! I will get back to you soon.</div>', unsafe_allow_html=True)
        st.session_state.form_submitted = False
    with st.form("contact_form", clear_on_submit=True):
        st.markdown('<label style="color:#fff;font-weight:600;">Name <span style="color:#ff4444;">*</span></label>', unsafe_allow_html=True)
        name = st.text_input("", placeholder="Your name", key="name")
        if st.session_state.name_error:
            st.markdown(f'<div class="form-error">{st.session_state.name_error}</div>', unsafe_allow_html=True)
        st.markdown('<label style="color:#fff;font-weight:600;">Email <span style="color:#ff4444;">*</span></label>', unsafe_allow_html=True)
        email = st.text_input("", placeholder="Your email", key="email")
        if st.session_state.email_error:
            st.markdown(f'<div class="form-error">{st.session_state.email_error}</div>', unsafe_allow_html=True)
        st.markdown('<label style="color:#fff;font-weight:600;">Message <span style="color:#ff4444;">*</span></label>', unsafe_allow_html=True)
        message = st.text_area("", placeholder="Your message", height=150, key="message")
        if st.session_state.message_error:
            st.markdown(f'<div class="form-error">{st.session_state.message_error}</div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("Send Message")
        if submitted:
            st.session_state.name_error = ""
            st.session_state.email_error = ""
            st.session_state.message_error = ""
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
            if valid_form:
                save_message_to_db(name, email, message)
                try:
                    send_email_notification(name, email, message)
                except Exception as e:
                    st.warning(f"Email notification could not be sent: {e}")
                st.session_state.form_submitted = True
                st.rerun()
with col2:
    st.markdown("### 📱 Contact Information", unsafe_allow_html=True)
    st.markdown("#### 📍 Location")
    st.write("Anantapur, Andhra Pradesh, India")
    st.markdown("#### ✉️ Email")
    st.write("mahendraragimanu2@gmail.com")
    st.markdown("#### ☎️ Phone")
    st.write("+91 8106442744")
    st.markdown("#### 🔗 Connect With Me")
    social_cols = st.columns(3)
    with social_cols[0]:
        st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sivamahendranath-ragimanu-68a94823b/)")
    with social_cols[1]:
        st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Sivamahendranath)")
    with social_cols[2]:
        st.markdown("[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:mahendraragimanu2@gmail.com)")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown("""<div class="footer"><p>&copy; 2025 Sivamahendranath Ragimanu | All Rights Reserved</p><p>Built with ❤️ using Streamlit & Python</p></div>""", unsafe_allow_html=True)
