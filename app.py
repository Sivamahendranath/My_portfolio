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

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="Sivamahendranath Ragimanu | AI Developer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/yourusername',
        'Report a bug': 'mailto:mahendraragimanu2@gmail.com',
        'About': '# AI-Powered Portfolio\nVersion 3.0 - Production Ready'
    }
)

# Initialize session state
if 'form_submissions' not in st.session_state:
    st.session_state.form_submissions = []
if 'page_loaded' not in st.session_state:
    st.session_state.page_loaded = False
if 'preloader_done' not in st.session_state:
    st.session_state.preloader_done = False

def load_custom_css():
    """Enhanced CSS with advanced animated background"""
    custom_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;600;700&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
        
        /* ============ ROOT & GLOBAL VARIABLES ============ */
        :root {
            --primary-color: #00ff41;
            --secondary-color: #7877c6;
            --accent-color: #ff006e;
            --bg-dark: #0a0a0a;
            --bg-darker: #050505;
            --text-primary: #ffffff;
            --text-secondary: #b0b0b0;
            --glow-primary: rgba(0, 255, 65, 0.5);
            --glow-secondary: rgba(120, 119, 198, 0.5);
        }
        
        /* ============ GLOBAL STYLES ============ */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body {
            scroll-behavior: smooth;
            overflow-x: hidden;
        }
        
        /* ============ ANIMATED PARTICLE BACKGROUND ============ */
        .particle-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        }
        
        /* ============ STREAMLIT APP CONTAINER ============ */
        [data-testid="stAppViewContainer"] {
            background: transparent;
            position: relative;
        }
        
        [data-testid="stApp"] {
            background: transparent;
        }
        
        [data-testid="stHeader"] {
            background: rgba(10, 10, 10, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(0, 255, 65, 0.1);
        }
        
        [data-testid="stMainBlockContainer"] {
            padding-top: 1rem;
            padding-bottom: 3rem;
            max-width: 100%;
            position: relative;
            z-index: 1;
        }
        
        section[data-testid="stMain"] {
            background: transparent;
            padding: 0rem 1rem;
        }
        
        /* ============ ANIMATED GRID OVERLAY ============ */
        [data-testid="stAppViewContainer"]::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                linear-gradient(rgba(0, 255, 65, 0.02) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 255, 65, 0.02) 1px, transparent 1px);
            background-size: 60px 60px;
            animation: gridMove 30s linear infinite;
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes gridMove {
            0% { background-position: 0 0; }
            100% { background-position: 60px 60px; }
        }
        
        /* ============ FLOATING GRADIENT ORBS ============ */
        [data-testid="stAppViewContainer"]::after {
            content: '';
            position: fixed;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(0, 255, 65, 0.15) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(120, 119, 198, 0.12) 0%, transparent 45%),
                radial-gradient(circle at 50% 50%, rgba(255, 0, 110, 0.1) 0%, transparent 35%),
                radial-gradient(circle at 10% 80%, rgba(0, 204, 255, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 90% 20%, rgba(255, 195, 0, 0.08) 0%, transparent 40%);
            animation: orbFloat 25s ease-in-out infinite;
            pointer-events: none;
            z-index: 0;
        }
        
        @keyframes orbFloat {
            0%, 100% { 
                transform: translate(0, 0) rotate(0deg) scale(1);
                opacity: 0.6;
            }
            25% { 
                transform: translate(100px, -100px) rotate(90deg) scale(1.2);
                opacity: 0.8;
            }
            50% { 
                transform: translate(-50px, 50px) rotate(180deg) scale(0.9);
                opacity: 0.7;
            }
            75% { 
                transform: translate(80px, 80px) rotate(270deg) scale(1.1);
                opacity: 0.85;
            }
        }
        
        /* ============ WAVE ANIMATION LAYER ============ */
        .wave-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 200px;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
            opacity: 0.3;
        }
        
        .wave {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 200%;
            height: 100%;
            background: linear-gradient(180deg, transparent, rgba(0, 255, 65, 0.1));
            border-radius: 100% 100% 0 0;
            animation: wave 15s linear infinite;
        }
        
        .wave:nth-child(2) {
            background: linear-gradient(180deg, transparent, rgba(120, 119, 198, 0.08));
            animation: wave 20s linear infinite reverse;
            opacity: 0.7;
        }
        
        .wave:nth-child(3) {
            background: linear-gradient(180deg, transparent, rgba(255, 0, 110, 0.06));
            animation: wave 25s linear infinite;
            opacity: 0.5;
        }
        
        @keyframes wave {
            0% { transform: translateX(0) translateY(0); }
            50% { transform: translateX(-25%) translateY(-20px); }
            100% { transform: translateX(-50%) translateY(0); }
        }
        
        /* ============ FLOATING GEOMETRIC SHAPES ============ */
        .geometric-shapes {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            pointer-events: none;
            overflow: hidden;
        }
        
        .shape {
            position: absolute;
            opacity: 0.05;
            animation: floatShape 20s ease-in-out infinite;
        }
        
        .shape:nth-child(1) {
            top: 10%;
            left: 10%;
            width: 80px;
            height: 80px;
            border: 2px solid var(--primary-color);
            border-radius: 50%;
            animation-duration: 25s;
            animation-delay: 0s;
        }
        
        .shape:nth-child(2) {
            top: 60%;
            left: 80%;
            width: 100px;
            height: 100px;
            border: 2px solid var(--secondary-color);
            transform: rotate(45deg);
            animation-duration: 30s;
            animation-delay: 2s;
        }
        
        .shape:nth-child(3) {
            top: 30%;
            left: 70%;
            width: 60px;
            height: 60px;
            border: 2px solid var(--accent-color);
            clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
            animation-duration: 22s;
            animation-delay: 4s;
        }
        
        .shape:nth-child(4) {
            top: 80%;
            left: 20%;
            width: 90px;
            height: 90px;
            border: 2px solid #00ccff;
            border-radius: 20%;
            animation-duration: 28s;
            animation-delay: 1s;
        }
        
        .shape:nth-child(5) {
            top: 50%;
            left: 50%;
            width: 70px;
            height: 70px;
            border: 2px solid #ffc300;
            clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
            animation-duration: 26s;
            animation-delay: 3s;
        }
        
        @keyframes floatShape {
            0%, 100% {
                transform: translate(0, 0) rotate(0deg);
                opacity: 0.05;
            }
            25% {
                transform: translate(50px, -50px) rotate(90deg);
                opacity: 0.08;
            }
            50% {
                transform: translate(-30px, 30px) rotate(180deg);
                opacity: 0.06;
            }
            75% {
                transform: translate(40px, 40px) rotate(270deg);
                opacity: 0.09;
            }
        }
        
        /* ============ SCANLINE EFFECT ============ */
        .scanline {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
            box-shadow: 0 0 20px var(--glow-primary);
            animation: scanlineMove 4s linear infinite;
            z-index: 0;
            pointer-events: none;
            opacity: 0.3;
        }
        
        @keyframes scanlineMove {
            0% { top: 0%; }
            100% { top: 100%; }
        }
        
        /* ============ PRELOADER ============ */
        .preloader {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #0a0a0a 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            animation: preloaderFade 0.8s ease 3s forwards;
        }
        
        @keyframes preloaderFade {
            to {
                opacity: 0;
                visibility: hidden;
            }
        }
        
        .preloader-content {
            text-align: center;
            animation: glitchPulse 2s ease-in-out infinite;
        }
        
        .preloader-logo {
            font-size: 4rem;
            font-weight: 900;
            font-family: 'Fira Code', monospace;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color), var(--accent-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
            animation: logoGlow 2s ease-in-out infinite;
        }
        
        @keyframes logoGlow {
            0%, 100% {
                filter: drop-shadow(0 0 20px var(--glow-primary));
            }
            50% {
                filter: drop-shadow(0 0 40px var(--glow-secondary)) drop-shadow(0 0 60px var(--glow-primary));
            }
        }
        
        .preloader-text {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.2rem;
            color: var(--primary-color);
            letter-spacing: 3px;
            margin-top: 1rem;
        }
        
        .loading-bar {
            width: 300px;
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            overflow: hidden;
            margin-top: 2rem;
        }
        
        .loading-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-color), var(--secondary-color), var(--accent-color));
            animation: loadingProgress 3s ease-in-out forwards;
            box-shadow: 0 0 20px var(--glow-primary);
        }
        
        @keyframes loadingProgress {
            from { width: 0%; }
            to { width: 100%; }
        }
        
        /* ============ CYBERPUNK TABS ============ */
        [data-testid="stTabs"] {
            position: relative;
            z-index: 10;
        }
        
        [data-testid="stTabs"] [data-baseweb="tab-list"] {
            gap: 1rem;
            animation: slideInDown 1s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            padding: 8px;
            background: rgba(10, 10, 10, 0.8);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            border: 1px solid rgba(0, 255, 65, 0.2);
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.1);
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
            height: 45px;
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            border: 1px solid rgba(255, 255, 255, 0.05);
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.7) !important;
            font-size: 1rem;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }
        
        [data-testid="stTabs"] [data-baseweb="tab"]:hover {
            background: rgba(0, 255, 65, 0.1);
            transform: translateY(-3px);
            box-shadow: 
                0 10px 30px rgba(0, 255, 65, 0.2),
                inset 0 0 20px rgba(0, 255, 65, 0.05);
            border: 1px solid rgba(0, 255, 65, 0.5);
            color: var(--primary-color) !important;
        }
        
        [data-testid="stTabs"] [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(0, 255, 65, 0.15), rgba(120, 119, 198, 0.1)) !important;
            border: 1px solid var(--primary-color) !important;
            box-shadow: 
                0 0 30px var(--glow-primary),
                inset 0 0 20px rgba(0, 255, 65, 0.1) !important;
            color: var(--primary-color) !important;
            text-shadow: 0 0 10px var(--glow-primary);
        }
        
        [data-testid="stTabs"] [aria-selected="true"]::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0, 255, 65, 0.3), transparent);
            animation: scanLine 2s ease-in-out infinite;
        }
        
        @keyframes scanLine {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        /* ============ CYBERPUNK GLASS CARDS ============ */
        .card-container {
            background: rgba(10, 10, 10, 0.6) !important;
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-radius: 20px;
            padding: 30px 25px;
            margin: 20px 0;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.05),
                0 0 20px rgba(0, 255, 65, 0.05);
            border: 1px solid rgba(0, 255, 65, 0.2);
            position: relative;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            animation: cardSlideUp 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) backwards;
            overflow: hidden;
        }
        
        @keyframes cardSlideUp {
            from {
                opacity: 0;
                transform: translateY(50px) scale(0.95);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        
        .card-container:hover {
            background: rgba(10, 10, 10, 0.8) !important;
            transform: translateY(-10px);
            box-shadow: 
                0 20px 60px rgba(0, 255, 65, 0.15),
                inset 0 1px 0 rgba(0, 255, 65, 0.2),
                0 0 40px rgba(0, 255, 65, 0.1);
            border: 1px solid rgba(0, 255, 65, 0.4);
        }
        
        .card-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 30px;
            height: 30px;
            border-top: 2px solid var(--primary-color);
            border-left: 2px solid var(--primary-color);
            opacity: 0.5;
            transition: all 0.3s ease;
        }
        
        .card-container::after {
            content: '';
            position: absolute;
            bottom: 0;
            right: 0;
            width: 30px;
            height: 30px;
            border-bottom: 2px solid var(--primary-color);
            border-right: 2px solid var(--primary-color);
            opacity: 0.5;
            transition: all 0.3s ease;
        }
        
        .card-container:hover::before,
        .card-container:hover::after {
            width: 60px;
            height: 60px;
            opacity: 1;
        }
        
        .card-container > * {
            position: relative;
            z-index: 1;
        }
        
        /* ============ GLOWING HEADER TEXT ============ */
        .glow-text {
            font-family: 'Space Grotesk', sans-serif;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color), var(--accent-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: textPulse 3s ease-in-out infinite;
            font-weight: 900;
            display: inline-block;
            position: relative;
        }
        
        @keyframes textPulse {
            0%, 100% {
                filter: brightness(1) drop-shadow(0 0 20px var(--glow-primary));
            }
            50% {
                filter: brightness(1.4) drop-shadow(0 0 40px var(--glow-secondary));
            }
        }
        
        /* ============ TYPEWRITER EFFECT ============ */
        .typewriter {
            font-family: 'Fira Code', monospace;
            color: var(--primary-color);
            border-right: 2px solid var(--primary-color);
            animation: typing 3.5s steps(40, end), blink 0.75s step-end infinite;
            white-space: nowrap;
            overflow: hidden;
            display: inline-block;
        }
        
        @keyframes typing {
            from { width: 0; }
            to { width: 100%; }
        }
        
        @keyframes blink {
            from, to { border-color: transparent; }
            50% { border-color: var(--primary-color); }
        }
        
        /* ============ GLITCH EFFECT ============ */
        .glitch {
            position: relative;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            animation: glitch 1s linear infinite;
        }
        
        @keyframes glitch {
            2%, 64% {
                transform: translate(2px, 0) skew(0deg);
            }
            4%, 60% {
                transform: translate(-2px, 0) skew(0deg);
            }
            62% {
                transform: translate(0, 0) skew(5deg);
            }
        }
        
        .glitch:before,
        .glitch:after {
            content: attr(data-text);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        
        .glitch:before {
            left: 2px;
            text-shadow: -2px 0 var(--accent-color);
            clip: rect(44px, 450px, 56px, 0);
            animation: glitch-anim 5s infinite linear alternate-reverse;
        }
        
        .glitch:after {
            left: -2px;
            text-shadow: -2px 0 var(--primary-color);
            clip: rect(44px, 450px, 56px, 0);
            animation: glitch-anim2 5s infinite linear alternate-reverse;
        }
        
        @keyframes glitch-anim {
            0% { clip: rect(10px, 9999px, 31px, 0); }
            20% { clip: rect(70px, 9999px, 71px, 0); }
            40% { clip: rect(60px, 9999px, 130px, 0); }
            60% { clip: rect(90px, 9999px, 110px, 0); }
            80% { clip: rect(50px, 9999px, 90px, 0); }
            100% { clip: rect(30px, 9999px, 50px, 0); }
        }
        
        @keyframes glitch-anim2 {
            0% { clip: rect(65px, 9999px, 119px, 0); }
            20% { clip: rect(20px, 9999px, 40px, 0); }
            40% { clip: rect(80px, 9999px, 120px, 0); }
            60% { clip: rect(40px, 9999px, 60px, 0); }
            80% { clip: rect(90px, 9999px, 150px, 0); }
            100% { clip: rect(50px, 9999px, 100px, 0); }
        }
        
        /* ============ NEON SKILL BADGES ============ */
        .skill-badge {
            display: inline-block;
            background: rgba(0, 255, 65, 0.05);
            border: 1px solid rgba(0, 255, 65, 0.3);
            padding: 10px 20px;
            border-radius: 8px;
            margin: 6px 8px;
            font-family: 'Fira Code', monospace;
            font-weight: 500;
            font-size: 0.95rem;
            color: var(--primary-color) !important;
            box-shadow: 
                0 0 10px rgba(0, 255, 65, 0.2),
                inset 0 0 10px rgba(0, 255, 65, 0.05);
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }
        
        .skill-badge:hover {
            background: rgba(0, 255, 65, 0.15);
            transform: translateY(-3px) scale(1.05);
            box-shadow: 
                0 0 30px var(--glow-primary),
                inset 0 0 20px rgba(0, 255, 65, 0.1);
            border: 1px solid var(--primary-color);
            text-shadow: 0 0 10px var(--glow-primary);
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
                transparent 30%,
                rgba(0, 255, 65, 0.3) 50%,
                transparent 70%
            );
            transform: rotate(45deg);
            transition: all 0.6s;
            opacity: 0;
        }
        
        .skill-badge:hover::before {
            opacity: 1;
            left: 100%;
        }
        
        /* ============ 3D IMAGE CONTAINERS ============ */
        .image-container {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 
                0 10px 40px rgba(0, 0, 0, 0.5),
                0 0 20px rgba(0, 255, 65, 0.2);
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            border: 1px solid rgba(0, 255, 65, 0.3);
        }
        
        .image-container:hover {
            transform: translateY(-8px) scale(1.03);
            box-shadow: 
                0 20px 60px rgba(0, 255, 65, 0.3),
                0 0 40px var(--glow-primary);
            border: 1px solid var(--primary-color);
        }
        
        .image-container img {
            width: 100%;
            height: auto;
            display: block;
            transition: transform 0.5s;
            filter: brightness(0.9);
        }
        
        .image-container:hover img {
            transform: scale(1.05);
            filter: brightness(1);
        }
        
        /* ============ NEON DIVIDERS ============ */
        .animated-divider {
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--primary-color), var(--secondary-color), var(--accent-color), transparent);
            margin: 2rem 0;
            animation: dividerGlow 3s ease-in-out infinite;
            box-shadow: 0 0 20px var(--glow-primary);
            border-radius: 2px;
            position: relative;
        }
        
        @keyframes dividerGlow {
            0%, 100% {
                opacity: 0.6;
                box-shadow: 0 0 20px var(--glow-primary);
            }
            50% {
                opacity: 1;
                box-shadow: 0 0 40px var(--glow-primary);
            }
        }
        
        .animated-divider::after {
            content: '';
            position: absolute;
            top: -3px;
            width: 8px;
            height: 8px;
            background: var(--primary-color);
            border-radius: 50%;
            box-shadow: 0 0 15px var(--glow-primary);
            animation: dotMove 3s linear infinite;
        }
        
        @keyframes dotMove {
            0% { left: 0%; }
            100% { left: 100%; }
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
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* ============ FLOAT ANIMATION ============ */
        .float-animation {
            animation: floatUpDown 4s ease-in-out infinite;
        }
        
        @keyframes floatUpDown {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-15px); }
        }
        
        /* ============ BUTTONS ============ */
        .stButton > button {
            background: linear-gradient(135deg, rgba(0, 255, 65, 0.2), rgba(120, 119, 198, 0.2));
            color: var(--primary-color) !important;
            padding: 14px 32px;
            border: 1px solid var(--primary-color);
            border-radius: 10px;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.05rem;
            font-weight: 600;
            letter-spacing: 1px;
            box-shadow: 
                0 0 20px rgba(0, 255, 65, 0.3),
                inset 0 0 10px rgba(0, 255, 65, 0.1);
            transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            width: 100%;
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 
                0 10px 40px var(--glow-primary),
                inset 0 0 20px rgba(0, 255, 65, 0.2);
            background: linear-gradient(135deg, rgba(0, 255, 65, 0.3), rgba(120, 119, 198, 0.3));
            border: 1px solid var(--primary-color);
            text-shadow: 0 0 10px var(--glow-primary);
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        /* ============ FORM INPUTS ============ */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: rgba(0, 0, 0, 0.5) !important;
            border: 1px solid rgba(0, 255, 65, 0.3) !important;
            color: var(--text-primary) !important;
            padding: 16px 20px !important;
            border-radius: 10px !important;
            font-family: 'Fira Code', monospace !important;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.3);
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            background: rgba(0, 0, 0, 0.7) !important;
            border: 1px solid var(--primary-color) !important;
            box-shadow: 
                0 0 30px var(--glow-primary),
                inset 0 0 15px rgba(0, 255, 65, 0.1) !important;
            transform: translateY(-2px);
        }
        
        /* ============ TEXT COLORS ============ */
        .stMarkdown, p, h1, h2, h3, h4, h5, h6, span, div, li {
            color: var(--text-primary) !important;
        }
        
        h1, h2, h3 {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
        }
        
        /* ============ CUSTOM SCROLLBAR ============ */
        ::-webkit-scrollbar {
            width: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.3);
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
            border-radius: 10px;
            box-shadow: 0 0 10px var(--glow-primary);
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, var(--secondary-color), var(--accent-color));
            box-shadow: 0 0 20px var(--glow-secondary);
        }
        
        /* ============ RESPONSIVE DESIGN ============ */
        @media (max-width: 768px) {
            .preloader-logo {
                font-size: 2.5rem;
            }
            
            .card-container {
                padding: 20px 15px;
                margin: 15px 0;
            }
            
            [data-testid="stTabs"] [data-baseweb="tab"] {
                padding: 10px 12px;
                font-size: 0.85rem;
            }
            
            .glow-text {
                font-size: 1.8rem !important;
            }
            
            .skill-badge {
                padding: 8px 14px;
                font-size: 0.85rem;
            }
            
            .shape {
                display: none;
            }
        }
        
        /* ============ PERFORMANCE ============ */
        @media (prefers-reduced-motion: reduce) {
            *,
            *::before,
            *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
        
        a {
            color: var(--primary-color) !important;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        
        a:hover {
            color: var(--secondary-color) !important;
            text-shadow: 0 0 10px var(--glow-primary);
        }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def show_animated_background():
    """Display animated background layers"""
    background_html = """
    <!-- Wave Container -->
    <div class="wave-container">
        <div class="wave"></div>
        <div class="wave"></div>
        <div class="wave"></div>
    </div>
    
    <!-- Geometric Shapes -->
    <div class="geometric-shapes">
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
        <div class="shape"></div>
    </div>
    
    <!-- Scanline Effect -->
    <div class="scanline"></div>
    """
    st.markdown(background_html, unsafe_allow_html=True)

def show_preloader():
    """Display preloader animation"""
    preloader_html = """
    <div class="preloader">
        <div class="preloader-content">
            <div class="preloader-logo">🚀</div>
            <div class="preloader-text">INITIALIZING AI PORTFOLIO...</div>
            <div class="loading-bar">
                <div class="loading-bar-fill"></div>
            </div>
        </div>
    </div>
    <script>
        setTimeout(() => {
            document.querySelector('.preloader').style.display = 'none';
        }, 3000);
    </script>
    """
    st.markdown(preloader_html, unsafe_allow_html=True)

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
            return get_placeholder_image(400, 400, color="#00ff41")
    except Exception as e:
        logger.error(f"Error loading image {image_path}: {e}")
        return get_placeholder_image(400, 400, color="#00ff41")

def get_placeholder_image(width, height, color="#00ff41"):
    """Generate placeholder image"""
    img = Image.new('RGB', (width, height), color=color)
    return img

def rate_limit_check():
    """Rate limiting"""
    current_time = time.time()
    st.session_state.form_submissions = [
        t for t in st.session_state.form_submissions 
        if current_time - t < 3600
    ]
    return len(st.session_state.form_submissions) < 5

def save_message_to_db(name, email, message):
    """Save contact messages"""
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
        <body style="font-family: 'Courier New', monospace; background: #0a0a0a; padding: 40px;">
            <div style="max-width: 600px; margin: 0 auto; background: rgba(0,255,65,0.05); padding: 40px; border-radius: 15px; border: 1px solid #00ff41;">
                <h2 style="color: #00ff41;">⚡ NEW CONTACT FORM SUBMISSION</h2>
                <div style="background: rgba(0,0,0,0.5); padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 3px solid #00ff41;">
                    <p style="color: #fff;"><strong style="color: #00ff41;">NAME:</strong> {name}</p>
                    <p style="color: #fff;"><strong style="color: #00ff41;">EMAIL:</strong> {email}</p>
                </div>
                <div style="background: rgba(0,0,0,0.5); padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 3px solid #7877c6;">
                    <p style="color: #fff;"><strong style="color: #00ff41;">MESSAGE:</strong></p>
                    <p style="color: #ddd;">{message}</p>
                </div>
                <hr style="border: 1px solid rgba(0,255,65,0.2);">
                <p style="color: #999; font-size: 12px; text-align: center;">
                    🤖 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                </p>
            </div>
        </body>
        </html>
        """
        
        email_message.attach(MIMEText(html_content, "html"))
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(email_message)
        
        logger.info(f"Email sent for: {name}")
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

def is_valid_email(email):
    """Email validation"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(email_pattern, email))

def sanitize_input(text):
    """Sanitize input"""
    return text.strip()[:500]

# Portfolio data
ABOUT = """I'm an aspiring AI & Data Science Professional with hands-on experience in Python, Machine Learning, LLMs (GPT-4, LLaMA), and RAG pipelines. I interned at C-DAC Hyderabad, where I architected AI-powered knowledge graphs, semantic search engines, and document analysis systems using cutting-edge technologies.

I believe in practical learning and hands-on experience. If it's smart, it's vulnerable to innovation! 🚀"""

WORK_EXPERIENCE = [
    {
        "company": "C-DAC Hyderabad",
        "position": "AI Engineering Intern",
        "duration": "June 2024 - August 2024",
        "details": [
            "🔧 Built AI-powered knowledge graphs using NetworkX and GPT-4",
            "🔍 Developed semantic search engine with LangChain and FAISS",
            "💬 Created document analysis chatbot using Streamlit and Ollama",
            "⚡ Optimized data processing pipelines reducing latency by 40%",
            "📊 Implemented data visualization dashboards with Plotly"
        ],
        "image": "work_experience_cdac.png"
    },
    {
        "company": "Oppo Mobiles India",
        "position": "QA Testing Intern",
        "duration": "Feb 2024 - Apr 2024",
        "details": [
            "🧪 Conducted automated and manual testing for mobile applications",
            "🐛 Identified and documented 50+ software bugs with detailed reports",
            "🤝 Collaborated with development teams for rapid issue resolution",
            "📈 Improved test coverage by 30% using pytest automation",
            "✅ Ensured quality standards across multiple product releases"
        ],
        "image": "work_experience_oppo.jpg"
    }
]

PROJECTS = [
    {
        "title": "Knowledge Graph Visualizer",
        "description": "Interactive knowledge graph visualization system with semantic search capabilities and AI-powered insights",
        "tech": ["Python", "NetworkX", "Streamlit", "Neo4j", "LangChain", "GPT-4"],
        "link": "#",
        "image": "knowledge_graph.png"
    },
    {
        "title": "DocuGenius - Document Chat",
        "description": "AI-powered document analysis and Q&A system using RAG pipelines with vector embeddings",
        "tech": ["Python", "LangChain", "GPT-4", "FAISS", "Streamlit", "Ollama"],
        "link": "#",
        "image": "docugenius.png"
    },
    {
        "title": "Student Analytics Dashboard",
        "description": "Real-time interactive analytics dashboard for student performance tracking and predictive insights",
        "tech": ["Python", "Plotly", "Pandas", "Streamlit", "SQLite3", "ML"],
        "link": "#",
        "image": "student_dashboard.png"
    },
    {
        "title": "APSPDCL Data Analysis",
        "description": "Power distribution data analysis and visualization system with anomaly detection",
        "tech": ["Python", "Pandas", "Matplotlib", "Tableau", "NumPy"],
        "link": "#",
        "image": "apspdcl.jpg"
    }
]

SKILLS = {
    "Programming Languages": ["Python", "JavaScript", "SQL", "C", "Go", "Bash"],
    "AI/ML & LLMs": ["GPT-4", "LangChain", "LLaMA2", "FAISS", "RAG", "Ollama", "Hugging Face"],
    "Data Science": ["Pandas", "NumPy", "Plotly", "Matplotlib", "Seaborn", "Scikit-learn"],
    "Tools & Frameworks": ["Streamlit", "Neo4j", "NetworkX", "VS Code", "Git", "Docker", "Jupyter"],
    "Databases": ["SQLite3", "PostgreSQL", "MongoDB", "Neo4j", "Vector DBs"],
    "Soft Skills": ["Problem Solving", "Communication", "Teamwork", "Leadership", "Research"]
}

EDUCATION = [
    {
        "institution": "KSRM College of Engineering",
        "degree": "B.Tech in Computer Science & Engineering",
        "year": "2023",
        "gpa": "8.2/10 CGPA",
        "highlights": ["Top 10% of graduating class", "Academic Excellence Award", "Published research paper"],
        "image": "education.jpg"
    }
]

CERTIFICATIONS = [
    {"name": "Google AI Essentials", "issuer": "Google", "date": "2024", "icon": "🎓"},
    {"name": "Python for Data Science", "issuer": "Coursera", "date": "2023", "icon": "🐍"},
    {"name": "Machine Learning Specialization", "issuer": "Stanford Online", "date": "2023", "icon": "🤖"},
    {"name": "LangChain for LLM Application Development", "issuer": "DeepLearning.AI", "date": "2024", "icon": "⛓️"}
]

def animated_background_plot(tab_key):
    """Create animated visualizations"""
    n = 500
    x = np.linspace(0, 10, n)
    noise = np.random.rand() * 2
    y = np.sin(x + noise) * np.cos(x * 0.5) * random.uniform(1.2, 2.5)
    
    colors = ["#00ff41", "#7877c6"]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines',
        line=dict(color=colors[0], width=3),
        fill='tonexty',
        fillcolor=f'rgba(0, 255, 65, 0.05)',
        opacity=0.3
    ))
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        template=None,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=150
    )
    
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

def main():
    """Main application"""
    load_custom_css()
    
    # Show animated background
    show_animated_background()
    
    # Show preloader
    if not st.session_state.preloader_done:
        show_preloader()
        st.session_state.preloader_done = True
    
    # Hero section
    st.markdown("""
    <div class="fade-in" style="text-align:center; padding:4rem 1.5rem 2rem;">
        <h1 class="glow-text glitch" data-text="SIVAMAHENDRANATH RAGIMANU" style="font-size:3.5rem; margin-bottom:0.5rem;">
            SIVAMAHENDRANATH RAGIMANU
        </h1>
        <div class="typewriter" style="font-size:1.3rem; margin-top:1.5rem; display:inline-block;">
            🚀 AI Engineer | ML Developer | Python Expert
        </div>
        <p style="font-size:1.1rem; opacity:0.8; margin-top:1.5rem; font-family:'Fira Code', monospace; color:#00ff41;">
            > If it's smart, it's vulnerable to innovation! 💡
        </p>
        <div class="animated-divider" style="margin-top:2.5rem;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "👤 ABOUT", 
        "💼 EXPERIENCE", 
        "🚀 PROJECTS", 
        "🎯 SKILLS", 
        "🎓 EDUCATION", 
        "📧 CONTACT"
    ])
    
    # About Tab
    with tab1:
        animated_background_plot("about")
        col1, col2 = st.columns([1, 1.5], gap="large")
        
        with col1:
            st.markdown('<div class="card-container float-animation">', unsafe_allow_html=True)
            profile_img = load_image(get_image_path("profile.jpeg"))
            st.image(profile_img, width=340)
            st.markdown("""
            <div style="text-align:center; margin-top:1.5rem;">
                <span class="skill-badge">🐍 Python Expert</span>
                <span class="skill-badge">🤖 AI Engineer</span>
                <span class="skill-badge">📊 Data Scientist</span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card-container fade-in">', unsafe_allow_html=True)
            st.markdown("### 👨‍💻 About Me")
            st.write(ABOUT)
            
            st.markdown("### 🔗 Connect With Me")
            col_links = st.columns(4, gap="small")
            with col_links[0]:
                st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-000000?style=for-the-badge&logo=github&logoColor=00ff41)](https://github.com)")
            with col_links[1]:
                st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=00ff41)](https://linkedin.com)")
            with col_links[2]:
                st.markdown("[![Email](https://img.shields.io/badge/Email-000000?style=for-the-badge&logo=gmail&logoColor=00ff41)](mailto:mahendraragimanu2@gmail.com)")
            with col_links[3]:
                st.markdown("[![Resume](https://img.shields.io/badge/Resume-000000?style=for-the-badge&logo=adobe&logoColor=00ff41)](https://example.com)")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Experience Tab
    with tab2:
        animated_background_plot("exp")
        st.markdown("### 💼 Professional Experience")
        
        for idx, exp in enumerate(WORK_EXPERIENCE):
            col1, col2 = st.columns([0.85, 1.15], gap="large")
            
            with col1:
                st.markdown('<div class="card-container fade-in">', unsafe_allow_html=True)
                exp_img = load_image(get_image_path(exp["image"]))
                st.image(exp_img, width=280)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="card-container fade-in-delay-1">', unsafe_allow_html=True)
                st.markdown(f"### {exp['company']}")
                st.markdown(f"**🎯 {exp['position']}**")
                st.markdown(f"**📅 {exp['duration']}**")
                st.markdown("#### Key Achievements:")
                for detail in exp['details']:
                    st.markdown(f"{detail}")
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
                st.image(proj_img, use_column_width=True)
                st.markdown(f"#### {project['title']}")
                st.write(project['description'])
                st.markdown("**⚡ Tech Stack:**")
                for tech in project['tech']:
                    st.markdown(f'<span class="skill-badge">{tech}</span>', unsafe_allow_html=True)
                st.markdown(f"<br><br>[🔗 View Project →]({project['link']})", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Skills Tab
    with tab4:
        animated_background_plot("skills")
        st.markdown("### 🎯 Technical Arsenal")
        
        for category, skills in SKILLS.items():
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
            st.image(edu_img, width=300)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            for edu in EDUCATION:
                st.markdown('<div class="card-container fade-in">', unsafe_allow_html=True)
                st.markdown(f"### {edu['institution']}")
                st.markdown(f"**🎓 {edu['degree']}**")
                st.markdown(f"**📅 {edu['year']} | 📊 GPA: {edu['gpa']}**")
                st.markdown("#### 🏆 Highlights:")
                for highlight in edu['highlights']:
                    st.markdown(f"✨ {highlight}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="animated-divider"></div>', unsafe_allow_html=True)
            
            st.markdown("#### 🏅 Certifications")
            cert_cols = st.columns(2, gap="medium")
            for idx, cert in enumerate(CERTIFICATIONS):
                with cert_cols[idx % 2]:
                    st.markdown('<div class="card-container fade-in-delay-1">', unsafe_allow_html=True)
                    st.markdown(f"{cert['icon']} **{cert['name']}**")
                    st.markdown(f"*{cert['issuer']} • {cert['date']}*")
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # Contact Tab
    with tab6:
        animated_background_plot("contact")
        st.markdown("### 📧 Let's Connect!")
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown("#### 📍 Contact Information")
            st.markdown("""
            **📍 Location:** Anantapur, Andhra Pradesh, India  
            **📧 Email:** [mahendraragimanu2@gmail.com](mailto:mahendraragimanu2@gmail.com)  
            **📱 Phone:** +91 8106442744  
            **🌐 Portfolio:** [https://example.com](https://example.com)
            """)
            
            st.markdown("#### 🌟 Quick Stats")
            stats_html = """
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px; margin-top:20px;">
                <div style="background:rgba(0,255,65,0.1); padding:15px; border-radius:10px; border:1px solid rgba(0,255,65,0.3); text-align:center;">
                    <div style="font-size:2rem; font-weight:bold; color:#00ff41;">10+</div>
                    <div style="font-size:0.9rem; opacity:0.8;">Projects</div>
                </div>
                <div style="background:rgba(120,119,198,0.1); padding:15px; border-radius:10px; border:1px solid rgba(120,119,198,0.3); text-align:center;">
                    <div style="font-size:2rem; font-weight:bold; color:#7877c6;">5+</div>
                    <div style="font-size:0.9rem; opacity:0.8;">Certifications</div>
                </div>
            </div>
            """
            st.markdown(stats_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="card-container">', unsafe_allow_html=True)
            st.markdown("#### ✉️ Send a Message")
            
            with st.form("contact_form", clear_on_submit=True):
                name = st.text_input("🔖 Your Name", placeholder="John Doe")
                email = st.text_input("📧 Your Email", placeholder="john@example.com")
                message = st.text_area("💬 Message", placeholder="Tell me about your project!", height=130)
                submit_button = st.form_submit_button("🚀 SEND MESSAGE", use_container_width=True)
                
                if submit_button:
                    if not rate_limit_check():
                        st.error("⚠️ Too many submissions.")
                    elif not name or not email or not message:
                        st.error("❌ Please fill all fields")
                    elif not is_valid_email(email):
                        st.error("❌ Invalid email")
                    elif len(message) < 10:
                        st.error("❌ Message too short")
                    else:
                        name = sanitize_input(name)
                        email = sanitize_input(email)
                        message = sanitize_input(message)
                        
                        if save_message_to_db(name, email, message):
                            st.session_state.form_submissions.append(time.time())
                            send_email_notification(name, email, message)
                            st.success("✅ Message sent successfully!", icon="🎉")
                        else:
                            st.error("❌ Failed to send.")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="animated-divider" style="margin-top:5rem;"></div>
    <div style="text-align:center; padding:3rem 1.5rem 2rem;">
        <p style="font-size:1.1rem; font-family:'Space Grotesk', sans-serif; font-weight:600;">
            © 2025 Sivamahendranath Ragimanu
        </p>
        <p style="font-size:0.95rem; opacity:0.7; font-family:'Fira Code', monospace;">
            Built with 💚 using Streamlit | Cyberpunk Design
        </p>
        <div class="fade-in" style="margin-top:2rem;">
            <span class="glow-text" style="font-size:1.3rem;">
                > Let's build the future with AI! 🚀
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
