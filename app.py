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

# Page configuration
st.set_page_config(
    page_title="Sivamahendranath Ragimanu | Portfolio",
    page_icon="👨‍💻",
    layout="wide",
)

# Function to get image path
def get_image_path(relative_path):
    """Get absolute path for an image based on relative path"""
    # Define the base path for your images
    # When deployed, this should be relative to your app's main script
    base_path = Path(__file__).parent / "images"
    return str(base_path / relative_path)

# Function to load an image safely
def load_image(image_path):
    """Load an image from path, with error handling"""
    try:
        return Image.open(image_path)
    except FileNotFoundError:
        st.warning(f"Image not found: {image_path}")
        # Return a placeholder image instead
        return get_placeholder_image(400, 300, color="#5846f6")
    except Exception as e:
        st.warning(f"Error loading image {image_path}: {str(e)}")
        return get_placeholder_image(400, 300, color="#5846f6")

# Function to verify image paths exist
def verify_image_paths():
    """Verify all image paths exist and are accessible"""
    image_paths = [
        "profile.jpeg",
        "background.jpg",
        "about_me.jpeg",
        "work_experience_cdac.png",
        "work_experience/oppo.jpg",
        "knowledge_graph.png",
        "docugenius.png",
        "student_dashboard.jpg",
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

# Include Font Awesome for icons
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)

# Improved CSS styling
st.markdown("""
<style>
    /* Basic styling */
    .hero-section h1 {
        font-size: 3rem;
        font-weight: 700;
    }
    .highlight {
        color: #5846f6;
    }
    .section-header h2 {
        border-bottom: 2px solid #5846f6;
        padding-bottom: 10px;
        margin-top: 30px;
    }
    .custom-card {
        border-left: 4px solid #5846f6;
        padding: 15px;
        margin: 15px 0;
        background-color: rgba(88, 70, 246, 0.05);
    }
    .fade-in {
        animation: fadeIn 1s ease-in;
    }
    .skill-container {
        margin: 15px 0;
    }
    .skill-bar-container {
        background-color: #e0e0e0;
        border-radius: 10px;
        height: 10px;
        width: 100%;
    }
    .skill-bar {
        background-color: #5846f6;
        border-radius: 10px;
        height: 10px;
    }
    .timeline-item {
        position: relative;
        padding-left: 30px;
        margin-bottom: 30px;
    }
    .timeline-dot {
        position: absolute;
        left: 0;
        top: 5px;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        background-color: #5846f6;
    }
    .timeline-date {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .timeline-content {
        margin-left: 10px;
    }
    .footer {
        margin-top: 50px;
        padding: 20px 0;
        text-align: center;
        border-top: 1px solid #e0e0e0;
    }
    .key-points {
        margin-top: 15px;
    }
    .key-point {
        margin-bottom: 8px;
    }
    .key-point i {
        margin-right: 10px;
        color: #5846f6;
    }
    .project-meta {
        margin: 20px 0;
    }
    .project-meta div {
        margin-bottom: 10px;
    }
    .project-meta i {
        margin-right: 10px;
        color: #5846f6;
    }
    .tech-stack {
        margin-top: 20px;
    }
    .tech-badge {
        display: inline-block;
        background-color: rgba(88, 70, 246, 0.1);
        color: #5846f6;
        padding: 5px 10px;
        margin: 5px;
        border-radius: 15px;
    }
    .project-icon {
        text-align: center;
        color: #5846f6;
        margin: 20px 0;
    }
    .project-details h3 {
        margin-bottom: 15px;
    }
    .project-description {
        font-style: italic;
        margin-bottom: 20px;
    }
    .feature-list li {
        margin-bottom: 10px;
    }
    .education-grade {
        margin-top: 10px;
    }
    .education-grade i {
        color: gold;
    }
    .language-card {
        text-align: center;
        padding: 15px;
        background-color: rgba(88, 70, 246, 0.05);
        border-radius: 10px;
        margin: 10px;
    }
    .language-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    .contact-info {
        margin: 20px 0;
    }
    .contact-item {
        display: flex;
        align-items: flex-start;
        margin-bottom: 20px;
    }
    .contact-item i {
        font-size: 1.5rem;
        color: #5846f6;
        margin-right: 15px;
        margin-top: 5px;
    }
    .social-links {
        margin-top: 15px;
    }
    .social-links a {
        margin: 0 10px;
        color: #5846f6;
        text-decoration: none;
    }
    .accomplishment-card {
        display: flex;
        align-items: flex-start;
        background-color: rgba(88, 70, 246, 0.05);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .accomplishment-icon {
        font-size: 1.5rem;
        color: #5846f6;
        margin-right: 15px;
    }
    .soft-skill-card {
        text-align: center;
        padding: 15px;
        background-color: rgba(88, 70, 246, 0.05);
        border-radius: 10px;
        margin: 10px;
    }
    .soft-skill-card i {
        font-size: 1.5rem;
        color: #5846f6;
        margin-bottom: 10px;
    }
    .profile-img {
        border-radius: 50%;
        max-width: 100%;
        border: 3px solid #5846f6;
    }
    .contact-button {
        background-color: #5846f6;
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
    }
    .contact-button:hover {
        background-color: #4835d4;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .section-divider {
        height: 50px;
    }
    .section {
        padding: 30px 0;
        border-bottom: 1px solid #e0e0e0;
    }
    .section:last-child {
        border-bottom: none;
    }
    .image-debug {
        padding: 10px;
        background-color: #f0f0f0;
        border-radius: 5px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Create a simple sidebar for theme selection
with st.sidebar:
    st.title("Theme Settings")
    theme = st.selectbox("Choose Theme", ["Blue", "Green"])
    
    # Apply theme via session state
    if 'theme' not in st.session_state:
        st.session_state.theme = theme
    
    if st.session_state.theme != theme:
        st.session_state.theme = theme
        st.rerun()
    # Add social links in sidebar
    st.markdown("---")
    cols = st.columns(3)
    cols[0].markdown(f'<a href="https://www.linkedin.com/in/sivamahendranath-ragimanu-68a94823b/" target="_blank"><i class="fab fa-linkedin fa-2x" style="color: #5846f6;"></i></a>', unsafe_allow_html=True)
    cols[1].markdown(f'<a href="https://github.com/Sivamahendranath" target="_blank"><i class="fab fa-github fa-2x" style="color: #5846f6;"></i></a>', unsafe_allow_html=True)
    cols[2].markdown(f'<a href="mailto:mahendraragimanu2@gmail.com" target="_blank"><i class="fas fa-envelope fa-2x" style="color: #5846f6;"></i></a>', unsafe_allow_html=True)

# Apply the selected theme
theme_colors = {
    "Blue": {"bg": "#0a192f", "text": "#e6f1ff", "accent": "#64ffda"},
    "Green": {"bg": "#0f1a0f", "text": "#e6ffe6", "accent": "#4dff4d"}
}

# Apply theme colors via CSS
selected_theme = theme_colors[st.session_state.theme]
st.markdown(f"""
<style>
    .stApp {{
        background-color: {selected_theme["bg"]};
        color: {selected_theme["text"]};
    }}
    .highlight, .section-header h2 {{
        color: {selected_theme["accent"]} !important;
    }}
    .custom-card {{
        border-left: 4px solid {selected_theme["accent"]};
    }}
    .skill-bar {{
        background-color: {selected_theme["accent"]};
    }}
    .timeline-dot {{
        background-color: {selected_theme["accent"]};
    }}
    .tech-badge {{
        color: {selected_theme["accent"]};
    }}
    .project-icon {{
        color: {selected_theme["accent"]};
    }}
    .contact-item i {{
        color: {selected_theme["accent"]};
    }}
    .social-links a {{
        color: {selected_theme["accent"]};
    }}
    .contact-button {{
        background-color: {selected_theme["accent"]};
    }}
    .contact-button:hover {{
        background-color: {selected_theme["accent"]};
        opacity: 0.9;
    }}
</style>
""", unsafe_allow_html=True)

# Main content - Now in scrolling format
# SECTION 1: Home
st.markdown('<div class="section" id="home">', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="hero-section fade-in">
        <h1>Sivamahendranath <span class="highlight">Ragimanu</span></h1>
        <h3>Data Analyst | Python Developer | Machine Learning Enthusiast</h3>
        <p class="lead-text">Fresher Engineer with a solid foundation in Python, web development, data analysis, and machine learning. 
        Adept at leading projects, collaborating with cross-functional teams, and delivering impactful solutions.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Load profile image
    profile_image_path = get_image_path("profile.jpeg")
    if os.path.exists(profile_image_path):
        profile_img = load_image(profile_image_path)
    else:
        profile_img = get_placeholder_image(300, 300, color="#5846f6")
    st.image(profile_img, use_container_width=True)

# About Section
st.markdown("<div class='section-header'><h2>About Me</h2></div>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    # Load about image
    about_image_path = get_image_path("about_me.jpeg")
    if os.path.exists(about_image_path):
        about_img = load_image(about_image_path)
    else:
        about_img = get_placeholder_image(400, 400, color="#4a3bf5")
    st.image(about_img, caption="Sivamahendranath Ragimanu", use_container_width=True)

with col2:
    st.markdown("""
    <div class="about-text fade-in">
        <p>Fresher Engineer with strong skills in Python, web development, data analysis, and machine learning. 
        Experienced in working with LLMs and RAG pipelines for intelligent data solutions. Proven ability to lead 
        projects, collaborate across teams, and build impactful tools. Quick learner with strong problem-solving and communication skills,
        eager to grow in a fast-paced, innovative environment. </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add key points separately
    st.markdown("""
    <div class="key-points">
        <div class="key-point"><i class="fas fa-map-marker-alt"></i> Anantapur,  Andhra Pradesh</div>
        <div class="key-point"><i class="fas fa-phone"></i> 8106442744</div>
        <div class="key-point"><i class="fas fa-envelope"></i> mahendraragimanu2@gmail.com</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# SECTION 2: Skills & Experience
st.markdown('<div class="section" id="skills">', unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Technical Skills</h2></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Load skills image
    skills_image_path = get_image_path("skills.jpg")
    if os.path.exists(skills_image_path):
        skills_img = load_image(skills_image_path)
    else:
        skills_img = get_placeholder_image(400, 300, color="#7265f2")
    st.image(skills_img, caption="Technical Skills", use_container_width=True)

with col2:
    # Technical Skills
    skills = {
        "Python": 85,
        "HTML/CSS": 75,
        "Java": 65,
        "SQL (Oracle)": 70,
        "Machine Learning": 75,
        "Data Analysis": 80,
        "LLMs & RAG": 65
    }
    
    for skill, proficiency in skills.items():
        st.markdown(f"""
        <div class="skill-container fade-in">
            <div class="skill-name">{skill}</div>
            <div class="skill-bar-container">
                <div class="skill-bar" style="width: {proficiency}%"></div>
            </div>
            <div class="skill-percentage">{proficiency}%</div>
        </div>
        """, unsafe_allow_html=True)

# Soft Skills
st.markdown("<div class='section-header'><h2>Soft Skills</h2></div>", unsafe_allow_html=True)

soft_skills = ["Communication", "Team Work", "Leadership", "Problem Solving", "Analytical Thinking"]

col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

for i, skill in enumerate(soft_skills):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="soft-skill-card fade-in">
            <i class="fas fa-check-circle"></i>
            <h4>{skill}</h4>
        </div>
        """, unsafe_allow_html=True)

# Work Experience
st.markdown("<div class='section-header'><h2>Work Experience</h2></div>", unsafe_allow_html=True)

# Load work experience image for CDAC
cdac_img_path = get_image_path("work_experience_cdac.png")
if os.path.exists(cdac_img_path):
    exp_img = load_image(cdac_img_path)
else:
    exp_img = get_placeholder_image(800, 300, color="#3b2ff5")
st.image(exp_img, caption="Work Experience at CDAC", use_container_width=True)

# Experience 1
st.markdown("""
<div class="timeline fade-in">
    <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-date">October 2024 - Present</div>
        <div class="timeline-content custom-card">
            <h3>Data Analyst (Python), Intern</h3>
            <h4>C-DAC, Hyderabad</h4>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# List items for Experience 1
st.markdown("""
<ul style="margin-top: -20px; margin-left: 40px;">
    <li>Analyzed and visualized complex datasets using Python, Pandas, and Matplotlib to uncover actionable business insights.</li>
    <li>Extracted structured information from unstructured text using LLMs (GPT-4) and applied NLP techniques for deeper analysis.</li>
    <li>Designed and managed SQLite3 databases to efficiently store, query, and retrieve knowledge graph data.</li>
    <li>Built interactive data visualizations and semantic graphs using NetworkX and Pyvis for intuitive insight communication.</li>
    <li>Automated data collection and enrichment using web scraping (BeautifulSoup), enhancing analysis depth 
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

# List items for Experience 2
st.markdown("""
<ul style="margin-top: -20px; margin-left: 40px;">
    <li>Worked as a device testing engineer role in intern position.</li>
    <li>Testing and checking the mobile device performance.</li>
    <li>Finding the bugs in the device and reporting them to the team leader.</li>
    <li>Communicating with team members and Developers, Giving and sharing the ideas for solving the bug issues and improving the device performance.</li>
</ul>
""", unsafe_allow_html=True)

# Professional Accomplishments
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
        <div class="accomplishment-card fade-in">
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
    # Project image placeholder
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

# Individual Projects with GitHub links
projects = [
    {
        "title": "AI-Powered Knowledge Graph Explorer",
        "date": "January 2025, March 2025",
        "org": "C-DAC, Hyderabad",
        "type": "Main Project",
        "description": "AI-Powered Knowledge Graph Generator using LLMs and Graph Visualization Application using Streamlit",
        "details": [
            "Multi-Format Input Handling: Ingested and parsed raw input from Text files and Web URLs for seamless data processing",
            "LLM-Based Entity Extraction: Leveraged Google Gemini API to extract entities, attributes, relationships, and contextual links.",
            "Structured Data Storage: Stored parsed information in SQLite3 using a scalable, query-ready schema.",
            "Interactive Graph Visualization: Built dynamic knowledge graphs with NetworkX and Pyvis,supporting node-click expansion.",
            "Semantic Relationship Exploration: Enabled deep relationship analysis with continuous graph expansion and case study generation."
        ],
        "tech": ["Python", "Streamlit", "Google Gemini API", "Sqlite3","Plotly", "NLP", "NetworkX", "BeautifulSoup"],
        "github": "https://github.com/Sivamahendranath/AI-Knowledge-Graph-Explorer"
    },
    {
        "title": "DocuGenius Pro",
        "date": "January 2025",
        "org": "C-DAC, Hyderabad",
        "type": "Personal Mini Project",
        "description": "AI-powered document processing application using Streamlit",
        "details": [
            "Multi-Format Document Processing: Extracts and processes Text, PDFs, CSVs, and Web URLs",
            "AI-Powered Analysis: Leverages Google Gemini API for insights, summaries, and answers",
            "Data Visualization: Creates interactive graphs and statistics for CSV data with Plotly",
            "Named Entity Recognition (NER): Identifies key entities from processed documents",
            "Query-Based Analysis: Allows users to ask questions based on document content",
            "Customizable Themes & Export Analysis History"
        ],
        "tech": ["Python", "Streamlit", "Google Gemini API", "Plotly", "NLP"],
        "github": "https://github.com/Sivamahendranath/Gemini-Document-RAG/tree/main/code"
    },
    {
        "title": "Student Performance Dashboards for Exams",
        "date": "October 2024 - November 2024",
        "org": "C-DAC, Hyderabad",
        "type": "Mini Project",
        "description": "Data visualization dashboards for analyzing student performance",
        "details": [
            "Cleaned and processed datasets, converting columns to numeric and handling missing data",
            "Designed thresholds to classify performance into categories (Fail to Excellent)",
            "Aggregated and summarized student performance metrics across lab and theory scores",
            "Created diverse visualizations including pie charts, bar charts, stacked bars, heatmaps",
            "Implemented advanced visualization techniques for trend analysis and insights",
            "Optimized data workflows for decision-making"
        ],
        "tech": ["Python", "Pandas", "Matplotlib", "Seaborn", "Data Visualization"],
        "github": "https://github.com/Sivamahendranath/Student-Performance-Dashboard"
    },
    {
        "title": "Andhra Pradesh Southern Power Distribution Company Limited",
        "date": "April 2024 - May 2024",
        "org": "KSRM College Of Engineering, Kadapa",
        "type": "Personal Mini Project",
        "description": "Electricity Bill Calculator – Streamlit Web Application",
        "details": [
            "Multi-Tariff Bill Calculation: Calculates electricity bills for domestic, commercial, and industrial users with tiered and time-of-use tariff logic.",
            "Interactive Visualizations: Uses Plotly to display consumption patterns and billing breakdown through dynamic charts and graphs.",
            "PDF Bill Generation: Generates downloadable and printable bills in PDF format using ReportLab for professional documentation.",
            "Usage History & Trends: Tracks historical electricity usage and visualizes spending trends to help users monitor and manage consumption.",
            "Responsive UI Design: Built with Streamlit for a mobile-friendly, intuitive interface that works seamlessly across all devices.",
            "Real-World Utility Integration: Tailored for APSPDCL with accurate tariff modeling, due date logic, and late fee calculations.",
            "Modular Architecture: Structured with scalable components and future-ready plans including authentication, payments, and multi-language support."
        ],
        "tech": ["Python", "Streamlit", "Plotly", "Pandas", "ReportLab", "HTML/CSS"],
        "github": "https://github.com/Sivamahendranath/Electricity_Bill_App/blob/main/readme.md",
    },
    {
        "title": "Exam Proctoring System",
        "date": "December 2023 - March 2024",
        "org": "KSRM College Of Engineering, Kadapa",
        "type": "Major Project",
        "description": "Machine learning application for online exam proctoring",
        "details": [
            "Led a team and developed a machine learning application for online exam proctoring",
            "Used OpenCV, Dlib, and Face Recognition Library for monitoring candidates",
            "Monitored candidates' movements and flagged suspicious activities during exams",
            "Implemented warning mechanisms and automatic termination for suspicious activities",
            "Generated detailed malpractice reports, including activity graphs, for authorities"
        ],
        "tech": ["Python", "OpenCV", "Dlib", "Face Recognition", "Machine Learning"],
        "github": "https://github.com/Sivamahendranath/Exam-Proctoring-System",
    },
    {
        "title": "Smart Fan Energy System",
        "date": "July 2023 - September 2023",
        "org": "KSRM College Of Engineering, Kadapa",
        "type": "Minor Project",
        "description": "IoT-based solution for optimizing energy usage in fan systems",
        "details": [
            "Led as Team Leader, Circuit Designer, and Arduino Coder",
            "Combined hardware and software expertise using Arduino and sensors",
            "Designed a cost-effective, customizable system for automating fan speed and power control",
            "Created a system that increased energy efficiency by 25% compared to manual fan control",
            "Implemented automatic temperature-based fan speed adjustment for optimal comfort"
        ],
        "tech": ["Arduino", "IoT", "Sensors"],
        "github": "https://github.com/Sivamahendranath/Smart-Fan-Energy-System",
    }
]

# Display projects in tabs with images
tab_titles = [project["title"] for project in projects]
tabs = st.tabs(tab_titles)

for i, tab in enumerate(tabs):
    with tab:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Load project image
            img_path = get_image_path(project_images.get(projects[i]["title"], "projects/default.jpg"))
            if os.path.exists(img_path):
                proj_img = load_image(img_path)
            else:
                proj_img = get_placeholder_image(400, 300, color="#544bf2")
            st.image(proj_img, use_container_width=True)
            
            # Project metadata - Fixed with st.markdown and unsafe_allow_html=True
            st.markdown(f"""
            <div class="project-meta">
                <div><i class="fas fa-calendar"></i> <strong>Date:</strong> {projects[i]["date"]}</div>
                <div><i class="fas fa-building"></i> <strong>Organization:</strong> {projects[i]["org"]}</div>
                <div><i class="fas fa-tag"></i> <strong>Type:</strong> {projects[i]["type"]}</div>
                <div><i class="fas fa-link"></i> <strong>GitHub:</strong> <a href="{projects[i]["github"]}" target="_blank">View Project</a></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Project details - Fixed implementation to avoid HTML showing in UI
            st.markdown(f"<div class='project-description'>{projects[i]['description']}</div>", unsafe_allow_html=True)
            st.markdown("<h4>Features & Achievements:</h4>", unsafe_allow_html=True)
            
            # Using Streamlit's native list component instead of HTML
            for item in projects[i]["details"]:
                st.markdown(f"- {item}")
            
            # Technologies section - Fixed implementation
            st.markdown("<h4>Technologies Used:</h4>", unsafe_allow_html=True)
            
            # Create tech badges using columns for better layout
            tech_cols = st.columns(len(projects[i]["tech"]))
            for idx, tech in enumerate(projects[i]["tech"]):
                tech_cols[idx].markdown(f"<div class='tech-badge'>{tech}</div>", unsafe_allow_html=True)
# SECTION 4: Education
st.markdown('<div class="section" id="education">', unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Education</h2></div>", unsafe_allow_html=True)

# Load education image
education_img_path = get_image_path("education.jpg")
if os.path.exists(education_img_path):
    edu_img = load_image(education_img_path)
else:
    edu_img = get_placeholder_image(800, 300, color="#4d3ef3")
st.image(edu_img, caption="Educational Background", use_container_width=True)

# Education Timeline
st.markdown(f"""
<div class="timeline fade-in">
    <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-date">2020 - 2024</div>
        <div class="timeline-content custom-card">
            <h3>B.Tech in Computer Science and Engineering</h3>
            <h4>KSRM College of Engineering, Kadapa, Andhra Pradesh</h4>
            <div class="education-grade">
                <i class="fas fa-star"></i> CGPA: 8.3/10
            </div>
        </div>
    </div>
    <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-date">2018 - 2020</div>
        <div class="timeline-content custom-card">
            <h3>Intermediate Education</h3>
            <h4>JCDR Junior College, Anantapur, Andhra Pradesh</h4>
            <div class="education-grade">
                <i class="fas fa-star"></i> CGPA: 6.21/10
            </div>
        </div>
    </div>
    <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-date">2017 - 2018</div>
        <div class="timeline-content custom-card">
            <h3>Board of Secondary Education</h3>
            <h4>ZP High School, Anantapur, Andhra Pradesh</h4>
            <div class="education-grade">
                <i class="fas fa-star"></i> GPA: 9.0/10
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Certifications
st.markdown("<div class='section-header'><h2>Certifications</h2></div>", unsafe_allow_html=True)
certifications = [
    {"title":"Certification of Completion Of WBL Internship [Data Analyst with Python]","issuer": "C-DAC, Hyderabad", "date": "28-April-2025"},
    {"title": "Certification of Completion, Python 3.X-Programming Course (Hands-On)", "issuer": "Skill Rack", "date": "02-August-2022"},
    {"title": "Certification of Completion Python-STARTER", "issuer": "SKill Rack", "date": "03-August-2022"},
    {"title": "Certfifcation of Completion PYTHON3.X - 50 VERY-EASY CHALLENGES", "issuer": "Skill Rack", "date": "03-August-2022"},
]

col1, col2 = st.columns(2)

for i, cert in enumerate(certifications):
    with col1 if i % 2 == 0 else col2:
        st.markdown(f"""
        <div class="custom-card fade-in">
            <h4>{cert["title"]}</h4>
            <p><strong>Issuer:</strong> {cert["issuer"]}</p>
            <p><strong>Date:</strong> {cert["date"]}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# SECTION 5: Languages
st.markdown('<div class="section" id="languages">', unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Languages</h2></div>", unsafe_allow_html=True)

languages = [
    {"name": "English", "proficiency": "Fluent", "icon": "fas fa-globe-americas"},
    {"name": "Telugu", "proficiency": "Native", "icon": "fas fa-globe-asia"},
    {"name": "Hindi", "proficiency": "Intermediate", "icon": "fas fa-globe-asia"},
]

col1, col2, col3, col4 = st.columns(4)
cols = [col1, col2, col3, col4]

for i, lang in enumerate(languages):
    with cols[i]:
        st.markdown(f"""
        <div class="language-card fade-in">
            <div class="language-icon"><i class="{lang['icon']}"></i></div>
            <h4>{lang['name']}</h4>
            <p>{lang['proficiency']}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# SECTION 6: Contact
st.markdown('<div class="section" id="contact">', unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Contact Me</h2></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    # Contact form
    st.markdown("<h3>Send me a message</h3>", unsafe_allow_html=True)
    
    with st.form("contact_form"):
        st.text_input("Name")
        st.text_input("Email")
        st.text_area("Message")
        submit_button = st.form_submit_button("Send Message")
        
        if submit_button:
            st.success("Thanks for your message! I'll get back to you soon.")

with col2:
    # Contact info
    st.markdown("<h3>Contact Information</h3>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="contact-info fade-in">
        <div class="contact-item">
            <i class="fas fa-envelope"></i>
            <div>
                <h4>Email</h4>
                <p>mahendraragimanu2@gmail.com</p>
            </div>
        </div>
        <div class="contact-item">
            <i class="fas fa-phone"></i>
            <div>
                <h4>Phone</h4>
                <p>+91 8106442744</p>
            </div>
        </div>
        <div class="contact-item">
            <i class="fas fa-map-marker-alt"></i>
            <div>
                <h4>Location</h4>
                <p>Anantapur, Andhra Pradesh, India</p>
            </div>
        </div>
    </div>
    
    <div class="social-links">
        <h4>Social Media</h4>
        <a href="https://www.linkedin.com/in/sivamahendranath-ragimanu-68a94823b/" target="_blank"><i class="fab fa-linkedin fa-2x"></i></a>
        <a href="https://github.com/Sivamahendranath" target="_blank"><i class="fab fa-github fa-2x"></i></a>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer section
st.markdown("""
<div class="footer">
    <p>© 2025 Sivamahendranath Ragimanu. All rights reserved.<br>@2025 Copy Right</p>
    <div>
        <a href="#home">Home</a> | 
        <a href="#skills">Skills</a> | 
        <a href="#projects">Projects</a> | 
        <a href="#education">Education</a> | 
        <a href="#contact">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Add smooth scrolling JS
st.markdown("""
<script>
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
</script>
""", unsafe_allow_html=True)
