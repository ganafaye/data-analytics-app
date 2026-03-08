import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import re
from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, StandardScaler
from scipy import stats
import base64
import warnings

warnings.filterwarnings('ignore')

# Pour le profiling (optionnel)
try:
    from ydata_profiling import ProfileReport
    import streamlit.components.v1 as components

    PROFILING_AVAILABLE = True
except ImportError:
    PROFILING_AVAILABLE = False

# Configuration de la page
st.set_page_config(
    page_title="Data Quality Analyzer | Analyse & Traitement",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS AMÉLIORÉ AVEC SIDEBAR BLANC STYLISÉE ---
# [Votre CSS existant ici, inchangé]
st.markdown("""
    <style>
    /* Import des polices */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Style général avec dégradé élégant */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #9f7aea 100%);
        background-size: 200% 200%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Inter', sans-serif;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* En-tête principal avec effet glassmorphisme */
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 2rem 2.5rem;
        border-radius: 30px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
        background-size: 300% 100%;
        animation: rainbow 6s ease infinite;
    }

    @keyframes rainbow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .main-header::after {
        content: '📊';
        position: absolute;
        bottom: -20px;
        right: -20px;
        font-size: 8rem;
        opacity: 0.05;
        transform: rotate(-15deg);
    }

    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ff6b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
        font-family: 'Plus Jakarta Sans', sans-serif;
        position: relative;
        z-index: 1;
    }

    .main-subtitle {
        color: #4a5568;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }

    /* Sidebar blanche stylisée */
    section[data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid rgba(102, 126, 234, 0.2);
        box-shadow: 5px 0 30px rgba(0, 0, 0, 0.03);
    }

    section[data-testid="stSidebar"] > div {
        background: white;
    }

    .sidebar-header {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 2rem 1.5rem;
        border-radius: 0 0 30px 30px;
        margin-bottom: 1.5rem;
        color: #2d3748;
        text-align: center;
        border-bottom: 1px solid rgba(102, 126, 234, 0.2);
        position: relative;
        overflow: hidden;
    }

    .sidebar-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #9f7aea);
    }

    .sidebar-header::after {
        content: '📊';
        position: absolute;
        bottom: -10px;
        right: -10px;
        font-size: 4rem;
        opacity: 0.1;
        transform: rotate(10deg);
    }

    .sidebar-header h3 {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Plus Jakarta Sans', sans-serif;
        position: relative;
        z-index: 1;
    }

    .sidebar-header p {
        opacity: 0.8;
        font-size: 0.95rem;
        margin: 0.5rem 0 0 0;
        color: #718096;
        position: relative;
        z-index: 1;
    }

    /* Style des widgets dans la sidebar */
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #2d3748;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #edf2f7;
    }

    section[data-testid="stSidebar"] .stFileUploader {
        border: 2px dashed #e2e8f0;
        border-radius: 15px;
        padding: 0.5rem;
        background: #f8fafc;
        transition: all 0.3s ease;
    }

    section[data-testid="stSidebar"] .stFileUploader:hover {
        border-color: #667eea;
        background: white;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
    }

    section[data-testid="stSidebar"] .stSelectbox > div > div {
        border-radius: 12px !important;
        border: 2px solid #edf2f7 !important;
        transition: all 0.3s ease;
    }

    section[data-testid="stSidebar"] .stSelectbox > div > div:hover {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    section[data-testid="stSidebar"] .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
    }

    section[data-testid="stSidebar"] .stCheckbox > div {
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }

    section[data-testid="stSidebar"] .stCheckbox > div:hover {
        transform: translateX(5px);
        background: #f7fafc;
    }

    /* Cartes de qualité avec design moderne */
    .quality-card {
        background: white;
        padding: 1.5rem;
        border-radius: 25px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05), 0 0 0 1px rgba(102, 126, 234, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }

    .quality-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        transition: width 0.3s ease;
    }

    .quality-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.15), 0 0 0 1px #667eea;
    }

    .quality-card:hover::before {
        width: 6px;
    }

    .quality-score {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
        filter: drop-shadow(0 5px 10px rgba(102, 126, 234, 0.2));
    }

    .quality-label {
        color: #718096;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
    }

    /* Badges de qualité avec design premium */
    .quality-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-right: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }

    .badge-excellent {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
    }

    .badge-good {
        background: linear-gradient(135deg, #667eea 0%, #5a67d8 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }

    .badge-fair {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(237, 137, 54, 0.3);
    }

    .badge-poor {
        background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
        color: white;
        box-shadow: 0 4px 15px rgba(229, 62, 62, 0.3);
    }

    /* Badges pour types de variables */
    .badge-quantitative {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 30px;
        font-size: 0.7rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(72, 187, 120, 0.2);
    }

    .badge-qualitative {
        background: linear-gradient(135deg, #667eea 0%, #5a67d8 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 30px;
        font-size: 0.7rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }

    .badge-date {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 30px;
        font-size: 0.7rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(237, 137, 54, 0.2);
    }

    .badge-target {
        background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 30px;
        font-size: 0.7rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(229, 62, 62, 0.2);
    }

    /* Cartes métriques */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.03), 0 0 0 1px rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        height: 100%;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .metric-card::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.05) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.1), 0 0 0 1px #667eea;
    }

    .metric-card:hover::after {
        opacity: 1;
    }

    .metric-value-sm {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }

    .metric-label-sm {
        color: #718096;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
        font-weight: 600;
    }

    /* Timeline avec design moderne */
    .timeline-item {
        display: flex;
        align-items: center;
        padding: 1.2rem;
        background: #f8fafc;
        border-radius: 16px;
        margin-bottom: 0.8rem;
        border-left: 5px solid #667eea;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    }

    .timeline-item:hover {
        transform: translateX(8px);
        background: white;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.1);
    }

    .timeline-icon {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1.2rem;
        font-size: 1.3rem;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        flex-shrink: 0;
    }

    /* Progress bars */
    .progress-container {
        background: #edf2f7;
        height: 8px;
        border-radius: 20px;
        overflow: hidden;
        margin: 0.5rem 0;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2, #9f7aea);
        background-size: 200% 200%;
        animation: gradientMove 3s ease infinite;
        border-radius: 20px;
        transition: width 0.3s ease;
    }

    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Variables grid */
    .variable-item {
        background: white;
        padding: 1rem;
        border-radius: 14px;
        border: 1px solid #edf2f7;
        display: flex;
        flex-direction: column;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
        position: relative;
        overflow: hidden;
    }

    .variable-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        opacity: 0;
        transition: opacity 0.3s ease;
    }

    .variable-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.1);
        border-color: #667eea;
    }

    .variable-item:hover::before {
        opacity: 1;
    }

    .variable-name {
        font-weight: 600;
        color: #2d3748;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .variable-stats {
        font-size: 0.8rem;
        color: #718096;
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }

    /* Tabs avec design premium */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.8rem;
        background: white;
        padding: 0.8rem;
        border-radius: 60px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin-bottom: 2rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.02);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 40px;
        padding: 0.7rem 1.8rem;
        font-weight: 500;
        color: #4a5568;
        transition: all 0.3s ease;
        border: 1px solid transparent;
        font-size: 0.95rem;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.05);
        border-color: rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
        border: none;
    }

    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 0.7rem 2rem;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
        width: 100%;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }

    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.3);
    }

    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        box-shadow: 0 8px 16px rgba(72, 187, 120, 0.2);
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 40px 40px 0 0;
        margin-top: 3rem;
        color: #4a5568;
        font-size: 0.95rem;
        border-top: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 -10px 30px rgba(0, 0, 0, 0.05);
        position: relative;
        overflow: hidden;
    }

    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #9f7aea);
    }

    /* Animations */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    .floating {
        animation: float 4s ease-in-out infinite;
    }

    /* Info boxes */
    .info-box {
        background: #f8fafc;
        padding: 1.2rem;
        border-radius: 16px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
    }

    .info-box:hover {
        background: white;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.1);
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 16px !important;
        border: 1px solid #edf2f7 !important;
        padding: 1rem 1.5rem !important;
        font-weight: 600 !important;
        color: #2d3748 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02) !important;
    }

    .streamlit-expanderHeader:hover {
        border-color: #667eea !important;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.1) !important;
        transform: translateX(5px);
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 16px !important;
        border: 1px solid #edf2f7 !important;
        overflow: hidden !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.02) !important;
    }

    /* Messages */
    .stAlert {
        border-radius: 16px !important;
        border: none !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05) !important;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.2rem;
        }

        .main-subtitle {
            font-size: 1rem;
        }

        .metric-value-sm {
            font-size: 1.5rem;
        }

        .quality-score {
            font-size: 2.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
        }
    }

    @media (max-width: 480px) {
        .main-header {
            padding: 1.5rem;
        }

        .main-title {
            font-size: 1.8rem;
        }

        .sidebar-header {
            padding: 1.5rem 1rem;
        }

        .sidebar-header h3 {
            font-size: 1.5rem;
        }
    }

    /* Effet de brillance */
    .shine {
        position: relative;
        overflow: hidden;
    }

    .shine::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -60%;
        width: 20%;
        height: 200%;
        background: rgba(255, 255, 255, 0.2);
        transform: rotate(25deg);
        animation: shine 8s ease-in-out infinite;
        pointer-events: none;
    }

    @keyframes shine {
        0% { left: -60%; }
        20% { left: 120%; }
        100% { left: 120%; }
    }

    /* Tooltips personnalisés */
    .custom-tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 2px dotted #667eea;
        cursor: help;
    }

    .custom-tooltip .tooltip-text {
        visibility: hidden;
        width: 200px;
        background: #2d3748;
        color: white;
        text-align: center;
        border-radius: 10px;
        padding: 0.5rem;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.8rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    .custom-tooltip:hover .tooltip-text {
        visibility: visible;
        opacity: 1;
    }
/* 1. On garde le header mais on le rend invisible (transparent) */
    header[data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        color: transparent !important;
    }

    /* 2. On masque spécifiquement les boutons de droite (Deploy, Menu, etc.) */
    header[data-testid="stHeader"] div:first-child > div:nth-child(2) {
        display: none !important;
    }

    /* 3. On s'assure que le bouton de la sidebar reste visible et blanc/couleur voulue */
    button[data-testid="stBaseButton-headerNoPadding"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important; /* Change en 'black' si ton fond est clair */
    }

    /* 4. On réduit la marge pour que le contenu remonte */
    .main .block-container {
        padding-top: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* 1. Cibler le bouton de la Sidebar (Ouverture/Fermeture) */
    button[data-testid="stBaseButton-headerNoPadding"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        width: 45px !important;
        height: 45px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        margin-left: 10px !important;
        margin-top: 5px !important;
    }

    /* 2. Effet au survol (Hover) */
    button[data-testid="stBaseButton-headerNoPadding"]:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid #60a5fa !important; /* Bordure bleue comme ton titre */
        transform: scale(1.1) rotate(5deg) !important;
        box-shadow: 0 0 20px rgba(96, 165, 250, 0.4) !important;
    }

    /* 3. Style de l'icône à l'intérieur du bouton */
    button[data-testid="stBaseButton-headerNoPadding"] svg {
        fill: white !important;
        width: 24px !important;
        height: 24px !important;
    }

    /* 4. Ajustement pour que l'icône reste visible même si le header est transparent */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Optionnel : Animation d'apparition douce */
    @keyframes fadeInIcon {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    button[data-testid="stBaseButton-headerNoPadding"] {
        animation: fadeInIcon 0.8s ease-out;
    }
    </style>
""", unsafe_allow_html=True)


# ============================================================
# NOUVELLES FONCTIONS IMPLÉMENTÉES
# ============================================================

# --- FONCTIONS DE TRAITEMENT AUTOMATISÉ (DATA CLEANING) ---

def nettoyer_noms_colonnes(df):
    """
    Standardise les noms de colonnes :
    - minuscules
    - underscores au lieu d'espaces
    - supprime caractères spéciaux
    """
    df_clean = df.copy()
    nouveau_noms = {}
    for col in df_clean.columns:
        # Conversion en minuscules
        new_col = col.lower().strip()
        # Remplacer espaces et caractères spéciaux par underscores
        new_col = re.sub(r'[^a-z0-9]', '_', new_col)
        # Supprimer les underscores multiples
        new_col = re.sub(r'_+', '_', new_col)
        # Supprimer les underscores en début/fin
        new_col = new_col.strip('_')
        nouveau_noms[col] = new_col

    df_clean.rename(columns=nouveau_noms, inplace=True)
    return df_clean, nouveau_noms


def imputer_valeurs_manquantes(df, colonnes, methode='moyenne'):
    """
    Impute les valeurs manquantes selon la méthode choisie
    """
    df_imp = df.copy()
    stats = {}

    for col in colonnes:
        if col in df_imp.columns:
            if methode == 'moyenne' and pd.api.types.is_numeric_dtype(df_imp[col]):
                valeur = df_imp[col].mean()
                stats[col] = {'methode': 'moyenne', 'valeur': valeur}
                df_imp[col].fillna(valeur, inplace=True)
            elif methode == 'mediane' and pd.api.types.is_numeric_dtype(df_imp[col]):
                valeur = df_imp[col].median()
                stats[col] = {'methode': 'médiane', 'valeur': valeur}
                df_imp[col].fillna(valeur, inplace=True)
            elif methode == 'mode':
                valeur = df_imp[col].mode()[0] if not df_imp[col].mode().empty else None
                if valeur is not None:
                    stats[col] = {'methode': 'mode', 'valeur': valeur}
                    df_imp[col].fillna(valeur, inplace=True)

    return df_imp, stats


def encoder_variables(df, colonnes, methode='label'):
    """
    Encode les variables qualitatives
    """
    df_enc = df.copy()
    encoders = {}

    for col in colonnes:
        if col in df_enc.columns:
            if methode == 'label':
                le = LabelEncoder()
                df_enc[col + '_encoded'] = le.fit_transform(df_enc[col].astype(str))
                encoders[col] = le
            elif methode == 'onehot':
                dummies = pd.get_dummies(df_enc[col], prefix=col, drop_first=True)
                df_enc = pd.concat([df_enc, dummies], axis=1)
                df_enc.drop(col, axis=1, inplace=True)

    return df_enc, encoders


def detecter_outliers_multivaries(df, contamination=0.1):
    """
    Détection d'outliers multivariés avec Isolation Forest
    """
    df_num = df.select_dtypes(include=[np.number])

    if len(df_num.columns) < 2:
        return pd.Series([False] * len(df))

    iso_forest = IsolationForest(contamination=contamination, random_state=42)
    outliers = iso_forest.fit_predict(df_num.fillna(df_num.mean()))

    return pd.Series(outliers == -1, index=df.index)


def standardiser_donnees(df, colonnes):
    """
    Standardisation (Z-score) des variables numériques
    """
    df_std = df.copy()
    scaler = StandardScaler()

    if colonnes:
        df_std[colonnes] = scaler.fit_transform(df_std[colonnes])

    return df_std, scaler


# --- FONCTIONS D'ANALYSE STATISTIQUE AVANCÉE ---

def matrice_correlation(df, seuil=0.8):
    """
    Calcule et retourne la matrice de corrélation avec identification des fortes corrélations
    """
    df_num = df.select_dtypes(include=[np.number])

    if len(df_num.columns) < 2:
        return None, []

    corr_matrix = df_num.corr()

    # Identifier les paires fortement corrélées
    high_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) > seuil:
                high_corr.append({
                    'col1': corr_matrix.columns[i],
                    'col2': corr_matrix.columns[j],
                    'correlation': corr_matrix.iloc[i, j]
                })

    return corr_matrix, high_corr


def test_normalite(df, colonnes, alpha=0.05):
    """
    Test de Shapiro-Wilk pour la normalité
    """
    results = []

    for col in colonnes:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            # Échantillonner si trop grand (Shapiro-Wilk max 5000)
            data = df[col].dropna()
            if len(data) > 5000:
                data = data.sample(5000, random_state=42)

            if len(data) >= 3:
                statistic, p_value = stats.shapiro(data)
                normal = p_value > alpha
                results.append({
                    'colonne': col,
                    'statistique': statistic,
                    'p_value': p_value,
                    'normal': normal,
                    'interpretation': 'Normale' if normal else 'Non normale'
                })

    return results


def profil_donnees_rapide(df):
    """
    Génère un profil rapide des données
    """
    profil = {
        'lignes': len(df),
        'colonnes': len(df.columns),
        'memoire': df.memory_usage(deep=True).sum() / 1024 ** 2,
        'types': df.dtypes.value_counts().to_dict(),
        'colonnes_manquantes': df.isnull().any().sum(),
        'total_manquantes': df.isnull().sum().sum(),
        'colonnes_constantes': sum(df.nunique() == 1),
        'colonnes_uniques': sum(df.nunique() == len(df))
    }

    return profil


# --- FONCTIONS DE REPORTING ---

def generer_rapport_html(analyse, historique=None):
    """
    Génère un rapport HTML complet
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rapport Data Quality - {analyse['nom']}</title>
        <style>
            body {{ font-family: 'Arial', sans-serif; margin: 40px; background: #f8fafc; }}
            .header {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 30px; border-radius: 15px; margin-bottom: 30px; }}
            .section {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
            .score {{ font-size: 3rem; font-weight: bold; }}
            .badge {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; }}
            .badge-excellent {{ background: #48bb78; color: white; }}
            .badge-good {{ background: #667eea; color: white; }}
            .badge-fair {{ background: #ed8936; color: white; }}
            .badge-poor {{ background: #e53e3e; color: white; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
            th {{ background: #f7fafc; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Rapport d'analyse - {analyse['nom']}</h1>
            <p>Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
        </div>

        <div class="section">
            <h2>📈 Score de qualité</h2>
            <div class="score">{analyse['quality_score']:.1f}/100</div>
            <span class="badge badge-{analyse['quality_badge'].replace('badge-', '')}">{analyse['quality_category']}</span>
        </div>

        <div class="section">
            <h2>📊 Informations générales</h2>
            <table>
                <tr><td>Lignes</td><td>{analyse['total_lignes']:,}</td></tr>
                <tr><td>Colonnes</td><td>{analyse['total_colonnes']}</td></tr>
                <tr><td>Mémoire</td><td>{analyse['memoire']:.2f} MB</td></tr>
                <tr><td>Valeurs manquantes</td><td>{analyse['total_missing']} ({analyse['pct_missing']:.1f}%)</td></tr>
                <tr><td>Doublons</td><td>{analyse['duplicates']} ({analyse['pct_duplicates']:.1f}%)</td></tr>
            </table>
        </div>

        <div class="section">
            <h2>⚠️ Problèmes détectés</h2>
            <table>
                <tr>
                    <th>Colonne</th>
                    <th>Problèmes</th>
                </tr>
    """

    for prob in analyse['problem_columns'][:10]:
        html += f"""
                <tr>
                    <td><strong>{prob['colonne']}</strong></td>
                    <td>{', '.join(prob['issues'])}</td>
                </tr>
        """

    html += """
            </table>
        </div>
    """

    if historique:
        html += """
        <div class="section">
            <h2>📜 Historique des traitements</h2>
            <table>
                <tr>
                    <th>Étape</th>
                    <th>Score avant</th>
                    <th>Score après</th>
                    <th>Amélioration</th>
                </tr>
        """

        for i, h in enumerate(historique):
            html += f"""
                <tr>
                    <td>{h.get('etape', f'Étape {i + 1}')}</td>
                    <td>{h.get('score_avant', 0):.1f}</td>
                    <td>{h.get('score_apres', 0):.1f}</td>
                    <td>+{h.get('amelioration', 0):.1f}</td>
                </tr>
            """

        html += "</table></div>"

    html += """
        <div class="section">
            <p style="text-align: center; color: #718096;">
                Rapport généré automatiquement par Data Quality Analyzer<br>
                © 2026 - Tous droits réservés
            </p>
        </div>
    </body>
    </html>
    """

    return html


# --- FONCTIONS D'INTERFACE AVANCÉE ---

def split_view_comparaison(df_avant, df_apres, changes):
    """
    Affiche une vue comparative avec mise en évidence des changements
    """
    st.markdown("### 🔍 Vue comparative (Avant vs Après)")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📋 Dataset AVANT**")
        st.dataframe(df_avant.head(20), use_container_width=True)

    with col2:
        st.markdown("**✨ Dataset APRÈS**")
        st.dataframe(df_apres.head(20), use_container_width=True)

    if changes:
        st.markdown("**📝 Modifications effectuées :**")
        for change in changes:
            st.success(f"✅ {change}")


def afficher_filtres_variables(analyse):
    """
    Affiche des filtres pour les variables problématiques
    """
    st.markdown("### 🔍 Filtres rapides")

    col1, col2, col3 = st.columns(3)

    with col1:
        seuil_missing = st.slider("Seuil valeurs manquantes (%)", 0, 100, 10)

    with col2:
        show_outliers = st.checkbox("Afficher uniquement les colonnes avec outliers")

    with col3:
        show_constantes = st.checkbox("Afficher les colonnes constantes")

    # Filtrer les colonnes
    filtered_cols = []
    for col in analyse['col_stats']:
        include = True

        if col['pct_nulles'] < seuil_missing:
            include = False

        if show_outliers and 'outliers' in col and col['pct_outliers'] == 0:
            include = False

        if show_constantes and col['uniques'] > 1:
            include = False

        if include:
            filtered_cols.append(col)

    return filtered_cols


# --- FONCTIONS EXISTANTES (conservées) ---
def detecter_type_fichier(nom_fichier):
    ext = nom_fichier.split('.')[-1].lower() if '.' in nom_fichier else ''
    types = {
        'csv': 'CSV',
        'xlsx': 'Excel',
        'xls': 'Excel',
        'json': 'JSON',
        'parquet': 'Parquet',
        'pkl': 'Pickle',
        'txt': 'Texte'
    }
    return types.get(ext, 'Inconnu')


def charger_fichier(uploaded_file):
    ext = uploaded_file.name.split('.')[-1].lower()
    try:
        if ext == 'csv':
            df = pd.read_csv(uploaded_file)
        elif ext in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        elif ext == 'json':
            df = pd.read_json(uploaded_file)
        elif ext == 'parquet':
            df = pd.read_parquet(uploaded_file)
        elif ext == 'pkl':
            df = pd.read_pickle(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file, sep=None, engine='python')
        return df, None
    except Exception as e:
        return None, str(e)


def classifier_variables(df):
    quantitative = []
    qualitative = []
    dates = []
    target_potential = []
    a_convertir = []

    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            dates.append(col)
            continue

        if any(keyword in col.lower() for keyword in ['date', 'time', 'annee', 'year', 'month', 'jour', 'day']):
            try:
                pd.to_datetime(df[col], errors='raise')
                a_convertir.append({
                    'colonne': col,
                    'type_actuel': str(df[col].dtype),
                    'type_suggere': 'datetime',
                    'raison': 'Nom suggère une date'
                })
                dates.append(col)
                continue
            except:
                pass

        if pd.api.types.is_numeric_dtype(df[col]):
            n_unique = df[col].nunique()
            if n_unique < 10:
                quantitative.append(col)
                a_convertir.append({
                    'colonne': col,
                    'type_actuel': str(df[col].dtype),
                    'type_suggere': 'catégoriel',
                    'raison': f'{n_unique} valeurs uniques'
                })
            else:
                quantitative.append(col)

            if n_unique == 2:
                target_potential.append({
                    'colonne': col,
                    'type': 'binaire',
                    'raison': 'Classification binaire'
                })
            elif 2 < n_unique < 20:
                target_potential.append({
                    'colonne': col,
                    'type': 'multiclasse',
                    'raison': f'{n_unique} classes'
                })
        else:
            qualitative.append(col)
            n_unique = df[col].nunique()
            if n_unique == 2:
                target_potential.append({
                    'colonne': col,
                    'type': 'binaire',
                    'raison': 'Classification binaire'
                })
            elif 2 < n_unique < 20:
                target_potential.append({
                    'colonne': col,
                    'type': 'multiclasse',
                    'raison': f'{n_unique} classes'
                })

    return {
        'quantitative': quantitative,
        'qualitative': qualitative,
        'dates': dates,
        'target_potential': target_potential,
        'a_convertir': a_convertir
    }


def analyser_qualite_dataset(df, nom_dataset="Dataset"):
    classification = classifier_variables(df)

    total_lignes = len(df)
    total_colonnes = len(df.columns)
    memoire = df.memory_usage(deep=True).sum() / 1024 ** 2

    dtypes_summary = df.dtypes.astype(str).value_counts()

    col_stats = []
    for col in df.columns:
        stats = {
            'nom': col,
            'type': str(df[col].dtype),
            'classification': 'quantitative' if col in classification['quantitative'] else 'qualitative' if col in
                                                                                                            classification[
                                                                                                                'qualitative'] else 'date',
            'non_nulles': df[col].count(),
            'nulles': df[col].isnull().sum(),
            'pct_nulles': (df[col].isnull().sum() / total_lignes) * 100 if total_lignes > 0 else 0,
            'uniques': df[col].nunique(),
            'pct_uniques': (df[col].nunique() / total_lignes) * 100 if total_lignes > 0 else 0
        }

        if col in classification['quantitative']:
            stats['min'] = df[col].min() if not df[col].isnull().all() else None
            stats['max'] = df[col].max() if not df[col].isnull().all() else None
            stats['mean'] = df[col].mean() if not df[col].isnull().all() else None
            stats['std'] = df[col].std() if not df[col].isnull().all() else None
            stats['skew'] = df[col].skew() if not df[col].isnull().all() else None

            if not df[col].isnull().all():
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
                stats['outliers'] = outliers
                stats['pct_outliers'] = (outliers / total_lignes) * 100 if total_lignes > 0 else 0

        col_stats.append(stats)

    missing_values = df.isnull().sum()
    missing_cols = missing_values[missing_values > 0]
    total_missing = missing_values.sum()
    pct_missing = (total_missing / (total_lignes * total_colonnes)) * 100 if (total_lignes * total_colonnes) > 0 else 0

    duplicates = df.duplicated().sum()
    pct_duplicates = (duplicates / total_lignes) * 100 if total_lignes > 0 else 0

    problem_columns = []
    for stats in col_stats:
        issues = []

        if ' ' in stats['nom'] or any(c in stats['nom'] for c in '!@#$%^&*()+='):
            issues.append("Nom non standard")
        if stats['uniques'] == 1:
            issues.append("Constante")
        if stats['uniques'] == total_lignes:
            issues.append("Potentiel ID")
        if stats['pct_nulles'] > 30:
            issues.append(f"{stats['pct_nulles']:.1f}% manquantes")
        if stats['uniques'] > 0 and stats['uniques'] < total_lignes:  # Éviter division par zéro
            # Vérification des types mixtes (simplifiée)
            pass
        if 'outliers' in stats and stats['pct_outliers'] > 5:
            issues.append(f"{stats['pct_outliers']:.1f}% outliers")
        if 'skew' in stats and stats['skew'] is not None and abs(stats['skew']) > 1:
            issues.append(f"Asymétrie ({stats['skew']:.2f})")

        if issues:
            problem_columns.append({
                'colonne': stats['nom'],
                'issues': issues,
                'severity': len(issues)
            })

    quality_score = 100
    quality_score -= pct_missing * 1.5
    quality_score -= pct_duplicates * 2
    quality_score -= len(problem_columns) * 2
    quality_score -= sum(p['severity'] for p in problem_columns)
    quality_score = max(0, min(100, quality_score))

    if quality_score >= 90:
        quality_category = "EXCELLENT"
        quality_color = "#48bb78"
        quality_badge = "badge-excellent"
    elif quality_score >= 75:
        quality_category = "BON"
        quality_color = "#667eea"
        quality_badge = "badge-good"
    elif quality_score >= 50:
        quality_category = "MOYEN"
        quality_color = "#ed8936"
        quality_badge = "badge-fair"
    else:
        quality_category = "FAIBLE"
        quality_color = "#e53e3e"
        quality_badge = "badge-poor"

    return {
        'nom': nom_dataset,
        'total_lignes': total_lignes,
        'total_colonnes': total_colonnes,
        'memoire': memoire,
        'classification': classification,
        'dtypes_summary': dtypes_summary,
        'col_stats': col_stats,
        'missing_cols': missing_cols.to_dict() if len(missing_cols) > 0 else {},
        'total_missing': total_missing,
        'pct_missing': pct_missing,
        'duplicates': duplicates,
        'pct_duplicates': pct_duplicates,
        'problem_columns': problem_columns,
        'quality_score': quality_score,
        'quality_category': quality_category,
        'quality_color': quality_color,
        'quality_badge': quality_badge
    }


def comparer_datasets(avant, apres):
    comparaison = {
        'amelioration_score': apres['quality_score'] - avant['quality_score'],
        'amelioration_score_pct': ((apres['quality_score'] - avant['quality_score']) / avant['quality_score']) * 100 if
        avant['quality_score'] > 0 else 0,
        'reduction_lignes': avant['total_lignes'] - apres['total_lignes'],
        'pct_reduction_lignes': ((avant['total_lignes'] - apres['total_lignes']) / avant['total_lignes']) * 100 if
        avant['total_lignes'] > 0 else 0,
        'reduction_colonnes': avant['total_colonnes'] - apres['total_colonnes'],
        'reduction_missing': avant['total_missing'] - apres['total_missing'],
        'pct_reduction_missing': ((avant['total_missing'] - apres['total_missing']) / avant['total_missing']) * 100 if
        avant['total_missing'] > 0 else 0,
        'reduction_duplicates': avant['duplicates'] - apres['duplicates'],
        'resolution_problemes': len(avant['problem_columns']) - len(apres['problem_columns']),
        'colonnes_ajoutees': max(0, apres['total_colonnes'] - avant['total_colonnes']),
        'colonnes_supprimees': max(0, avant['total_colonnes'] - apres['total_colonnes']),
        'avant': avant,
        'apres': apres
    }
    return comparaison


def creer_dashboard_qualite(analyse):
    """
    Crée un dashboard complet de qualité des données
    """
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Distribution des types', 'Top valeurs manquantes',
                        'Distribution du score', 'Top problèmes'),
        specs=[[{'type': 'pie'}, {'type': 'bar'}],
               [{'type': 'histogram'}, {'type': 'bar'}]]
    )

    # Graphique 1: Distribution des types
    types_counts = pd.Series([c['classification'] for c in analyse['col_stats']]).value_counts()
    fig.add_trace(
        go.Pie(labels=types_counts.index, values=types_counts.values,
               marker=dict(colors=['#48bb78', '#667eea', '#ed8936'])),
        row=1, col=1
    )

    # Graphique 2: Top colonnes avec valeurs manquantes
    missing_data = [(c['nom'], c['pct_nulles']) for c in analyse['col_stats'] if c['pct_nulles'] > 0]
    missing_data = sorted(missing_data, key=lambda x: x[1], reverse=True)[:10]
    if missing_data:
        cols, pcts = zip(*missing_data)
        fig.add_trace(
            go.Bar(x=pcts, y=cols, orientation='h',
                   marker=dict(color='#ed8936')),
            row=1, col=2
        )

    # Graphique 3: Distribution du score de qualité (simulée avec des valeurs)
    scores = [analyse['quality_score']] * 10  # Simuler une distribution
    fig.add_trace(
        go.Histogram(x=scores, nbinsx=10,
                     marker=dict(color='#667eea')),
        row=2, col=1
    )

    # Graphique 4: Top problèmes
    problem_cols = analyse['problem_columns'][:10]
    if problem_cols:
        cols = [p['colonne'] for p in problem_cols]
        severities = [p['severity'] for p in problem_cols]
        fig.add_trace(
            go.Bar(x=cols, y=severities,
                   marker=dict(color='#e53e3e')),
            row=2, col=2
        )

    fig.update_layout(height=800, showlegend=False,
                      title_text="Dashboard Qualité des Données")
    return fig


def creer_comparaison_radar(avant, apres):
    """
    Graphique radar pour comparer avant/après
    """
    categories = ['Score Qualité', 'Complétude', 'Unicité', 'Problèmes résolus']

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[avant['quality_score'], 100 - avant['pct_missing'],
           100 - avant['pct_duplicates'], 100 - len(avant['problem_columns'])],
        theta=categories,
        fill='toself',
        name='Avant traitement',
        line=dict(color='#e53e3e')
    ))

    fig.add_trace(go.Scatterpolar(
        r=[apres['quality_score'], 100 - apres['pct_missing'],
           100 - apres['pct_duplicates'], 100 - len(apres['problem_columns'])],
        theta=categories,
        fill='toself',
        name='Après traitement',
        line=dict(color='#48bb78')
    ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=True,
        title="Comparaison Avant/Après (Radar)",
        height=500
    )
    return fig


def suggerer_traitements(analyse):
    """
    Génère des suggestions de traitement basées sur l'analyse
    """
    suggestions = []

    # Suggestions pour les valeurs manquantes
    cols_manquantes = [c for c in analyse['col_stats'] if c['pct_nulles'] > 0]
    if cols_manquantes:
        for col in cols_manquantes[:5]:
            if col['pct_nulles'] < 5:
                suggestions.append({
                    'type': 'info',
                    'message': f"Colonne '{col['nom']}': {col['pct_nulles']:.1f}% valeurs manquantes - Supprimer les lignes",
                    'action': 'dropna',
                    'colonne': col['nom']
                })
            elif col['pct_nulles'] < 30:
                suggestions.append({
                    'type': 'warning',
                    'message': f"Colonne '{col['nom']}': {col['pct_nulles']:.1f}% valeurs manquantes - Imputer par la moyenne/médiane",
                    'action': 'impute',
                    'colonne': col['nom']
                })
            else:
                suggestions.append({
                    'type': 'danger',
                    'message': f"Colonne '{col['nom']}': {col['pct_nulles']:.1f}% valeurs manquantes - Supprimer la colonne",
                    'action': 'dropcol',
                    'colonne': col['nom']
                })

    # Suggestions pour les outliers
    for col in analyse['col_stats']:
        if 'outliers' in col and col['pct_outliers'] > 5:
            suggestions.append({
                'type': 'warning',
                'message': f"Colonne '{col['nom']}': {col['pct_outliers']:.1f}% outliers - Considérer winsorisation",
                'action': 'winsorize',
                'colonne': col['nom']
            })

    # Suggestions pour les doublons
    if analyse['pct_duplicates'] > 5:
        suggestions.append({
            'type': 'warning',
            'message': f"{analyse['pct_duplicates']:.1f}% de doublons - Supprimer les doublons",
            'action': 'drop_duplicates'
        })

    # Suggestions pour les colonnes problématiques
    for prob in analyse['problem_columns']:
        if 'Constante' in str(prob['issues']):
            suggestions.append({
                'type': 'danger',
                'message': f"Colonne '{prob['colonne']}' constante - Supprimer",
                'action': 'dropcol',
                'colonne': prob['colonne']
            })
        if 'Potentiel ID' in str(prob['issues']):
            suggestions.append({
                'type': 'info',
                'message': f"Colonne '{prob['colonne']}' potentiel ID - Peut être ignorée",
                'action': 'keep',
                'colonne': prob['colonne']
            })

    return suggestions


# ============================================================
# INTERFACE PRINCIPALE
# ============================================================

# --- EN-TÊTE ---
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🔬 Data Quality Analyzer Pro</h1>
    <p class="main-subtitle">Analyse intelligente, nettoyage automatisé et reporting avancé</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR AMÉLIORÉE ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h3>📊 Data Quality Pro</h3>
        <p>Analyse et traitement intelligent</p>
    </div>
    """, unsafe_allow_html=True)

    # Onglets dans la sidebar
    tab_upload, tab_clean, tab_advanced, tab_report = st.tabs([
        "📁 Chargement", "🧹 Nettoyage", "⚙️ Avancé", "📄 Rapport"
    ])

    with tab_upload:
        st.markdown("### 📂 Charger un fichier")
        uploaded_file = st.file_uploader(
            "Sélectionnez un fichier",
            type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'pkl'],
            key="main_uploader"
        )

        if uploaded_file:
            st.success(f"✅ Fichier chargé : {uploaded_file.name}")
            st.info(f"📁 Type : {detecter_type_fichier(uploaded_file.name)}")

    with tab_clean:
        st.markdown("### 🧹 Options de nettoyage")

        clean_names = st.checkbox("🏷️ Standardiser les noms de colonnes", value=True)

        st.markdown("**Valeurs manquantes**")
        missing_strategy = st.radio(
            "Stratégie",
            ["Aucun traitement", "Supprimer lignes", "Imputer moyenne", "Imputer médiane", "Imputer mode"],
            key="missing_strategy"
        )

        st.markdown("**Doublons**")
        remove_duplicates = st.checkbox("Supprimer les doublons", value=False)

        st.markdown("**Encodage**")
        encoding_strategy = st.radio(
            "Encoder les variables qualitatives",
            ["Aucun", "Label Encoding", "One-Hot Encoding"],
            key="encoding_strategy"
        )

        st.markdown("**Outliers**")
        remove_outliers = st.checkbox("Détecter outliers multivariés", value=False)
        outlier_contamination = st.slider("Contamination", 0.01, 0.3, 0.1, 0.01) if remove_outliers else 0.1

        standardize = st.checkbox("Standardiser les variables numériques", value=False)

    with tab_advanced:
        st.markdown("### ⚙️ Analyse avancée")

        show_correlation = st.checkbox("📈 Matrice de corrélation", value=True)
        corr_threshold = st.slider("Seuil corrélation", 0.5, 0.95, 0.8, 0.05) if show_correlation else 0.8

        show_normality = st.checkbox("📊 Test de normalité", value=False)

        show_profiling = st.checkbox("📋 Profilage rapide", value=True)

        if PROFILING_AVAILABLE:
            show_full_profiling = st.checkbox("📑 Profilage complet (ydata)", value=False)
        else:
            show_full_profiling = False
            st.caption("💡 Installer ydata-profiling pour plus d'options")

        filters = st.checkbox("🔍 Activer filtres variables", value=False)

    with tab_report:
        st.markdown("### 📄 Options de rapport")

        report_format = st.radio("Format", ["Texte", "HTML", "Les deux"], key="report_format")

        include_history = st.checkbox("Inclure historique", value=True)

        st.markdown("### 📜 Historique des traitements")

        if 'history' not in st.session_state:
            st.session_state.history = []

        if st.button("🗑️ Effacer historique"):
            st.session_state.history = []
            st.success("Historique effacé")

        st.caption(f"📊 Étapes: {len(st.session_state.history)}")

# --- INITIALISATION SESSION STATE ---
if 'df_original' not in st.session_state:
    st.session_state.df_original = None
if 'df_processed' not in st.session_state:
    st.session_state.df_processed = None
if 'analyse_original' not in st.session_state:
    st.session_state.analyse_original = None
if 'changes_log' not in st.session_state:
    st.session_state.changes_log = []

# --- TRAITEMENT PRINCIPAL ---
if uploaded_file is not None:
    # Chargement du fichier
    df, error = charger_fichier(uploaded_file)

    if df is not None:
        # Initialiser si c'est la première fois
        if st.session_state.df_original is None:
            st.session_state.df_original = df.copy()
            st.session_state.df_processed = df.copy()
            st.session_state.analyse_original = analyser_qualite_dataset(df, "Dataset original")

        # --- APPLICATION DES TRAITEMENTS ---
        changes = []
        df_current = st.session_state.df_processed.copy()

        # 1. Standardisation des noms de colonnes
        if clean_names:
            df_cleaned, name_changes = nettoyer_noms_colonnes(df_current)
            if not df_cleaned.equals(df_current):
                changes.append(f"Noms standardisés : {len(name_changes)} colonnes modifiées")
                df_current = df_cleaned

        # 2. Gestion des valeurs manquantes
        if missing_strategy != "Aucun traitement":
            if missing_strategy == "Supprimer lignes":
                avant = len(df_current)
                df_current = df_current.dropna()
                apres = len(df_current)
                if apres < avant:
                    changes.append(f"Lignes supprimées : {avant - apres}")
            elif missing_strategy in ["Imputer moyenne", "Imputer médiane", "Imputer mode"]:
                methode = missing_strategy.split()[1].lower()
                cols_numeriques = df_current.select_dtypes(include=[np.number]).columns
                df_current, impute_stats = imputer_valeurs_manquantes(df_current, cols_numeriques, methode)
                if impute_stats:
                    changes.append(f"Imputation {methode} : {len(impute_stats)} colonnes")

        # 3. Suppression des doublons
        if remove_duplicates:
            avant = len(df_current)
            df_current = df_current.drop_duplicates()
            apres = len(df_current)
            if apres < avant:
                changes.append(f"Doublons supprimés : {avant - apres}")

        # 4. Encodage
        if encoding_strategy != "Aucun":
            qualitatives = [c for c in df_current.columns if c in classifier_variables(df_current)['qualitative']]
            if qualitatives:
                methode = 'label' if encoding_strategy == "Label Encoding" else 'onehot'
                df_current, encoders = encoder_variables(df_current, qualitatives, methode)
                changes.append(f"Encodage {methode} : {len(qualitatives)} colonnes")

        # 5. Détection outliers
        if remove_outliers:
            outliers = detecter_outliers_multivaries(df_current, outlier_contamination)
            n_outliers = outliers.sum()
            if n_outliers > 0:
                changes.append(f"Outliers détectés : {n_outliers} lignes")

        # 6. Standardisation
        if standardize:
            cols_numeriques = df_current.select_dtypes(include=[np.number]).columns.tolist()
            if cols_numeriques:
                df_current, scaler = standardiser_donnees(df_current, cols_numeriques)
                changes.append(f"Standardisation : {len(cols_numeriques)} colonnes")

        # Mise à jour du DataFrame traité
        st.session_state.df_processed = df_current
        if changes:
            st.session_state.changes_log.extend(changes)

    else:
        st.error(f"Erreur de chargement : {error}")

# --- AFFICHAGE PRINCIPAL ---
if st.session_state.df_original is not None:
    # Analyser l'état actuel
    analyse_actuelle = analyser_qualite_dataset(st.session_state.df_processed, "Dataset traité")

    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value-sm">{analyse_actuelle['quality_score']:.0f}</div>
            <div class="metric-label-sm">Score qualité</div>
            <span class="quality-badge {analyse_actuelle['quality_badge']}">{analyse_actuelle['quality_category']}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        delta = analyse_actuelle['quality_score'] - st.session_state.analyse_original['quality_score']
        delta_color = "normal" if delta >= 0 else "inverse"
        st.metric(
            "Amélioration",
            f"{delta:+.1f}",
            delta=f"{delta:+.1f} pts",
            delta_color=delta_color
        )

    with col3:
        st.metric(
            "Lignes",
            f"{analyse_actuelle['total_lignes']:,}",
            delta=f"{analyse_actuelle['total_lignes'] - st.session_state.analyse_original['total_lignes']:+d}"
        )

    with col4:
        st.metric(
            "Colonnes",
            analyse_actuelle['total_colonnes'],
            delta=f"{analyse_actuelle['total_colonnes'] - st.session_state.analyse_original['total_colonnes']:+d}"
        )

    # Historique des changements
    if st.session_state.changes_log:
        with st.expander("📝 Dernières modifications"):
            for change in st.session_state.changes_log[-5:]:
                st.success(change)

    # Tabs principales
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Aperçu", "🔍 Problèmes", "📈 Visualisations",
        "💡 Suggestions", "📊 Analyse avancée", "🔄 Comparaison"
    ])

    with tab1:
        st.dataframe(st.session_state.df_processed.head(100), use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Types de données:**")
            st.json(dict(analyse_actuelle['dtypes_summary']))
        with col_b:
            if st.button("📥 Télécharger dataset traité"):
                csv = st.session_state.df_processed.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="dataset_traite.csv">Télécharger CSV</a>'
                st.markdown(href, unsafe_allow_html=True)

    with tab2:
        if analyse_actuelle['problem_columns']:
            if filters:
                filtered = afficher_filtres_variables(analyse_actuelle)
                for prob in filtered[:10]:
                    severity_color = "🔴" if prob['severity'] > 3 else "🟡" if prob['severity'] > 1 else "🟢"
                    st.markdown(f"""
                    <div class="info-box">
                        <strong>{severity_color} {prob['nom']}</strong> - Type: {prob['type']}<br>
                        {' · '.join(prob['issues'])}<br>
                        <small>Manquantes: {prob['pct_nulles']:.1f}% | Uniques: {prob['uniques']}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                for prob in analyse_actuelle['problem_columns'][:15]:
                    severity_color = "🔴" if prob['severity'] > 3 else "🟡" if prob['severity'] > 1 else "🟢"
                    st.markdown(f"""
                    <div class="info-box">
                        <strong>{severity_color} {prob['colonne']}</strong><br>
                        {' · '.join(prob['issues'])}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.success("✅ Aucun problème détecté !")

    with tab3:
        fig = creer_dashboard_qualite(analyse_actuelle)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        suggestions = suggerer_traitements(analyse_actuelle)
        if suggestions:
            for sug in suggestions[:10]:
                if sug['type'] == 'danger':
                    st.error(sug['message'])
                elif sug['type'] == 'warning':
                    st.warning(sug['message'])
                else:
                    st.info(sug['message'])
        else:
            st.success("✅ Aucune suggestion - Dataset propre !")

    with tab5:
        st.markdown("### 📊 Analyse statistique avancée")

        # Matrice de corrélation
        if show_correlation:
            st.markdown("#### 🔗 Matrice de corrélation")
            corr_matrix, high_corr = matrice_correlation(st.session_state.df_processed, corr_threshold)

            if corr_matrix is not None:
                fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                                     color_continuous_scale='RdBu_r')
                fig_corr.update_layout(height=600)
                st.plotly_chart(fig_corr, use_container_width=True)

                if high_corr:
                    st.warning(f"⚠️ {len(high_corr)} paires fortement corrélées (> {corr_threshold})")
                    for hc in high_corr[:5]:
                        st.info(f"📊 {hc['col1']} ↔ {hc['col2']} : {hc['correlation']:.2f}")
            else:
                st.info("Pas assez de variables numériques pour la corrélation")

        # Test de normalité
        if show_normality:
            st.markdown("#### 📈 Test de normalité (Shapiro-Wilk)")
            cols_num = st.session_state.df_processed.select_dtypes(include=[np.number]).columns[:10]
            if len(cols_num) > 0:
                norm_results = test_normalite(st.session_state.df_processed, cols_num)
                for res in norm_results:
                    emoji = "✅" if res['normal'] else "❌"
                    st.write(f"{emoji} **{res['colonne']}** : {res['interpretation']} (p={res['p_value']:.4f})")
            else:
                st.info("Pas de variables numériques pour le test")

        # Profilage rapide
        if show_profiling:
            st.markdown("#### 📋 Profilage rapide")
            profil = profil_donnees_rapide(st.session_state.df_processed)

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.metric("Colonnes constantes", profil['colonnes_constantes'])
                st.metric("Colonnes uniques (ID)", profil['colonnes_uniques'])
            with col_p2:
                st.metric("Colonnes avec manquantes", profil['colonnes_manquantes'])
                st.metric("Total valeurs manquantes", profil['total_manquantes'])

        # Profilage complet ydata
        if show_full_profiling and PROFILING_AVAILABLE:
            st.markdown("#### 📑 Profilage complet")
            if st.button("Générer le rapport complet"):
                with st.spinner("Génération du rapport en cours..."):
                    profile = ProfileReport(st.session_state.df_processed, title="Rapport Data Quality")
                    profile.to_file("rapport_complet.html")
                    st.success("Rapport généré !")
                    with open("rapport_complet.html", "r") as f:
                        html_data = f.read()
                        st.download_button(
                            label="📥 Télécharger rapport HTML",
                            data=html_data,
                            file_name="rapport_complet.html",
                            mime="text/html"
                        )

    with tab6:
        if st.session_state.analyse_original:
            st.markdown("### 🔄 Comparaison Avant / Après")

            # Vue split
            split_view_comparaison(
                st.session_state.df_original,
                st.session_state.df_processed,
                st.session_state.changes_log
            )

            # Radar chart
            fig_radar = creer_comparaison_radar(st.session_state.analyse_original, analyse_actuelle)
            st.plotly_chart(fig_radar, use_container_width=True)

            # Tableau comparatif
            comp = comparer_datasets(st.session_state.analyse_original, analyse_actuelle)

            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                st.metric("Score", f"{comp['avant']['quality_score']:.1f} → {comp['apres']['quality_score']:.1f}",
                          f"{comp['amelioration_score']:+.1f}")
            with col_c2:
                st.metric("Lignes", f"{comp['avant']['total_lignes']} → {comp['apres']['total_lignes']}",
                          f"-{comp['reduction_lignes']}")
            with col_c3:
                st.metric("Problèmes",
                          f"{len(comp['avant']['problem_columns'])} → {len(comp['apres']['problem_columns'])}",
                          f"-{comp['resolution_problemes']}")

    # Génération de rapport
    if report_format != "Texte":
        historique = st.session_state.history if include_history else None
        rapport_html = generer_rapport_html(analyse_actuelle, historique)

        if report_format in ["HTML", "Les deux"]:
            st.download_button(
                label="📥 Télécharger rapport HTML",
                data=rapport_html,
                file_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                mime="text/html"
            )

        if report_format in ["Texte", "Les deux"]:
            # Version texte simplifiée
            rapport_txt = f"""
            RAPPORT DATA QUALITY
            ====================
            Dataset: {analyse_actuelle['nom']}
            Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}

            Score qualité: {analyse_actuelle['quality_score']:.1f}/100 ({analyse_actuelle['quality_category']})

            Informations:
            - Lignes: {analyse_actuelle['total_lignes']:,}
            - Colonnes: {analyse_actuelle['total_colonnes']}
            - Mémoire: {analyse_actuelle['memoire']:.2f} MB

            Qualité:
            - Valeurs manquantes: {analyse_actuelle['total_missing']} ({analyse_actuelle['pct_missing']:.1f}%)
            - Doublons: {analyse_actuelle['duplicates']} ({analyse_actuelle['pct_duplicates']:.1f}%)

            Problèmes: {len(analyse_actuelle['problem_columns'])}
            """

            st.download_button(
                label="📥 Télécharger rapport texte",
                data=rapport_txt,
                file_name=f"rapport_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )

else:
    # Message d'accueil
    st.markdown("""
    <div style="text-align: center; padding: 4rem; background: white; border-radius: 20px;">
        <div style="font-size: 5rem; margin-bottom: 1rem;">📊</div>
        <h2 style="color: #2d3748;">Bienvenue sur Data Quality Analyzer Pro</h2>
        <p style="color: #718096; font-size: 1.2rem; max-width: 600px; margin: 1rem auto;">
            Chargez un fichier pour commencer l'analyse. Notre outil intelligent détectera automatiquement
            les problèmes de qualité et vous proposera des solutions de nettoyage.
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem;">
            <div>📁 CSV, Excel, JSON</div>
            <div>🔍 Détection outliers</div>
            <div>🧹 Nettoyage auto</div>
            <div>📈 Visualisations</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    <strong>🔬 Data Quality Analyzer Pro</strong> · Analyse intelligente et traitement automatisé<br>
    <span style="opacity: 0.7;">© 2026 - Version 2.0 · Tous droits réservés</span>
</div>
""", unsafe_allow_html=True)