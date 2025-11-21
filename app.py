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
st.set_page_config(
page_title="Sivamahendranath Ragimanu | AI & Data Professional",
page_icon="👨‍💻",
layout="wide",
initial_sidebar_state="collapsed"
)
def get_image_path(relative_path):
base_path=Path(__file__).parent/"images"
return str(base_path/relative_path)
def load_image(image_path):
try:
return Image.open(image_path)
except FileNotFoundError:
return get_placeholder_image(400,300,color="#5846f6")
except Exception as e:
return get_placeholder_image(400,300,color="#5846f6")
def get_placeholder_image(width,height,color="#5846f6"):
img=Image.new('RGB',(width,height),color=color)
return img
def save_message_to_db(name,email,message):
timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
message_data={"name":name,"email":email,"message":message,"timestamp":timestamp,"read":False}
db_path=Path(__file__).parent/"data"
db_path.mkdir(exist_ok=True)
messages_file=db_path/"contact_messages.json"
if messages_file.exists():
with open(messages_file,"r") as f:
try:
messages=json.load(f)
except json.JSONDecodeError:
messages=[]
else:
messages=[]
messages.append(message_data)
with open(messages_file,"w") as f:
json.dump(messages,f,indent=4)
return True
def send_email_notification(name,email,message):
try:
smtp_server=os.getenv("SMTP_SERVER","smtp.gmail.com")
smtp_port=int(os.getenv("SMTP_PORT","587"))
sender_email=os.getenv("SENDER_EMAIL")
sender_password=os.getenv("SENDER_PASSWORD")
recipient_email=os.getenv("RECIPIENT_EMAIL","mahendraragimanu2@gmail.com")
if not all([sender_email,sender_password,recipient_email]):
return False
subject=f"New Portfolio Contact from {name}"
email_message=MIMEMultipart()
email_message["From"]=sender_email
email_message["To"]=recipient_email
email_message["Subject"]=subject
html_content=f"""
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
email_message.attach(MIMEText(html_content,"html"))
with smtplib.SMTP(smtp_server,smtp_port) as server:
server.starttls()
server.login(sender_email,sender_password)
server.send_message(email_message)
return True
except Exception as e:
return False
def is_valid_email(email):
email_pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$'
return bool(re.match(email_pattern,email))
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
""",unsafe_allow_html=True)
st.markdown("""
<style>
:root{--primary-color:#5846f6;--secondary-color:#4a34ff;--text-color:#e6f1ff;--dark-bg:#0a192f;--card-bg:rgba(88,70,246,0.08);--transition:all 0.3s ease;--shadow:0 5px 15px rgba(0,0,0,0.1);--border-radius:10px;}
::-webkit-scrollbar{width:10px;height:10px;}
::-webkit-scrollbar-track{background:rgba(255,255,255,0.1);border-radius:10px;}
::-webkit-scrollbar-thumb{background:var(--primary-color);border-radius:10px;transition:var(--transition);}
::-webkit-scrollbar-thumb:hover{background:var(--secondary-color);}
body{font-family:'Poppins',sans-serif;color:var(--text-color);line-height:1.6;letter-spacing:0.5px;}
h1,h2,h3,h4,h5,h6{font-weight:700;letter-spacing:1px;margin-bottom:1rem;}
.stApp{background:var(--dark-bg);background-image:linear-gradient(to bottom right,rgba(88,70,246,0.05),transparent),url('https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80');background-position:center;background-size:cover;background-attachment:fixed;background-blend-mode:overlay;}
.hero-section{position:relative;padding:3rem 2rem;border-radius:var(--border-radius);background:linear-gradient(145deg,rgba(88,70,246,0.15),rgba(10,25,47,0.95));box-shadow:var(--shadow);overflow:hidden;z-index:1;margin-bottom:2rem;}
.hero-section::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:conic-gradient(from 0deg at 50% 50%,transparent 0deg,var(--primary-color) 60deg,transparent 120deg);animation:rotate 10s linear infinite;z-index:-1;opacity:0.1;}
@keyframes rotate{from{transform:rotate(0deg);}to{transform:rotate(360deg);}}
.hero-section h1{font-size:3.5rem;margin-bottom:1rem;background:linear-gradient(90deg,var(--text-color),var(--primary-color));-webkit-background-clip:text;background-clip:text;color:transparent;display:inline-block;animation:fadeInUp 1s ease forwards;}
.hero-section h3{font-size:1.5rem;margin-bottom:1.5rem;opacity:0;animation:fadeInUp 1s ease forwards 0.3s;}
.hero-section .lead-text{font-size:1.1rem;line-height:1.8;opacity:0;animation:fadeInUp 1s ease forwards 0.6s;}
@keyframes fadeInUp{from{opacity:0;transform:translateY(30px);}to{opacity:1;transform:translateY(0);}}
.section-header{position:relative;margin-bottom:2rem;padding-bottom:0.5rem;}
.section-header h2{display:inline-block;font-size:2.2rem;margin-bottom:1rem;position:relative;padding-left:1rem;opacity:0;animation:slideInLeft 1s ease forwards;}
@keyframes slideInLeft{from{opacity:0;transform:translateX(-50px);}to{opacity:1;transform:translateX(0);}}
.section-header h2::before{content:'';position:absolute;left:0;height:100%;width:4px;background:var(--primary-color);border-radius:4px;}
.section-header::after{content:'';position:absolute;left:0;bottom:0;height:2px;width:100%;background:linear-gradient(90deg,var(--primary-color),transparent);animation:expandWidth 2s ease forwards;}
@keyframes expandWidth{from{width:0;}to{width:100%;}}
.custom-card{position:relative;background:var(--card-bg);padding:1.5rem;margin-bottom:1.5rem;border-radius:var(--border-radius);border-left:4px solid var(--primary-color);box-shadow:var(--shadow);overflow:hidden;transition:var(--transition);}
.custom-card:hover{transform:translateY(-5px);box-shadow:0 8px 20px rgba(0,0,0,0.2);border-left-width:8px;}
.profile-img{position:relative;border-radius:50%;border:4px solid var(--primary-color);padding:5px;background:rgba(10,25,47,0.7);box-shadow:0 0 20px rgba(88,70,246,0.5);transition:var(--transition);animation:pulseGlow 3s infinite alternate;max-width:90%;margin:0 auto;display:block;}
@keyframes pulseGlow{0%{box-shadow:0 0 5px rgba(88,70,246,0.5);}100%{box-shadow:0 0 20px rgba(88,70,246,0.8);}}
.profile-img::before{content:'';position:absolute;top:-10px;left:-10px;right:-10px;bottom:-10px;border-radius:50%;border:2px solid var(--primary-color);animation:pulseOutline 3s infinite;opacity:0.7;}
@keyframes pulseOutline{0%{transform:scale(1);opacity:0.7;}50%{transform:scale(1.05);opacity:0.3;}100%{transform:scale(1);opacity:0.7;}}
.skill-category{margin-bottom:30px;}
.skill-category h3{color:#5846f6;border-bottom:1px solid rgba(88,70,246,0.3);padding-bottom:8px;margin-bottom:15px;font-size:1.4rem;}
.skill-category-icon{font-size:1.8rem;margin-right:10px;color:#5846f6;vertical-align:middle;}
.skill-item{background:var(--card-bg);padding:1rem;margin:0.5rem 0;border-radius:8px;border-left:3px solid var(--primary-color);transition:var(--transition);}
.skill-item:hover{transform:translateX(5px);background:rgba(88,70,246,0.12);}
.timeline{position:relative;padding-left:2rem;}
.timeline-item{position:relative;padding-bottom:2rem;opacity:0;animation:fadeInUp 1s ease forwards;}
.timeline::before{content:'';position:absolute;left:7.5px;top:0;height:100%;width:2px;background:linear-gradient(to bottom,var(--primary-color),transparent);}
.timeline-dot{position:absolute;left:-2rem;top:0.5rem;width:16px;height:16px;border-radius:50%;background:var(--primary-color);box-shadow:0 0 10px var(--primary-color);z-index:1;transform:scale(0);animation:popIn 0.5s ease forwards;}
@keyframes popIn{from{transform:scale(0);}to{transform:scale(1);}}
.timeline-date{font-size:0.9rem;font-weight:500;margin-bottom:0.5rem;color:var(--primary-color);opacity:0.9;}
.timeline-content{position:relative;padding:1.5rem;background:var(--card-bg);border-radius:var(--border-radius);box-shadow:var(--shadow);transition:var(--transition);border-left:4px solid var(--primary-color);}
.timeline-content:hover{transform:translateX(5px);}
.project-card{position:relative;overflow:hidden;border-radius:var(--border-radius);margin-bottom:2rem;background:var(--card-bg);box-shadow:var(--shadow);transition:var(--transition);}
.project-card:hover{transform:translateY(-10px);box-shadow:0 15px 30px rgba(0,0,0,0.3);}
.project-image{position:relative;width:100%;overflow:hidden;border-radius:var(--border-radius) var(--border-radius) 0 0;}
.project-image img{width:100%;transition:transform 1s ease;}
.project-card:hover .project-image img{transform:scale(1.05);}
.project-image::after{content:'';position:absolute;top:0;left:0;width:100%;height:100%;background:linear-gradient(to bottom,transparent,rgba(10,25,47,0.8));}
.project-meta{padding:0.5rem 1rem;}
.project-details{padding:1rem;}
.tech-stack{margin-top:1rem;}
.tech-badge{display:inline-block;padding:0.3rem 0.8rem;margin:0.3rem;border-radius:15px;background:rgba(88,70,246,0.1);border:1px solid var(--primary-color);color:var(--primary-color);font-size:0.8rem;transition:var(--transition);}
.tech-badge:hover{background:var(--primary-color);color:white;transform:translateY(-3px);}
.soft-skill-card{text-align:center;padding:2rem 1rem;background:var(--card-bg);border-radius:var(--border-radius);box-shadow:var(--shadow);transition:var(--transition);position:relative;overflow:hidden;height:100%;}
.soft-skill-card:hover{transform:translateY(-5px);}
.soft-skill-card::before{content:'';position:absolute;top:-100%;left:-100%;width:300%;height:300%;background:radial-gradient(circle,var(--primary-color) 0%,transparent 70%);opacity:0;transition:var(--transition);z-index:-1;}
.soft-skill-card:hover::before{opacity:0.05;transform:translate(10%,10%);}
.soft-skill-card i{font-size:2.5rem;color:var(--primary-color);margin-bottom:1rem;transition:var(--transition);}
.soft-skill-card:hover i{transform:scale(1.2) rotate(10deg);}
.soft-skill-card h4{font-size:1.2rem;margin-bottom:0.5rem;}
.language-card{text-align:center;padding:1.5rem;background:var(--card-bg);border-radius:var(--border-radius);box-shadow:var(--shadow);transition:var(--transition);height:100%;}
.language-card:hover{transform:translateY(-5px);box-shadow:0 10px 20px rgba(0,0,0,0.2);}
.language-icon{font-size:2.5rem;color:var(--primary-color);margin-bottom:1rem;transition:var(--transition);}
.language-card:hover .language-icon{transform:scale(1.2);}
.contact-item{display:flex;align-items:flex-start;margin-bottom:1.5rem;transition:var(--transition);}
.contact-item:hover{transform:translateX(5px);}
.contact-item i{font-size:1.5rem;color:var(--primary-color);margin-right:1rem;transition:var(--transition);}
.contact-item:hover i{transform:scale(1.2);}
.contact-item h4{margin-bottom:0.3rem;font-weight:600;}
.contact-item p{margin:0;opacity:0.9;}
.footer{text-align:center;padding:2rem 0;margin-top:3rem;background:linear-gradient(to top,rgba(10,25,47,0.9),transparent);backdrop-filter:blur(5px);}
.footer p{margin-bottom:0.5rem;opacity:0.8;}
.footer i{color:var(--primary-color);animation:heartbeat 1.5s infinite;}
@keyframes heartbeat{0%{transform:scale(1);}14%{transform:scale(1.3);}28%{transform:scale(1);}42%{transform:scale(1.3);}70%{transform:scale(1);}}
.form-error{color:#ff4444;font-size:0.9rem;margin-top:2px;}
.form-success{color:#4CAF50;padding:10px;border-radius:5px;background-color:rgba(76,175,80,0.1);border-left:4px solid #4CAF50;margin:10px 0;}
.required-field:after{content:" *";color:#ff4444;}
.accomplishment-card{display:flex;align-items:flex-start;background-color:rgba(88,70,246,0.05);padding:15px;border-radius:10px;margin-bottom:15px;transition:var(--transition);}
.accomplishment-card:hover{transform:translateX(5px);background-color:rgba(88,70,246,0.10);}
.accomplishment-icon{font-size:1.5rem;color:#5846f6;margin-right:15px;}
input,textarea{background-color:rgba(255,255,255,0.05)!important;border:1px solid rgba(88,70,246,0.3)!important;border-radius:var(--border-radius)!important;color:var(--text-color)!important;transition:var(--transition)!important;}
input:focus,textarea:focus{border-color:var(--primary-color)!important;box-shadow:0 0 0 2px rgba(88,70,246,0.2)!important;}
[data-testid="stForm"] [data-baseweb="button"]{background-color:var(--primary-color)!important;border-radius:var(--border-radius)!important;transition:var(--transition)!important;}
[data-testid="stForm"] [data-baseweb="button"]:hover{background-color:var(--secondary-color)!important;transform:translateY(-2px)!important;box-shadow:0 5px 15px rgba(88,70,246,0.3)!important;}
.nav-link{display:inline-block;padding:0.5rem 1rem;margin:0 0.5rem;color:var(--text-color);text-decoration:none;border-radius:5px;transition:var(--transition);}
.nav-link:hover{background:var(--primary-color);color:white;}
@media screen and (max-width:768px){.hero-section h1{font-size:2.5rem;}.hero-section h3{font-size:1.2rem;}.section-header h2{font-size:1.8rem;}.timeline{padding-left:1.5rem;}.timeline-dot{left:-1.5rem;}}
.fade-in{opacity:0;animation:fadeIn 1s ease forwards;}
@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}
</style>
""",unsafe_allow_html=True)
st.markdown('<div class="section" id="home">',unsafe_allow_html=True)
col1,col2=st.columns([2,1])
with col1:
st.markdown("""
<div class="hero-section fade-in">
<h1>Sivamahendranath <span class="highlight">Ragimanu</span></h1>
<h3>🎓 AI & Data Professional | Python Developer | LLM Specialist</h3>
<p class="lead-text">
<strong>Data Analyst</strong> with hands-on experience in <strong>Python</strong>, <strong>Machine Learning</strong>, <strong>LLMs (GPT-4, Gemini)</strong>, and <strong>RAG pipelines</strong>.<br><br>
✨ Interned at <strong>C-DAC Hyderabad</strong>, building AI-powered knowledge graphs, semantic search tools, and document analysis applications.<br>
🔧 Expert in <strong>data visualization</strong>, <strong>NLP</strong>, <strong>automated data processing</strong>, and <strong>interactive web apps</strong> using Streamlit.<br>
🚀 Passionate about transforming raw data into actionable insights through scalable AI solutions.<br><br>
<strong>Open to roles in:</strong> AI Engineering | Data Science | Python Development
</p>
</div>
""",unsafe_allow_html=True)
with col2:
profile_image_path=get_image_path("profile.jpeg")
if os.path.exists(profile_image_path):
profile_img=load_image(profile_image_path)
else:
profile_img=get_placeholder_image(300,300,color="#5846f6")
st.image(profile_img,use_container_width=True)
st.markdown("</div>",unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>',unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>About Me</h2></div>",unsafe_allow_html=True)
col1,col2=st.columns([1,2])
with col1:
about_image_path=get_image_path("about_me.jpeg")
if os.path.exists(about_image_path):
about_img=load_image(about_image_path)
else:
about_img=get_placeholder_image(400,400,color="#4a3bf5")
st.image(about_img,caption="Sivamahendranath Ragimanu",use_container_width=True)
with col2:
st.markdown("""
<div class="about-text fade-in">
<p style="font-size:1.1rem;line-height:1.8;">
I'm an aspiring <strong>AI & Data Science professional</strong> with deep expertise in <strong>Python</strong>, <strong>NLP</strong>, <strong>LLMs (GPT-4, Gemini)</strong>, and <strong>RAG pipelines</strong>. During my internship at <strong>C-DAC Hyderabad</strong>, I developed AI-powered applications including:
</p>
<ul style="font-size:1rem;line-height:1.8;">
<li>🔍 <strong>Knowledge Graph Generators</strong> with semantic relationship mapping</li>
<li>📄 <strong>Document Analysis Chatbots</strong> for intelligent Q&A</li>
<li>📊 <strong>Data Visualization Dashboards</strong> with Plotly and NetworkX</li>
<li>🤖 <strong>Entity Extraction Systems</strong> using NER and LLM integration</li>
</ul>
<p style="font-size:1.1rem;line-height:1.8;">
<strong>Core Technical Skills:</strong><br>
Python | GPT-4 & Gemini APIs | LangChain | Streamlit | SQLite3 | NetworkX | Pandas | Matplotlib | OpenCV | BeautifulSoup
</p>
<p style="font-size:1.1rem;line-height:1.8;">
I'm passionate about building <strong>scalable</strong>, <strong>data-driven AI solutions</strong> that emphasize <strong>privacy</strong>, <strong>interactivity</strong>, and <strong>real-world impact</strong>.
</p>
</div>
""",unsafe_allow_html=True)
st.markdown("""
<div class="key-points">
<div class="key-point"><i class="fas fa-map-marker-alt"></i> Anantapur, Andhra Pradesh, India</div>
<div class="key-point"><i class="fas fa-phone"></i> +91 8106442744</div>
<div class="key-point"><i class="fas fa-envelope"></i> mahendraragimanu2@gmail.com</div>
</div>
""",unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>',unsafe_allow_html=True)
st.markdown('<div class="section" id="skills">',unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Technical Skills</h2></div>",unsafe_allow_html=True)
skill_categories={
"Operating Systems":{"icon":"fas fa-desktop","skills":["Windows","Linux (Ubuntu)"]},
"Programming & Tools":{"icon":"fas fa-code","skills":["Python","C","SQL"]},
"Technologies":{"icon":"fas fa-brain","skills":["LLMs (GPT-4, Gemini)","RAG Pipelines","Machine Learning","Artificial Intelligence","Virtualization (VirtualBox)"]}
}
for category,data in skill_categories.items():
st.markdown(f"""
<div class="skill-category">
<h3><i class="{data['icon']} skill-category-icon"></i>{category}</h3>
</div>
""",unsafe_allow_html=True)
col1,col2=st.columns(2)
skills_list=data["skills"]
half=len(skills_list)//2+len(skills_list)%2
with col1:
for skill in skills_list[:half]:
st.markdown(f"""
<div class="skill-item fade-in">
<div class="skill-name">{skill}</div>
</div>
""",unsafe_allow_html=True)
with col2:
for skill in skills_list[half:]:
st.markdown(f"""
<div class="skill-item fade-in">
<div class="skill-name">{skill}</div>
</div>
""",unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Soft Skills</h2></div>",unsafe_allow_html=True)
soft_skills=["Communication","Team Work","Leadership","Problem Solving","Analytical Thinking"]
col1,col2,col3=st.columns(3)
cols=[col1,col2,col3]
for i,skill in enumerate(soft_skills):
with cols[i%3]:
st.markdown(f"""
<div class="soft-skill-card fade-in">
<i class="fas fa-check-circle"></i>
<h4>{skill}</h4>
</div>
""",unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Work Experience</h2></div>",unsafe_allow_html=True)
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
""",unsafe_allow_html=True)
st.markdown("""
<ul style="margin-top:-20px;margin-left:40px;">
<li>Created data pipelines and visualized datasets with <strong>Pandas</strong>, <strong>Matplotlib</strong>, and <strong>Streamlit</strong> in Python for quick insights on data.</li>
<li>Used <strong>GPT-4</strong>, <strong>Gemini APIs</strong>, and <strong>NLP</strong> to extract structured data from raw text, improving data processing accuracy by <strong>30%</strong>.</li>
<li>Designed and optimized <strong>SQLite databases</strong> for storage of knowledge graph data that are scalable and helped with quick querying.</li>
<li>Built dynamic and interactive graph visualizations using <strong>NetworkX</strong> and <strong>Pyvis</strong> to help stakeholders understand the graphs and make better-informed decisions.</li>
<li>Built automation tools for collecting data using <strong>BeautifulSoup</strong> and led AI-powered projects that demonstrated my expertise in <strong>LLM integration</strong>, <strong>backend design</strong>, and <strong>Python scripting</strong>.</li>
</ul>
""",unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Professional Accomplishments</h2></div>",unsafe_allow_html=True)
accomplishments=[
{"title":"Event Organizer","icon":"fas fa-calendar-check","detail":"Leading as an Event Organizer (Coding, Workshops) at KSRM College of Engineering."},
{"title":"Team Leader","icon":"fas fa-users","detail":"Serving as Team Leader for both minor and major projects at KSRM College of Engineering."},
{"title":"Coder","icon":"fas fa-code","detail":"Actively involved as a coder in the major project development."}
]
col1,col2=st.columns(2)
for i,acc in enumerate(accomplishments):
with col1 if i%2==0 else col2:
st.markdown(f"""
<div class="accomplishment-card fade-in">
<div class="accomplishment-icon"><i class="{acc['icon']}"></i></div>
<div class="accomplishment-content">
<h4>{acc['title']}</h4>
<p>{acc['detail']}</p>
</div>
</div>
""",unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>',unsafe_allow_html=True)
st.markdown('<div class="section" id="projects">',unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Personal Projects</h2></div>",unsafe_allow_html=True)
projects=[
{
"title":"AI-Powered Knowledge Graph Generator using LLMs and Graph Visualization Application",
"date":"January 2025 - March 2025",
"org":"C-DAC, Hyderabad",
"description":"AI-powered knowledge graph system with semantic exploration capabilities",
"features":[
"Implemented an <strong>LLM-based pipeline</strong> using <strong>Google Gemini</strong> to extract entities & relationships from text sources.",
"Built dynamic, expandable knowledge graphs with <strong>NetworkX</strong> & <strong>Pyvis</strong>, enabling semantic exploration.",
"Stored extracted data in a structured <strong>SQLite3 schema</strong> to support complex querying."
],
"tech_stack":["Python","Streamlit","Google Gemini API","SQLite3","NetworkX","Pyvis","BeautifulSoup"],
"github":"https://github.com/Sivamahendranath/Gemini_Knowledge_Graph/blob/main/backup.py"
},
{
"title":"DocuGenius Pro: Streamlit-Based AI-Powered Document Processing Application (Chatbot)",
"date":"January 2025 - Personal Mini Project",
"org":"C-DAC, Hyderabad",
"description":"End-to-end AI document processing application with smart analytics",
"features":[
"Built an end-to-end document processing application with <strong>Streamlit</strong> and <strong>Google Gemini API</strong>.",
"Added support for <strong>Text</strong>, <strong>PDFs</strong>, <strong>CSVs</strong>, and <strong>URLs</strong> with smart analysis, summaries, and AI-powered Q&A.",
"Implemented <strong>Plotly visualizations</strong> and <strong>NER-based entity extraction</strong> for advanced analytics.",
"Enabled custom themes and exportable reports (<strong>CSV</strong>/<strong>JSON</strong>/<strong>PDF</strong>) for enhanced user experience."
],
"tech_stack":["Python","Streamlit","Google Gemini API","Plotly","NLP","NER"],
"github":"https://github.com/Sivamahendranath/Gemini-Document-RAG/blob/main/code/main.py"
},
{
"title":"Exam Proctoring System Using Machine Learning",
"date":"December 2023 - March 2024",
"org":"KSRM College Of Engineering, Kadapa",
"description":"ML-based live exam monitoring and integrity system",
"features":[
"Led a <strong>4-member team</strong> to build a live exam proctoring system using <strong>OpenCV</strong>, <strong>Dlib</strong>, and <strong>facial recognition</strong>.",
"Automated activity monitoring with <strong>warning triggers</strong> and <strong>report generation</strong>, improving exam integrity.",
"Delivered a fully functional monitoring platform with <strong>alerts</strong> and <strong>analytics dashboards</strong>."
],
"tech_stack":["Python","OpenCV","Dlib","Face Recognition","Machine Learning"],
"github":"https://github.com/Sivamahendranath/Exam-Proctoring-System"
}
]
for i,project in enumerate(projects):
st.markdown(f"""
<div class="project-card fade-in">
<div class="project-details">
<h3>{project["title"]}</h3>
<div class="project-meta">
<div><i class="far fa-calendar-alt"></i> {project["date"]}</div>
<div><i class="fas fa-building"></i> {project["org"]}</div>
</div>
<p class="project-description" style="font-style:italic;">{project["description"]}</p>
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
<div style="margin-top:15px;">
<a href="{project["github"]}" target="_blank" style="color:#5846f6;">
<i class="fab fa-github"></i> View on GitHub
</a>
</div>
</div>
</div>
""",unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>',unsafe_allow_html=True)
st.markdown('<div class="section" id="education">',unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Education</h2></div>",unsafe_allow_html=True)
education=[
{
"degree":"HPC-AI Certification Course",
"institution":"Centre for Development of Advanced Computing (C-DAC)",
"location":"Bangalore",
"duration":"August 2025 - Present",
"grade":"In Progress",
"courses":["High-Performance Computing","Cloud Infrastructure","AI-Driven System Automation"]
},
{
"degree":"Bachelor's Of Technology (B.Tech) in Computer Science and Engineering",
"institution":"KSRM College Of Engineering, JNTUA",
"location":"Kadapa",
"duration":"Dec 2020 - Apr 2024",
"grade":"8.3/10 CGPA",
"courses":["Data Structures","Algorithms","Machine Learning","Web Development","Database Management"]
},
{
"degree":"Higher Secondary School (MPC)",
"institution":"JCDR Junior College",
"location":"Anantapur",
"duration":"Jun 2018 - Mar 2020",
"grade":"6.21/10 CGPA",
"courses":["Mathematics","Physics","Chemistry"]
},
{
"degree":"Secondary School Certificate",
"institution":"ZP High School",
"location":"Anantapur",
"duration":"Jun 2017 - Mar 2018",
"grade":"9.0/10 CGPA",
"courses":["Mathematics","Science","Languages"]
}
]
for i,edu in enumerate(education):
st.markdown(f"""
<div class="timeline-item fade-in">
<div class="timeline-dot"></div>
<div class="timeline-date">{edu["duration"]}</div>
<div class="timeline-content custom-card">
<h3>{edu["degree"]}</h3>
<h4>{edu["institution"]}, {edu["location"]}</h4>
<div class="education-grade">
<span><i class="fas fa-star"></i> {edu["grade"]}</span>
</div>
<div class="key-courses" style="margin-top:10px;">
<h5>Key Courses:</h5>
<p>{", ".join(edu["courses"])}</p>
</div>
</div>
</div>
""",unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Languages</h2></div>",unsafe_allow_html=True)
languages=[
{"name":"English","proficiency":"Professional","icon":"fas fa-comment-dots"},
{"name":"Telugu","proficiency":"Native","icon":"fas fa-comments"},
{"name":"Hindi","proficiency":"Intermediate","icon":"fas fa-comment-alt"}
]
cols=st.columns(3)
for i,lang in enumerate(languages):
with cols[i]:
st.markdown(f"""
<div class="language-card fade-in">
<div class="language-icon">
<i class="{lang['icon']}"></i>
</div>
<h4>{lang["name"]}</h4>
<p>{lang["proficiency"]}</p>
</div>
""",unsafe_allow_html=True)
st.markdown('</div>',unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>',unsafe_allow_html=True)
st.markdown('<div class="section" id="contact">',unsafe_allow_html=True)
st.markdown("<div class='section-header'><h2>Contact Me</h2></div>",unsafe_allow_html=True)
col1,col2=st.columns([2,1])
with col1:
st.markdown("<h3>Send me a message</h3>",unsafe_allow_html=True)
if 'name_error' not in st.session_state:
st.session_state.name_error=""
if 'email_error' not in st.session_state:
st.session_state.email_error=""
if 'message_error' not in st.session_state:
st.session_state.message_error=""
if 'form_submitted' not in st.session_state:
st.session_state.form_submitted=False
if st.session_state.form_submitted:
st.markdown('<div class="form-success">Thank you for your message! I will get back to you soon.</div>',unsafe_allow_html=True)
st.session_state.form_submitted=False
with st.form("contact_form",clear_on_submit=True):
st.markdown('<label class="required-field">Name</label>',unsafe_allow_html=True)
name=st.text_input("",placeholder="Your name",key="name")
if st.session_state.name_error:
st.markdown(f'<div class="form-error">{st.session_state.name_error}</div>',unsafe_allow_html=True)
st.markdown('<label class="required-field">Email</label>',unsafe_allow_html=True)
email=st.text_input("",placeholder="Your email",key="email")
if st.session_state.email_error:
st.markdown(f'<div class="form-error">{st.session_state.email_error}</div>',unsafe_allow_html=True)
st.markdown('<label class="required-field">Message</label>',unsafe_allow_html=True)
message=st.text_area("",placeholder="Your message",height=150,key="message")
if st.session_state.message_error:
st.markdown(f'<div class="form-error">{st.session_state.message_error}</div>',unsafe_allow_html=True)
submitted=st.form_submit_button("Send Message")
if submitted:
st.session_state.name_error=""
st.session_state.email_error=""
st.session_state.message_error=""
valid_form=True
if not name.strip():
st.session_state.name_error="Please enter your name."
valid_form=False
if not email.strip():
st.session_state.email_error="Please enter your email."
valid_form=False
elif not is_valid_email(email):
st.session_state.email_error="Please enter a valid email address."
valid_form=False
if not message.strip():
st.session_state.message_error="Please enter your message."
valid_form=False
if valid_form:
save_message_to_db(name,email,message)
try:
send_email_notification(name,email,message)
except Exception as e:
pass
st.session_state.form_submitted=True
st.rerun()
with col2:
st.markdown("### 📱 Contact Information")
st.markdown("#### 📍 Location")
st.write("Anantapur, Andhra Pradesh, India")
st.markdown("#### ✉️ Email")
st.write("mahendraragimanu2@gmail.com")
st.markdown("#### ☎️ Phone")
st.write("+91 8106442744")
st.markdown("#### 🔗 Connect With Me")
social_cols=st.columns(3)
with social_cols[0]:
st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sivamahendranath-ragimanu-68a94823b/)")
with social_cols[1]:
st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Sivamahendranath)")
with social_cols[2]:
st.markdown("[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:mahendraragimanu2@gmail.com)")
st.markdown('</div>',unsafe_allow_html=True)
st.markdown("""
<div class="footer">
<p>&copy; 2025 Sivamahendranath Ragimanu | All Rights Reserved</p>
<p>Made with <i class="fas fa-heart"></i> using Streamlit</p>
</div>
""",unsafe_allow_html=True)
