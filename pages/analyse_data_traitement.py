import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import re
from datetime import datetime
# NOUVEAUX IMPORTS - CORRECTION
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from scipy import stats  # IMPORTANT: garder 'stats' pour scipy.stats
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
    page_title="Data Quality Analyzer | Analyse de données",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# INITIALISATION COMPLÈTE DE SESSION STATE (AJOUT IMPORTANT)
# ============================================================

# Variables de contrôle
if 'apply_cleaning' not in st.session_state:
    st.session_state.apply_cleaning = False
if 'generate_report' not in st.session_state:
    st.session_state.generate_report = False

# Variables pour les données nettoyées
if 'df_avant_cleaned' not in st.session_state:
    st.session_state.df_avant_cleaned = None
if 'changes_log' not in st.session_state:
    st.session_state.changes_log = []

# Variables pour les options de nettoyage
if 'clean_names' not in st.session_state:
    st.session_state.clean_names = False
if 'missing_strategy' not in st.session_state:
    st.session_state.missing_strategy = "Aucun"
if 'encoding_strategy' not in st.session_state:
    st.session_state.encoding_strategy = "Aucun"
if 'detect_outliers' not in st.session_state:
    st.session_state.detect_outliers = False
if 'outlier_contamination' not in st.session_state:  # AJOUT CRITIQUE
    st.session_state.outlier_contamination = 0.1
if 'standardize_method' not in st.session_state:
    st.session_state.standardize_method = "Aucun"

# Variables pour l'analyse avancée
if 'show_correlation' not in st.session_state:
    st.session_state.show_correlation = True
if 'corr_threshold' not in st.session_state:
    st.session_state.corr_threshold = 0.8
if 'show_normality' not in st.session_state:
    st.session_state.show_normality = False
if 'show_quick_profile' not in st.session_state:
    st.session_state.show_quick_profile = True
if 'show_full_profile' not in st.session_state:
    st.session_state.show_full_profile = False

# Variables pour le reporting
if 'generate_html_report' not in st.session_state:
    st.session_state.generate_html_report = False
if 'include_history' not in st.session_state:
    st.session_state.include_history = True

# Variables pour les filtres
if 'filtre_seuil_missing' not in st.session_state:
    st.session_state.filtre_seuil_missing = 10
if 'filtre_outliers' not in st.session_state:
    st.session_state.filtre_outliers = False
if 'filtre_constantes' not in st.session_state:
    st.session_state.filtre_constantes = False

# Variables pour les options existantes
if 'show_details' not in st.session_state:
    st.session_state.show_details = True
if 'threshold_missing' not in st.session_state:
    st.session_state.threshold_missing = 10
if 'show_problem_details' not in st.session_state:
    st.session_state.show_problem_details = True

# --- STYLE CSS AMÉLIORÉ AVEC SIDEBAR BLANC STYLISÉE ---
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
# NOUVELLES FONCTIONS AJOUTÉES (SANS MODIFIER L'EXISTANT)
# ============================================================

# --- 1. FONCTIONS DE TRAITEMENT AUTOMATISÉ (DATA CLEANING) ---

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
    stats_imp = {}

    for col in colonnes:
        if col in df_imp.columns:
            if methode == 'moyenne' and pd.api.types.is_numeric_dtype(df_imp[col]):
                valeur = df_imp[col].mean()
                stats_imp[col] = {'methode': 'moyenne', 'valeur': valeur}
                df_imp[col].fillna(valeur, inplace=True)
            elif methode == 'mediane' and pd.api.types.is_numeric_dtype(df_imp[col]):
                valeur = df_imp[col].median()
                stats_imp[col] = {'methode': 'médiane', 'valeur': valeur}
                df_imp[col].fillna(valeur, inplace=True)
            elif methode == 'mode':
                valeur = df_imp[col].mode()[0] if not df_imp[col].mode().empty else None
                if valeur is not None:
                    stats_imp[col] = {'methode': 'mode', 'valeur': valeur}
                    df_imp[col].fillna(valeur, inplace=True)

    return df_imp, stats_imp


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


def standardiser_donnees(df, colonnes, methode='zscore'):
    """
    Standardisation (Z-score) ou Normalisation (MinMax) des variables numériques
    """
    df_std = df.copy()

    if colonnes:
        if methode == 'zscore':
            scaler = StandardScaler()
            df_std[colonnes] = scaler.fit_transform(df_std[colonnes])
        elif methode == 'minmax':
            scaler = MinMaxScaler()
            df_std[colonnes] = scaler.fit_transform(df_std[colonnes])

    return df_std


# --- 2. FONCTIONS D'ANALYSE STATISTIQUE AVANCÉE ---

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
                # CORRECTION: utiliser stats.shapiro (pas stats['shapiro'])
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


# --- 3. FONCTIONS DE REPORTING AVANCÉ ---

def generer_rapport_html(analyse, comparaison=None, historique=None):
    """
    Génère un rapport HTML complet avec graphiques et comparaison
    """
    # Créer les graphiques en base64 pour les inclure dans le HTML
    import io
    import base64
    import matplotlib.pyplot as plt

    # Fonction pour convertir un graphique Plotly en image base64
    def fig_to_base64(fig):
        buf = io.BytesIO()
        fig.write_image(buf, format='png', width=800, height=400)
        buf.seek(0)
        return base64.b64encode(buf.getvalue()).decode()

    # Créer les graphiques avec Plotly
    # Graphique 1: Distribution des types de variables
    type_counts = {
        'Quantitatives': len(analyse['classification']['quantitative']),
        'Qualitatives': len(analyse['classification']['qualitative']),
        'Dates': len(analyse['classification']['dates'])
    }
    fig1 = px.pie(values=list(type_counts.values()), names=list(type_counts.keys()),
                  title="Types de variables", color_discrete_sequence=['#48bb78', '#667eea', '#ed8936'])
    fig1.update_layout(height=400)

    # Graphique 2: Top valeurs manquantes
    if analyse['missing_cols']:
        missing_df = pd.DataFrame({
            'Colonne': list(analyse['missing_cols'].keys()),
            'Manquantes': list(analyse['missing_cols'].values())
        }).sort_values('Manquantes', ascending=False).head(10)
        fig2 = px.bar(missing_df, x='Manquantes', y='Colonne', orientation='h',
                      title="Top 10 valeurs manquantes", color='Manquantes',
                      color_continuous_scale='Reds')
        fig2.update_layout(height=400)
    else:
        fig2 = None

    # Graphique 3: Matrice de corrélation (si disponible)
    if len(analyse['classification']['quantitative']) > 1:
        # Reconstruire un DataFrame pour la corrélation (simplifié)
        # Dans un cas réel, vous auriez besoin du DataFrame original
        fig3 = None
    else:
        fig3 = None

    # Graphique 4: Évolution du score (si comparaison)
    if comparaison:
        fig4 = go.Figure()
        categories = ['Score qualité', 'Complétude', 'Unicité']
        avant_values = [
            analyse['quality_score'],
            100 - analyse['pct_missing'],
            100 - analyse['pct_duplicates']
        ]
        apres_values = [
            comparaison['apres']['quality_score'],
            100 - comparaison['apres']['pct_missing'],
            100 - comparaison['apres']['pct_duplicates']
        ]

        fig4.add_trace(go.Scatterpolar(
            r=avant_values + [avant_values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Avant',
            line_color='#e53e3e'
        ))

        fig4.add_trace(go.Scatterpolar(
            r=apres_values + [apres_values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Après',
            line_color='#48bb78'
        ))

        fig4.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            height=400,
            title="Comparaison Avant/Après"
        )
    else:
        fig4 = None

    # Convertir les graphiques en base64
    fig1_base64 = fig_to_base64(fig1) if fig1 else ""
    fig2_base64 = fig_to_base64(fig2) if fig2 else ""
    fig4_base64 = fig_to_base64(fig4) if fig4 else ""

    # Déterminer la catégorie de qualité
    quality_badge_class = analyse['quality_badge'].replace('badge-', '')

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rapport Data Quality - {analyse['nom']}</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}

            body {{ 
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #f6f9f8 0%, #edf3f0 100%);
                margin: 0;
                padding: 20px;
                color: #1e293b;
            }}

            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 30px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }}

            .header {{ 
                background: linear-gradient(135deg, #667eea, #764ba2); 
                color: white; 
                padding: 40px 30px; 
                text-align: center;
                position: relative;
                overflow: hidden;
            }}

            .header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #feca57);
            }}

            .header::after {{
                content: '📊';
                position: absolute;
                bottom: -20px;
                right: -20px;
                font-size: 8rem;
                opacity: 0.1;
                transform: rotate(-15deg);
            }}

            .header h1 {{
                font-size: 2.5rem;
                font-weight: 700;
                margin-bottom: 10px;
                position: relative;
                z-index: 1;
            }}

            .header p {{
                font-size: 1.1rem;
                opacity: 0.9;
                position: relative;
                z-index: 1;
            }}

            .section {{ 
                background: white; 
                padding: 30px; 
                margin: 20px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.05);
                border: 1px solid #e2e8f0;
                transition: transform 0.3s ease;
            }}

            .section:hover {{
                transform: translateY(-5px);
                box-shadow: 0 20px 40px rgba(102, 126, 234, 0.1);
            }}

            .section-title {{
                display: flex;
                align-items: center;
                gap: 10px;
                color: #2d3748;
                font-size: 1.5rem;
                font-weight: 600;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #e2e8f0;
            }}

            .section-title span {{
                font-size: 2rem;
            }}

            .score-container {{
                text-align: center;
                padding: 20px;
                background: linear-gradient(135deg, #f8fafc, #ffffff);
                border-radius: 15px;
                margin-bottom: 20px;
            }}

            .score {{ 
                font-size: 5rem; 
                font-weight: 800; 
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                line-height: 1;
                display: inline-block;
                filter: drop-shadow(0 10px 20px rgba(102, 126, 234, 0.2));
            }}

            .badge {{ 
                display: inline-block; 
                padding: 10px 25px; 
                border-radius: 50px; 
                font-weight: 600; 
                font-size: 1.1rem;
                margin: 10px 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}

            .badge-excellent {{ background: linear-gradient(135deg, #48bb78, #38a169); color: white; }}
            .badge-good {{ background: linear-gradient(135deg, #667eea, #5a67d8); color: white; }}
            .badge-fair {{ background: linear-gradient(135deg, #ed8936, #dd6b20); color: white; }}
            .badge-poor {{ background: linear-gradient(135deg, #e53e3e, #c53030); color: white; }}

            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }}

            .stat-card {{
                background: #f8fafc;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                border: 1px solid #e2e8f0;
                transition: all 0.3s ease;
            }}

            .stat-card:hover {{
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.1);
                border-color: #667eea;
            }}

            .stat-number {{
                font-size: 2.2rem;
                font-weight: 700;
                color: #667eea;
                line-height: 1.2;
            }}

            .stat-label {{
                color: #64748b;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                margin-top: 5px;
                font-weight: 500;
            }}

            .progress-container {{
                background: #edf2f7;
                height: 10px;
                border-radius: 20px;
                overflow: hidden;
                margin: 10px 0;
            }}

            .progress-bar {{
                height: 100%;
                background: linear-gradient(90deg, #667eea, #764ba2);
                border-radius: 20px;
                transition: width 0.3s ease;
            }}

            table {{ 
                width: 100%; 
                border-collapse: collapse; 
                margin: 15px 0;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            }}

            th, td {{ 
                padding: 15px; 
                text-align: left; 
                border-bottom: 1px solid #e2e8f0; 
            }}

            th {{ 
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                font-weight: 600;
            }}

            tr:hover {{
                background: #f8fafc;
            }}

            .chart-container {{
                background: white;
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                border: 1px solid #e2e8f0;
            }}

            .chart-title {{
                color: #2d3748;
                font-weight: 600;
                margin-bottom: 15px;
                font-size: 1.2rem;
                display: flex;
                align-items: center;
                gap: 10px;
            }}

            .chart-title span {{
                font-size: 1.5rem;
            }}

            .chart-image {{
                width: 100%;
                height: auto;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            }}

            .comparison-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin: 20px 0;
            }}

            .comparison-card {{
                background: #f8fafc;
                padding: 20px;
                border-radius: 15px;
                border: 1px solid #e2e8f0;
            }}

            .comparison-card h4 {{
                color: #2d3748;
                margin-bottom: 15px;
                font-size: 1.1rem;
                border-bottom: 1px solid #e2e8f0;
                padding-bottom: 10px;
            }}

            .metric-improvement {{
                font-size: 1rem;
                font-weight: 600;
                margin-left: 5px;
            }}

            .improvement-positive {{
                color: #48bb78;
            }}

            .improvement-negative {{
                color: #e53e3e;
            }}

            .footer {{ 
                text-align: center; 
                padding: 30px; 
                background: linear-gradient(135deg, #f8fafc, #ffffff);
                color: #64748b;
                font-size: 0.9rem;
                border-top: 1px solid #e2e8f0;
            }}

            .footer strong {{
                color: #667eea;
            }}

            @media print {{
                body {{
                    background: white;
                    padding: 0;
                }}
                .container {{
                    box-shadow: none;
                }}
                .section {{
                    break-inside: avoid;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Rapport d'analyse - {analyse['nom']}</h1>
                <p>Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</p>
            </div>

            <div class="section">
                <div class="section-title">
                    <span>📈</span> Score de qualité
                </div>
                <div class="score-container">
                    <div class="score">{analyse['quality_score']:.1f}/100</div>
                    <span class="badge badge-{quality_badge_class}">{analyse['quality_category']}</span>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{analyse['total_lignes']:,}</div>
                        <div class="stat-label">Lignes</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{analyse['total_colonnes']}</div>
                        <div class="stat-label">Colonnes</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{analyse['memoire']:.2f}</div>
                        <div class="stat-label">MB</div>
                    </div>
                </div>

                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">{analyse['total_missing']:,}</div>
                        <div class="stat-label">Valeurs manquantes</div>
                        <div class="progress-container">
                            <div class="progress-bar" style="width:{analyse['pct_missing']}%"></div>
                        </div>
                        <small>{analyse['pct_missing']:.1f}%</small>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{analyse['duplicates']:,}</div>
                        <div class="stat-label">Doublons</div>
                        <div class="progress-container">
                            <div class="progress-bar" style="width:{analyse['pct_duplicates']}%"></div>
                        </div>
                        <small>{analyse['pct_duplicates']:.1f}%</small>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{len(analyse['problem_columns'])}</div>
                        <div class="stat-label">Problèmes détectés</div>
                    </div>
                </div>
            </div>

            <div class="section">
                <div class="section-title">
                    <span>📊</span> Types de données
                </div>
                <table>
                    <tr>
                        <th>Type</th>
                        <th>Nombre</th>
                        <th>Pourcentage</th>
                    </tr>
    """

    for dtype, count in analyse['dtypes_summary'].items():
        pct = (count / analyse['total_colonnes']) * 100
        html += f"""
                    <tr>
                        <td>{dtype}</td>
                        <td>{count}</td>
                        <td>{pct:.1f}%</td>
                    </tr>
        """

    html += """
                </table>
            </div>
    """

    # Ajouter les graphiques
    if fig1_base64:
        html += f"""
            <div class="section">
                <div class="section-title">
                    <span>🥧</span> Distribution des variables
                </div>
                <div class="chart-container">
                    <img src="data:image/png;base64,{fig1_base64}" class="chart-image" alt="Distribution des variables">
                </div>
            </div>
        """

    if fig2_base64 and analyse['missing_cols']:
        html += f"""
            <div class="section">
                <div class="section-title">
                    <span>⚠️</span> Top valeurs manquantes
                </div>
                <div class="chart-container">
                    <img src="data:image/png;base64,{fig2_base64}" class="chart-image" alt="Valeurs manquantes">
                </div>
            </div>
        """

    # Section problèmes détectés
    if analyse['problem_columns']:
        html += """
            <div class="section">
                <div class="section-title">
                    <span>⚠️</span> Problèmes détectés
                </div>
                <table>
                    <tr>
                        <th>Colonne</th>
                        <th>Problèmes</th>
                    </tr>
        """

        for prob in analyse['problem_columns'][:15]:
            html += f"""
                    <tr>
                        <td><strong>{prob['colonne']}</strong></td>
                        <td>{', '.join(prob['issues'])}</td>
                    </tr>
            """

        if len(analyse['problem_columns']) > 15:
            html += f"""
                    <tr>
                        <td colspan="2" style="text-align: center; font-style: italic;">
                            ... et {len(analyse['problem_columns']) - 15} autres problèmes
                        </td>
                    </tr>
            """

        html += """
                </table>
            </div>
        """

    # Section comparaison (si disponible)
    if comparaison:
        html += f"""
            <div class="section">
                <div class="section-title">
                    <span>🔄</span> Comparaison Original vs Nettoyé
                </div>

                <div class="comparison-grid">
                    <div class="comparison-card">
                        <h4>📋 Dataset Original</h4>
                        <table style="margin:0;">
                            <tr><td>Score qualité</td><td><strong>{comparaison['avant']['quality_score']:.1f}</strong></td></tr>
                            <tr><td>Lignes</td><td>{comparaison['avant']['total_lignes']:,}</td></tr>
                            <tr><td>Colonnes</td><td>{comparaison['avant']['total_colonnes']}</td></tr>
                            <tr><td>Valeurs manquantes</td><td>{comparaison['avant']['total_missing']} ({comparaison['avant']['pct_missing']:.1f}%)</td></tr>
                            <tr><td>Doublons</td><td>{comparaison['avant']['duplicates']} ({comparaison['avant']['pct_duplicates']:.1f}%)</td></tr>
                            <tr><td>Problèmes</td><td>{len(comparaison['avant']['problem_columns'])}</td></tr>
                        </table>
                    </div>

                    <div class="comparison-card">
                        <h4>✨ Dataset Nettoyé</h4>
                        <table style="margin:0;">
                            <tr><td>Score qualité</td><td><strong>{comparaison['apres']['quality_score']:.1f}</strong></td></tr>
                            <tr><td>Lignes</td><td>{comparaison['apres']['total_lignes']:,}</td></tr>
                            <tr><td>Colonnes</td><td>{comparaison['apres']['total_colonnes']}</td></tr>
                            <tr><td>Valeurs manquantes</td><td>{comparaison['apres']['total_missing']} ({comparaison['apres']['pct_missing']:.1f}%)</td></tr>
                            <tr><td>Doublons</td><td>{comparaison['apres']['duplicates']} ({comparaison['apres']['pct_duplicates']:.1f}%)</td></tr>
                            <tr><td>Problèmes</td><td>{len(comparaison['apres']['problem_columns'])}</td></tr>
                        </table>
                    </div>
                </div>

                <div style="margin-top:20px; padding:20px; background:#f8fafc; border-radius:15px;">
                    <h4 style="margin-bottom:15px;">📊 Bilan du nettoyage</h4>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">{comparaison['amelioration_score']:+.1f}</div>
                            <div class="stat-label">Amélioration score</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{comparaison['reduction_lignes']}</div>
                            <div class="stat-label">Lignes supprimées</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{comparaison['reduction_missing']}</div>
                            <div class="stat-label">Manquantes en moins</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{comparaison['reduction_duplicates']}</div>
                            <div class="stat-label">Doublons supprimés</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{comparaison['reduction_problemes']:+d}</div>
                            <div class="stat-label">Problèmes résolus</div>
                        </div>
                    </div>
                </div>
        """

        if fig4_base64:
            html += f"""
                <div class="chart-container">
                    <div class="chart-title">
                        <span>📊</span> Évolution de la qualité
                    </div>
                    <img src="data:image/png;base64,{fig4_base64}" class="chart-image" alt="Comparaison radar">
                </div>
            """

        html += """
            </div>
        """

    # Section historique (si disponible)
    if historique:
        html += """
            <div class="section">
                <div class="section-title">
                    <span>📜</span> Historique des traitements
                </div>
                <table>
                    <tr>
                        <th>Étape</th>
                        <th>Score avant</th>
                        <th>Score après</th>
                        <th>Amélioration</th>
                    </tr>
        """

        for i, h in enumerate(historique):
            amelioration = h.get('amelioration', 0)
            color_class = "improvement-positive" if amelioration > 0 else "improvement-negative" if amelioration < 0 else ""
            html += f"""
                    <tr>
                        <td>{h.get('etape', f'Étape {i + 1}')}</td>
                        <td>{h.get('score_avant', 0):.1f}</td>
                        <td>{h.get('score_apres', 0):.1f}</td>
                        <td class="{color_class}">{amelioration:+.1f}</td>
                    </tr>
            """

        html += """
                </table>
            </div>
        """

    html += """
            <div class="footer">
                <strong>Data Quality Analyzer v3.0</strong> · Rapport généré automatiquement<br>
                <span style="opacity: 0.7;">© 2026 - Tous droits réservés</span>
            </div>
        </div>
    </body>
    </html>
    """

    return html


def split_view_comparaison(df_avant, df_apres, changes):
    """
    Affiche une vue comparative avec mise en évidence des changements
    """
    st.markdown("### 🔍 Vue comparative (Avant vs Après)")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📋 Dataset AVANT**")
        st.dataframe(df_avant.head(10), use_container_width=True)

    with col2:
        st.markdown("**✨ Dataset APRÈS**")
        st.dataframe(df_apres.head(10), use_container_width=True)

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
        seuil_missing = st.slider("Seuil valeurs manquantes (%)", 0, 100, 10, key="filtre_seuil_missing")

    with col2:
        show_outliers = st.checkbox("Afficher uniquement les colonnes avec outliers", key="filtre_outliers")

    with col3:
        show_constantes = st.checkbox("Afficher les colonnes constantes", key="filtre_constantes")

    return seuil_missing, show_outliers, show_constantes


# --- FONCTIONS D'ANALYSE DE DONNÉES EXISTANTES (inchangées) ---
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
        stats_col = {
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
            stats_col['min'] = df[col].min() if not df[col].isnull().all() else None
            stats_col['max'] = df[col].max() if not df[col].isnull().all() else None
            stats_col['mean'] = df[col].mean() if not df[col].isnull().all() else None
            stats_col['std'] = df[col].std() if not df[col].isnull().all() else None
            stats_col['skew'] = df[col].skew() if not df[col].isnull().all() else None

            if not df[col].isnull().all():
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
                stats_col['outliers'] = outliers
                stats_col['pct_outliers'] = (outliers / total_lignes) * 100 if total_lignes > 0 else 0

        col_stats.append(stats_col)

    missing_values = df.isnull().sum()
    missing_cols = missing_values[missing_values > 0]
    total_missing = missing_values.sum()
    pct_missing = (total_missing / (total_lignes * total_colonnes)) * 100 if (total_lignes * total_colonnes) > 0 else 0

    duplicates = df.duplicated().sum()
    pct_duplicates = (duplicates / total_lignes) * 100 if total_lignes > 0 else 0

    problem_columns = []
    for stats_col in col_stats:
        issues = []

        if ' ' in stats_col['nom'] or any(c in stats_col['nom'] for c in '!@#$%^&*()+='):
            issues.append("Nom non standard")
        if stats_col['uniques'] == 1:
            issues.append("Constante")
        if stats_col['uniques'] == total_lignes:
            issues.append("Potentiel ID")
        if stats_col['pct_nulles'] > 30:
            issues.append(f"{stats_col['pct_nulles']:.1f}% manquantes")
        # Vérification simplifiée des types mixtes
        if 'outliers' in stats_col and stats_col['pct_outliers'] > 5:
            issues.append(f"{stats_col['pct_outliers']:.1f}% outliers")
        if 'skew' in stats_col and stats_col['skew'] is not None and abs(stats_col['skew']) > 1:
            issues.append(f"Asymétrie ({stats_col['skew']:.2f})")

        if issues:
            problem_columns.append({
                'colonne': stats_col['nom'],
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
        'reduction_missing': avant['total_missing'] - apres['total_missing'],
        'pct_reduction_missing': ((avant['total_missing'] - apres['total_missing']) / avant['total_missing']) * 100 if
        avant['total_missing'] > 0 else 0,
        'reduction_duplicates': avant['duplicates'] - apres['duplicates'],
        'pct_reduction_duplicates': ((avant['duplicates'] - apres['duplicates']) / avant['duplicates']) * 100 if avant[
                                                                                                                     'duplicates'] > 0 else 0,
        'reduction_problemes': len(avant['problem_columns']) - len(apres['problem_columns']),
        'nettoyage_reussi': apres['quality_score'] > avant['quality_score']
    }
    return comparaison


def verifier_nettoyage(comparaison):
    messages = []
    if comparaison['amelioration_score'] > 0:
        messages.append(("✅", "green", f"Score qualité amélioré de {comparaison['amelioration_score']:.1f} points"))
    else:
        messages.append(("❌", "red", "Le score qualité n'a pas augmenté"))

    if comparaison['reduction_missing'] > 0:
        messages.append(("✅", "green", f"Valeurs manquantes réduites de {comparaison['reduction_missing']}"))
    elif comparaison['reduction_missing'] < 0:
        messages.append(("⚠️", "orange", f"Nouvelles valeurs manquantes: {abs(comparaison['reduction_missing'])}"))

    if comparaison['reduction_duplicates'] > 0:
        messages.append(("✅", "green", f"Doublons réduits de {comparaison['reduction_duplicates']}"))

    if comparaison['reduction_problemes'] > 0:
        messages.append(("✅", "green", f"Problèmes résolus: {comparaison['reduction_problemes']}"))
    elif comparaison['reduction_problemes'] < 0:
        messages.append(("❌", "red", f"Nouveaux problèmes: {abs(comparaison['reduction_problemes'])}"))

    return messages


def generer_recommandations_feature_engineering(analyse):
    recommandations = []
    if analyse['classification']['quantitative']:
        for col in analyse['classification']['quantitative'][:5]:
            stats_col = next((s for s in analyse['col_stats'] if s['nom'] == col), None)
            if stats_col:
                if stats_col['std'] > 10:
                    recommandations.append({
                        'type': 'feature_engineering',
                        'categorie': 'Normalisation',
                        'colonne': col,
                        'technique': 'StandardScaler ou MinMaxScaler',
                        'raison': f"Grande échelle (std={stats_col['std']:.2f})",
                        'impact': 'Améliore la convergence des modèles',
                        'pour_ACP': True,
                        'priority': 'MOYENNE'
                    })

                if 'pct_outliers' in stats_col and stats_col['pct_outliers'] > 5:
                    recommandations.append({
                        'type': 'feature_engineering',
                        'categorie': 'Outliers',
                        'colonne': col,
                        'technique': 'Winsorisation ou transformation logarithmique',
                        'raison': f"{stats_col['pct_outliers']:.1f}% d'outliers",
                        'impact': 'Réduit l\'influence des valeurs extrêmes',
                        'pour_ACP': True,
                        'priority': 'MOYENNE'
                    })

                if 'skew' in stats_col and abs(stats_col['skew']) > 1:
                    transformation = 'log' if stats_col['skew'] > 1 else 'square' if stats_col[
                                                                                         'skew'] < -1 else 'box-cox'
                    recommandations.append({
                        'type': 'feature_engineering',
                        'categorie': 'Transformation',
                        'colonne': col,
                        'technique': f'Transformation {transformation}',
                        'raison': f"Asymétrie = {stats_col['skew']:.2f}",
                        'impact': 'Rend la distribution plus normale',
                        'pour_ACP': True,
                        'priority': 'MOYENNE'
                    })

    if len(analyse['classification']['quantitative']) >= 3:
        recommandations.append({
            'type': 'acp',
            'categorie': 'ACP',
            'technique': 'Analyse en Composantes Principales',
            'raison': f"{len(analyse['classification']['quantitative'])} variables quantitatives",
            'impact': 'Réduit la dimension et décorrèle les variables',
            'variables': analyse['classification']['quantitative'][:5],
            'priority': 'HAUTE'
        })

    return recommandations


def generer_recommandations_qualite(analyse):
    recommandations = []

    if analyse['pct_missing'] > 5:
        recommandations.append({
            'priority': 'HAUTE' if analyse['pct_missing'] > 20 else 'MOYENNE',
            'categorie': 'Valeurs manquantes',
            'message': f"{analyse['pct_missing']:.1f}% de valeurs manquantes",
            'action': "Imputer ou supprimer les colonnes/lignes concernées",
            'icon': '🔍'
        })

    if analyse['pct_duplicates'] > 1:
        recommandations.append({
            'priority': 'HAUTE' if analyse['pct_duplicates'] > 5 else 'MOYENNE',
            'categorie': 'Doublons',
            'message': f"{analyse['duplicates']} lignes dupliquées ({analyse['pct_duplicates']:.1f}%)",
            'action': "Supprimer les lignes dupliquées",
            'icon': '🔄'
        })

    for prob in analyse['problem_columns']:
        for issue in prob['issues']:
            if 'manquantes' in issue:
                recommandations.append({
                    'priority': 'MOYENNE',
                    'categorie': f"Colonne '{prob['colonne']}'",
                    'message': issue,
                    'action': f"Traiter les valeurs manquantes",
                    'icon': '📌'
                })
            elif 'Constante' in issue:
                recommandations.append({
                    'priority': 'BASSE',
                    'categorie': f"Colonne '{prob['colonne']}'",
                    'message': "Colonne constante",
                    'action': f"Envisager de supprimer",
                    'icon': '📊'
                })
            elif 'outliers' in issue:
                recommandations.append({
                    'priority': 'MOYENNE',
                    'categorie': f"Colonne '{prob['colonne']}'",
                    'message': issue,
                    'action': "Appliquer une transformation ou winsorisation",
                    'icon': '📈'
                })
            elif 'Asymétrie' in issue:
                recommandations.append({
                    'priority': 'MOYENNE',
                    'categorie': f"Colonne '{prob['colonne']}'",
                    'message': issue,
                    'action': "Appliquer une transformation logarithmique",
                    'icon': '📉'
                })

    return recommandations


# --- EN-TÊTE PRINCIPAL ---
st.markdown("""
    <div class="main-header floating shine">
        <h1 class="main-title">📊 Data Quality Analyzer</h1>
        <p class="main-subtitle">Analyse intelligente de la qualité des données · Comparaison aprés Nettoyage & Optimisation · Feature Engineering</p>
        <div style='display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap;'>
            <span class='badge-excellent quality-badge'>🎯 Classification auto</span>
            <span class='badge-good quality-badge'>📊 Feature engineering</span>
            <span class='badge-fair quality-badge'>🔬 Préparation ACP</span>
            <span class='badge-poor quality-badge'>💡 Recommandations ML</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR AMÉLIORÉE AVEC NOUVELLES OPTIONS ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <h3>📁 Chargement</h3>
            <p>Importez vos datasets</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📥 Dataset original")
    file_avant = st.file_uploader(
        "Charger le fichier original (obligatoire)",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'pkl', 'txt'],
        key="file_avant",
        help="Dataset avant nettoyage"
    )

    if file_avant:
        type_fichier = detecter_type_fichier(file_avant.name)
        st.info(f"📄 Original : {type_fichier}")

    st.markdown("---")

    st.markdown("### ✨ Dataset nettoyé")
    file_apres = st.file_uploader(
        "Charger la version nettoyée (optionnel)",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'pkl', 'txt'],
        key="file_apres",
        help="Version nettoyée à comparer avec l'original"
    )

    if file_apres:
        type_fichier = detecter_type_fichier(file_apres.name)
        st.info(f"📄 Nettoyé : {type_fichier}")

    st.markdown("---")

    # --- SECTION : OPTIONS DE TRAITEMENT AUTOMATISÉ ---
    with st.expander("🧹 Options de nettoyage automatique", expanded=False):
        st.markdown("**🏷️ Noms de colonnes**")
        clean_names = st.checkbox("Standardiser les noms (minuscules, underscores)", value=False, key="clean_names")

        st.markdown("**📉 Gestion des valeurs manquantes**")
        missing_strategy = st.radio(
            "Stratégie d'imputation",
            ["Aucun", "Supprimer lignes", "Moyenne", "Médiane", "Mode"],
            key="missing_strategy"
        )

        st.markdown("**🔄 Encodage des variables qualitatives**")
        encoding_strategy = st.radio(
            "Méthode d'encodage",
            ["Aucun", "Label Encoding", "One-Hot Encoding"],
            key="encoding_strategy"
        )

        st.markdown("**📊 Détection d'outliers**")
        detect_outliers = st.checkbox("Détection multivariée (Isolation Forest)", value=False, key="detect_outliers")
        if detect_outliers:
            outlier_contamination = st.slider("Taux de contamination", 0.01, 0.3, 0.1, 0.01,
                                              key="outlier_contamination")

        st.markdown("**⚖️ Standardisation**")
        standardize_method = st.radio(
            "Méthode",
            ["Aucun", "Z-score", "Min-Max"],
            key="standardize_method"
        )

        # CORRECTION: Ne pas modifier st.session_state.apply_cleaning ici
        if st.button("🚀 Appliquer le nettoyage", key="apply_cleaning_btn"):
            st.session_state.apply_cleaning = True

    # --- SECTION : ANALYSE STATISTIQUE AVANCÉE ---
    with st.expander("📈 Analyse avancée", expanded=False):
        show_correlation = st.checkbox("Afficher matrice de corrélation", value=True, key="show_correlation")
        if show_correlation:
            corr_threshold = st.slider("Seuil de corrélation", 0.5, 0.95, 0.8, 0.05, key="corr_threshold")

        show_normality = st.checkbox("Tester la normalité des variables", value=False, key="show_normality")
        show_quick_profile = st.checkbox("Afficher profil rapide", value=True, key="show_quick_profile")

        if PROFILING_AVAILABLE:
            show_full_profile = st.checkbox("Générer rapport complet (ydata-profiling)", value=False,
                                            key="show_full_profile")

    # --- SECTION : REPORTING ---
    with st.expander("📄 Reporting", expanded=False):
        generate_html_report = st.checkbox("Générer rapport HTML", value=False, key="generate_html_report")
        include_history = st.checkbox("Inclure historique dans le rapport", value=True, key="include_history")

        if st.button("📥 Générer rapport maintenant", key="generate_report_btn"):
            st.session_state.generate_report = True

    st.markdown("---")

    st.markdown("### ⚙️ Options existantes")
    show_details = st.checkbox("Afficher les détails par colonne", value=True, key="show_details")
    threshold_missing = st.slider("Seuil d'alerte valeurs manquantes (%)", 0, 50, 10, key="threshold_missing")
    show_problem_details = st.checkbox("Afficher les détails des problèmes", value=True, key="show_problem_details")

if file_avant:
    df_avant, error_avant = charger_fichier(file_avant)

    if error_avant:
        st.error(f"Erreur chargement original : {error_avant}")
    else:
        # CORRECTION: Récupérer les valeurs des widgets
        clean_names = st.session_state.clean_names
        missing_strategy = st.session_state.missing_strategy
        encoding_strategy = st.session_state.encoding_strategy
        detect_outliers = st.session_state.detect_outliers
        outlier_contamination = st.session_state.outlier_contamination  # Maintenant cette ligne fonctionne
        standardize_method = st.session_state.standardize_method
        show_correlation = st.session_state.show_correlation
        corr_threshold = st.session_state.corr_threshold
        show_normality = st.session_state.show_normality
        show_quick_profile = st.session_state.show_quick_profile
        show_full_profile = st.session_state.show_full_profile
        show_details = st.session_state.show_details
        threshold_missing = st.session_state.threshold_missing
        show_problem_details = st.session_state.show_problem_details

        # Application du nettoyage automatique si demandé
        if st.session_state.apply_cleaning:
            df_avant_original = df_avant.copy()
            changes_log = []

            # 1. Standardisation des noms
            if clean_names:
                df_avant, name_changes = nettoyer_noms_colonnes(df_avant)
                changes_log.append(f"Noms standardisés : {len(name_changes)} colonnes modifiées")

            # 2. Gestion des valeurs manquantes
            if missing_strategy != "Aucun":
                if missing_strategy == "Supprimer lignes":
                    avant = len(df_avant)
                    df_avant = df_avant.dropna()
                    apres = len(df_avant)
                    if apres < avant:
                        changes_log.append(f"Lignes supprimées : {avant - apres}")
                elif missing_strategy in ["Moyenne", "Médiane", "Mode"]:
                    methode_map = {"Moyenne": "moyenne", "Médiane": "mediane", "Mode": "mode"}
                    cols_numeriques = df_avant.select_dtypes(include=[np.number]).columns
                    df_avant, impute_stats = imputer_valeurs_manquantes(df_avant, cols_numeriques,
                                                                        methode_map[missing_strategy])
                    if impute_stats:
                        changes_log.append(f"Imputation {missing_strategy.lower()} : {len(impute_stats)} colonnes")

            # 3. Encodage
            if encoding_strategy != "Aucun":
                qualitatives = classifier_variables(df_avant)['qualitative']
                if qualitatives:
                    methode = 'label' if encoding_strategy == "Label Encoding" else 'onehot'
                    df_avant, encoders = encoder_variables(df_avant, qualitatives, methode)
                    changes_log.append(f"Encodage {encoding_strategy} : {len(qualitatives)} colonnes")

            # 4. Détection d'outliers
            if detect_outliers:
                outliers = detecter_outliers_multivaries(df_avant, outlier_contamination)
                n_outliers = outliers.sum()
                if n_outliers > 0:
                    changes_log.append(f"Outliers détectés : {n_outliers} lignes")
                    # Option pour filtrer les outliers
                    remove_outliers_checkbox = st.checkbox("Supprimer les outliers détectés", key="remove_outliers")
                    if remove_outliers_checkbox:
                        df_avant = df_avant[~outliers]
                        changes_log.append(f"Outliers supprimés : {n_outliers} lignes")

            # 5. Standardisation
            if standardize_method != "Aucun":
                cols_numeriques = df_avant.select_dtypes(include=[np.number]).columns.tolist()
                if cols_numeriques:
                    methode = 'zscore' if standardize_method == "Z-score" else 'minmax'
                    df_avant = standardiser_donnees(df_avant, cols_numeriques, methode)
                    changes_log.append(f"Standardisation {standardize_method} : {len(cols_numeriques)} colonnes")

            # Afficher les changements
            if changes_log:
                with st.expander("📝 Modifications appliquées"):
                    for change in changes_log:
                        st.success(change)

            # Sauvegarder dans session state pour comparaison
            st.session_state.df_avant_cleaned = df_avant
            st.session_state.changes_log = changes_log
            st.session_state.apply_cleaning = False

        with st.spinner("🔍 Analyse du dataset original..."):
            analyse_avant = analyser_qualite_dataset(df_avant, "Original")

        if file_apres:
            df_apres, error_apres = charger_fichier(file_apres)
            if error_apres:
                st.error(f"Erreur chargement nettoyé : {error_apres}")
                df_apres = None
                analyse_apres = None
                comparaison = None
            else:
                with st.spinner("🔍 Analyse du dataset nettoyé..."):
                    analyse_apres = analyser_qualite_dataset(df_apres, "Nettoyé")
                comparaison = comparer_datasets(analyse_avant, analyse_apres)
        else:
            df_apres = None
            analyse_apres = None
            comparaison = None

        st.markdown("## 📊 Dataset Original - Tableau de bord qualité")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
                <div class='quality-card'>
                    <div class='quality-score'>{analyse_avant['quality_score']:.1f}</div>
                    <div class='quality-label'>Score qualité</div>
                    <div style='margin-top:0.5rem;'>
                        <span class='quality-badge {analyse_avant['quality_badge']}'>
                            {analyse_avant['quality_category']}
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value-sm'>{analyse_avant['total_lignes']:,}</div>
                    <div class='metric-label-sm'>Lignes</div>
                    <div class='progress-container'><div class='progress-bar' style='width:100%'></div></div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value-sm'>{analyse_avant['total_colonnes']}</div>
                    <div class='metric-label-sm'>Colonnes</div>
                    <div class='progress-container'><div class='progress-bar' style='width:100%'></div></div>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value-sm'>{analyse_avant['memoire']:.2f}</div>
                    <div class='metric-label-sm'>MB</div>
                    <div class='progress-container'><div class='progress-bar' style='width:{min(100, analyse_avant['memoire'])}%'></div></div>
                </div>
            """, unsafe_allow_html=True)

        # --- TABS ---
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            "📋 Aperçu général",
            "🔢 Classification variables",
            "🔍 Détails colonnes",
            "⚠️ Problèmes détectés",
            "📈 Visualisations",
            "💡 Recommandations ML",
            "📊 Analyse avancée"  # NOUVEAU TAB
        ])

        with tab1:
            st.markdown('<div class="quality-card">', unsafe_allow_html=True)
            col_stat1, col_stat2 = st.columns(2)

            with col_stat1:
                st.markdown("### 📊 Statistiques globales")
                st.markdown(f"""
                    * **Lignes :** {analyse_avant['total_lignes']:,}
                    * **Colonnes :** {analyse_avant['total_colonnes']}
                    * **Mémoire :** {analyse_avant['memoire']:.2f} MB
                    * **Valeurs manquantes :** {analyse_avant['total_missing']:,} ({analyse_avant['pct_missing']:.1f}%)
                    * **Lignes dupliquées :** {analyse_avant['duplicates']:,} ({analyse_avant['pct_duplicates']:.1f}%)
                """)

            with col_stat2:
                st.markdown("### 📊 Types de données")
                for dtype, count in analyse_avant['dtypes_summary'].items():
                    pct = (count / analyse_avant['total_colonnes']) * 100
                    st.markdown(f"""
                        * **{dtype} :** {count} ({pct:.1f}%)
                        <div class='progress-container'><div class='progress-bar' style='width:{pct}%'></div></div>
                    """, unsafe_allow_html=True)

            if analyse_avant['missing_cols']:
                st.markdown("### ⚠️ Colonnes avec valeurs manquantes")
                for col, count in list(analyse_avant['missing_cols'].items())[:10]:
                    pct = (count / analyse_avant['total_lignes']) * 100
                    color = "#e53e3e" if pct > threshold_missing else "#ed8936"
                    st.markdown(f"""
                        * **{col} :** {count:,} ({pct:.1f}%)
                        <div class='progress-container'><div class='progress-bar' style='width:{pct}%; background:{color};'></div></div>
                    """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            col_var1, col_var2 = st.columns(2)

            with col_var1:
                st.markdown('<div class="quality-card">', unsafe_allow_html=True)
                st.markdown("### 📊 Variables Quantitatives")
                if analyse_avant['classification']['quantitative']:
                    st.markdown(f"**{len(analyse_avant['classification']['quantitative'])} variables**")
                    for col in analyse_avant['classification']['quantitative'][:10]:
                        stats_col = next((s for s in analyse_avant['col_stats'] if s['nom'] == col), None)
                        outliers = f" · {stats_col['pct_outliers']:.1f}% outliers" if stats_col and 'pct_outliers' in stats_col else ""
                        st.markdown(f"""
                            <div class='variable-item'>
                                <div class='variable-name'>
                                    {col}
                                    <span class='badge-quantitative'>QN</span>
                                </div>
                                <div class='variable-stats'>
                                    {stats_col['uniques']} valeurs · min={stats_col['min']:.1f} · max={stats_col['max']:.1f}{outliers}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    if len(analyse_avant['classification']['quantitative']) > 10:
                        st.info(f"... et {len(analyse_avant['classification']['quantitative']) - 10} autres")
                else:
                    st.info("Aucune variable quantitative")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_var2:
                st.markdown('<div class="quality-card">', unsafe_allow_html=True)
                st.markdown("### 🏷️ Variables Qualitatives")
                if analyse_avant['classification']['qualitative']:
                    st.markdown(f"**{len(analyse_avant['classification']['qualitative'])} variables**")
                    for col in analyse_avant['classification']['qualitative'][:10]:
                        stats_col = next((s for s in analyse_avant['col_stats'] if s['nom'] == col), None)
                        st.markdown(f"""
                            <div class='variable-item'>
                                <div class='variable-name'>
                                    {col}
                                    <span class='badge-qualitative'>QL</span>
                                </div>
                                <div class='variable-stats'>
                                    {stats_col['uniques']} catégories · {stats_col['non_nulles']} non-nulles
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    if len(analyse_avant['classification']['qualitative']) > 10:
                        st.info(f"... et {len(analyse_avant['classification']['qualitative']) - 10} autres")
                else:
                    st.info("Aucune variable qualitative")
                st.markdown('</div>', unsafe_allow_html=True)

            if analyse_avant['classification']['dates']:
                st.markdown('<div class="quality-card">', unsafe_allow_html=True)
                st.markdown("### 📅 Variables Date")
                for col in analyse_avant['classification']['dates']:
                    st.markdown(f"""
                        <div class='variable-item'>
                            <div class='variable-name'>
                                {col}
                                <span class='badge-date'>Date</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            if analyse_avant['classification']['target_potential']:
                st.markdown('<div class="quality-card">', unsafe_allow_html=True)
                st.markdown("### 🎯 Cibles potentielles ML")
                for target in analyse_avant['classification']['target_potential']:
                    st.markdown(f"""
                        <div class='variable-item'>
                            <div class='variable-name'>
                                {target['colonne']}
                                <span class='badge-target'>{target['type']}</span>
                            </div>
                            <div class='variable-stats'>{target['raison']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            if show_details:
                for stats_col in analyse_avant['col_stats'][:20]:
                    with st.expander(f"📊 {stats_col['nom']} ({stats_col['type']})"):
                        col_d1, col_d2, col_d3 = st.columns(3)

                        with col_d1:
                            st.metric("Non-nulles", f"{stats_col['non_nulles']:,}")
                            st.metric("Nulles", f"{stats_col['nulles']:,} ({stats_col['pct_nulles']:.1f}%)")

                        with col_d2:
                            st.metric("Valeurs uniques", f"{stats_col['uniques']:,}")
                            st.metric("Taux unicité", f"{stats_col['pct_uniques']:.1f}%")

                        with col_d3:
                            if 'min' in stats_col:
                                st.metric("Min", f"{stats_col['min']:.2f}")
                                st.metric("Max", f"{stats_col['max']:.2f}")
                                st.metric("Moyenne", f"{stats_col['mean']:.2f}")
                                if 'outliers' in stats_col:
                                    st.metric("Outliers", f"{stats_col['outliers']} ({stats_col['pct_outliers']:.1f}%)")

        with tab4:
            if analyse_avant['problem_columns']:
                if show_problem_details:
                    for prob in analyse_avant['problem_columns']:
                        color = "#e53e3e" if prob['severity'] > 2 else "#ed8936" if prob['severity'] > 1 else "#667eea"
                        st.markdown(f"""
                            <div class='timeline-item' style='border-left-color:{color};'>
                                <div class='timeline-icon'>⚠️</div>
                                <div>
                                    <strong style='color:{color};'>{prob['colonne']}</strong>
                                    <br><span style='color:#4a5568;'>{', '.join(prob['issues'])}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info(f"🔍 {len(analyse_avant['problem_columns'])} problèmes détectés (masqués)")
            else:
                st.success("✅ Aucun problème détecté !")

        with tab5:
            col_v1, col_v2 = st.columns(2)

            with col_v1:
                type_counts = {
                    'Quantitatives': len(analyse_avant['classification']['quantitative']),
                    'Qualitatives': len(analyse_avant['classification']['qualitative']),
                    'Dates': len(analyse_avant['classification']['dates'])
                }
                fig = px.pie(values=list(type_counts.values()), names=list(type_counts.keys()),
                             title="Types de variables", color_discrete_sequence=['#48bb78', '#667eea', '#ed8936'])
                fig.update_layout(height=350)
                st.plotly_chart(fig, width='stretch', key="plot_types")

            with col_v2:
                if analyse_avant['missing_cols']:
                    missing_df = pd.DataFrame({
                        'Colonne': list(analyse_avant['missing_cols'].keys()),
                        'Manquantes': list(analyse_avant['missing_cols'].values())
                    }).sort_values('Manquantes', ascending=False).head(10)
                    fig = px.bar(missing_df, x='Manquantes', y='Colonne', orientation='h',
                                 title="Top 10 valeurs manquantes", color='Manquantes',
                                 color_continuous_scale='Reds')
                    fig.update_layout(height=350)
                    st.plotly_chart(fig, width='stretch', key="plot_missing")
                else:
                    st.info("Aucune valeur manquante")

            if len(analyse_avant['classification']['quantitative']) > 1:
                corr_matrix = df_avant[analyse_avant['classification']['quantitative']].corr()
                fig = px.imshow(corr_matrix, text_auto='.2f', aspect="auto",
                                title="Matrice de corrélation", color_continuous_scale='RdBu')
                fig.update_layout(height=500)
                st.plotly_chart(fig, width='stretch', key="plot_corr")

        with tab6:
            st.markdown("### 🔧 Recommandations de nettoyage")
            recs_qualite = generer_recommandations_qualite(analyse_avant)
            if recs_qualite:
                for rec in recs_qualite:
                    color = "#e53e3e" if rec['priority'] == 'HAUTE' else "#ed8936" if rec[
                                                                                          'priority'] == 'MOYENNE' else "#667eea"
                    st.markdown(f"""
                        <div class='timeline-item' style='border-left-color:{color};'>
                            <div class='timeline-icon'>{rec['icon']}</div>
                            <div>
                                <span style='background:{color}; color:white; padding:0.2rem 0.5rem; border-radius:12px; font-size:0.7rem;'>{rec['priority']}</span>
                                <br><strong>{rec['categorie']}</strong>
                                <br><span style='color:#4a5568;'>{rec['message']}</span>
                                <br><span style='color:#667eea;'>💡 {rec['action']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ Dataset déjà propre !")

            st.markdown("### 🛠️ Feature Engineering recommandé")
            recs_fe = generer_recommandations_feature_engineering(analyse_avant)
            if recs_fe:
                for rec in recs_fe:
                    color = "#e53e3e" if rec['priority'] == 'HAUTE' else "#ed8936"
                    acp_badge = "✅ Compatible ACP" if rec.get('pour_ACP', False) else "⚠️ Non ACP"
                    st.markdown(f"""
                        <div class='timeline-item' style='border-left-color:{color};'>
                            <div class='timeline-icon'>🔧</div>
                            <div>
                                <span style='background:{color}; color:white; padding:0.2rem 0.5rem; border-radius:12px; font-size:0.7rem;'>{rec['priority']}</span>
                                <span style='margin-left:0.5rem; font-size:0.7rem;'>{acp_badge}</span>
                                <br><strong>{rec['categorie']} - {rec.get('colonne', 'Général')}</strong>
                                <br><span style='color:#4a5568;'>{rec['raison']}</span>
                                <br><span style='color:#667eea;'>💡 {rec['technique']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            if analyse_avant['classification']['a_convertir']:
                st.markdown("### 🔄 Conversions suggérées")
                for conv in analyse_avant['classification']['a_convertir']:
                    st.markdown(f"""
                        <div class='timeline-item' style='border-left-color:#ed8936;'>
                            <div class='timeline-icon'>🔄</div>
                            <div>
                                <strong>{conv['colonne']}</strong>
                                <br><span style='color:#4a5568;'>{conv['type_actuel']} → {conv['type_suggere']}</span>
                                <br><small>{conv['raison']}</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

        # --- NOUVEAU TAB : ANALYSE STATISTIQUE AVANCÉE ---
        with tab7:
            st.markdown("### 📊 Analyse statistique avancée")

            # Matrice de corrélation
            if show_correlation:
                st.markdown("#### 🔗 Matrice de corrélation")
                corr_matrix, high_corr = matrice_correlation(df_avant, corr_threshold)

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
                cols_num = df_avant.select_dtypes(include=[np.number]).columns[:10]
                if len(cols_num) > 0:
                    norm_results = test_normalite(df_avant, cols_num)
                    for res in norm_results:
                        emoji = "✅" if res['normal'] else "❌"
                        st.write(f"{emoji} **{res['colonne']}** : {res['interpretation']} (p={res['p_value']:.4f})")
                else:
                    st.info("Pas de variables numériques pour le test")

            # Profilage rapide
            if show_quick_profile:
                st.markdown("#### 📋 Profilage rapide")
                profil = profil_donnees_rapide(df_avant)

                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    st.metric("Colonnes constantes", profil['colonnes_constantes'])
                    st.metric("Colonnes uniques (ID)", profil['colonnes_uniques'])
                with col_p2:
                    st.metric("Colonnes avec manquantes", profil['colonnes_manquantes'])
                    st.metric("Total valeurs manquantes", profil['total_manquantes'])

            # Profilage complet ydata
            if show_full_profile and PROFILING_AVAILABLE:
                st.markdown("#### 📑 Profilage complet")
                if st.button("Générer le rapport complet", key="generate_full_profile"):
                    with st.spinner("Génération du rapport en cours..."):
                        profile = ProfileReport(df_avant, title="Rapport Data Quality")
                        profile.to_file("rapport_complet.html")
                        st.success("Rapport généré !")
                        with open("rapport_complet.html", "r") as f:
                            html_data = f.read()
                            st.download_button(
                                label="📥 Télécharger rapport HTML",
                                data=html_data,
                                file_name=f"rapport_complet_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                                mime="text/html"
                            )

        if analyse_apres:
            st.markdown("---")
            st.markdown("## 🔄 Comparaison Original vs Nettoyé")

            col_c1, col_c2, col_c3, col_c4 = st.columns(4)

            with col_c1:
                delta = comparaison['amelioration_score']
                delta_color = "green" if delta > 0 else "red"
                delta_symbol = "▲" if delta > 0 else "▼"
                st.metric("Score qualité", f"{analyse_apres['quality_score']:.1f}",
                          f"{delta_symbol} {abs(delta):.1f} ({comparaison['amelioration_score_pct']:.1f}%)",
                          delta_color=delta_color)

            with col_c2:
                delta = comparaison['reduction_lignes']
                st.metric("Lignes", f"{analyse_apres['total_lignes']:,}",
                          f"▼ {delta} ({comparaison['pct_reduction_lignes']:.1f}%)",
                          delta_color="green" if delta > 0 else "red")

            with col_c3:
                delta = comparaison['reduction_missing']
                st.metric("Valeurs manquantes", f"{analyse_apres['total_missing']:,}",
                          f"▼ {delta} ({comparaison['pct_reduction_missing']:.1f}%)",
                          delta_color="green" if delta > 0 else "red")

            with col_c4:
                delta = comparaison['reduction_problemes']
                delta_symbol = "▼" if delta > 0 else "▲" if delta < 0 else "="
                delta_value = f"{delta_symbol} {abs(delta)}" if delta != 0 else "="
                st.metric("Problèmes", len(analyse_apres['problem_columns']),
                          delta_value,
                          delta_color="green" if delta > 0 else "red" if delta < 0 else "gray")

            with st.expander("📋 Voir le bilan détaillé du nettoyage", expanded=False):
                messages = verifier_nettoyage(comparaison)
                for icon, color, msg in messages:
                    st.markdown(f"""
                        <div style='background:white; padding:1rem; border-radius:12px; border-left:4px solid {color}; margin-bottom:0.5rem;'>
                            <div style='display:flex; align-items:center; gap:0.5rem;'>
                                <span style='font-size:1.5rem;'>{icon}</span>
                                <span style='color:#4a5568; font-size:0.9rem;'>{msg}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                if show_problem_details and analyse_apres['problem_columns']:
                    st.markdown("### ⚠️ Problèmes restants dans le dataset nettoyé")
                    for prob in analyse_apres['problem_columns'][:5]:
                        color = "#e53e3e" if prob['severity'] > 2 else "#ed8936" if prob['severity'] > 1 else "#667eea"
                        st.markdown(f"""
                            <div class='timeline-item' style='border-left-color:{color};'>
                                <div class='timeline-icon'>⚠️</div>
                                <div>
                                    <strong style='color:{color};'>{prob['colonne']}</strong>
                                    <br><span style='color:#4a5568;'>{', '.join(prob['issues'])}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                    if len(analyse_apres['problem_columns']) > 5:
                        st.info(f"... et {len(analyse_apres['problem_columns']) - 5} autres problèmes")

            st.markdown("### 📈 Visualisation de la progression")

            fig_progress = go.Figure()

            categories = ['Score qualité', 'Lignes', 'Manquantes', 'Doublons', 'Problèmes']

            max_values = [
                100,
                max(analyse_avant['total_lignes'], analyse_apres['total_lignes']),
                max(analyse_avant['total_missing'], analyse_apres['total_missing']),
                max(analyse_avant['duplicates'], analyse_apres['duplicates']),
                max(len(analyse_avant['problem_columns']), len(analyse_apres['problem_columns']))
            ]

            avant_values = [
                analyse_avant['quality_score'],
                analyse_avant['total_lignes'],
                analyse_avant['total_missing'],
                analyse_avant['duplicates'],
                len(analyse_avant['problem_columns'])
            ]
            apres_values = [
                analyse_apres['quality_score'],
                analyse_apres['total_lignes'],
                analyse_apres['total_missing'],
                analyse_apres['duplicates'],
                len(analyse_apres['problem_columns'])
            ]

            avant_norm = [v / max_values[i] * 100 for i, v in enumerate(avant_values)]
            apres_norm = [v / max_values[i] * 100 for i, v in enumerate(apres_values)]

            fig_progress.add_trace(go.Scatterpolar(
                r=avant_norm,
                theta=categories,
                fill='toself',
                name='Original',
                line_color='#e53e3e'
            ))

            fig_progress.add_trace(go.Scatterpolar(
                r=apres_norm,
                theta=categories,
                fill='toself',
                name='Nettoyé',
                line_color='#48bb78'
            ))

            fig_progress.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                height=400
            )

            st.plotly_chart(fig_progress, width='stretch', key="plot_comparison_radar")

        # --- SECTION : GÉNÉRATION DE RAPPORT ---
        if st.session_state.generate_report:
            # Inclure la comparaison si disponible
            if analyse_apres and comparaison:
                rapport_html = generer_rapport_html(analyse_avant, comparaison, st.session_state.changes_log)
            else:
                rapport_html = generer_rapport_html(analyse_avant)

            st.download_button(
                label="📥 Télécharger rapport HTML",
                data=rapport_html,
                file_name=f"rapport_qualite_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                mime="text/html"
            )
            st.session_state.generate_report = False

        # --- SECTION : RÉSULTAT DU NETTOYAGE AUTOMATIQUE ---
        if st.session_state.df_avant_cleaned is not None:
            st.markdown("---")
            st.markdown("## 🔍 Résultat du nettoyage automatique")

            seuil, show_out, show_const = afficher_filtres_variables(analyse_avant)
            split_view_comparaison(
                st.session_state.df_avant_cleaned,
                df_avant,
                st.session_state.changes_log
            )

else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style='text-align:center; padding:3rem; background:white; border-radius:30px; box-shadow:0 20px 40px rgba(0,0,0,0.1);'>
                <span style='font-size:5rem;'>📊</span>
                <h2>Chargez un dataset pour commencer</h2>
                <p style='color:#666;'>Analyse complète · Comparaison Avant et Apres Nettoyage · Feature Engineering · ML</p>
                <div style='display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:2rem; text-align:left;'>
                    <div>✅ Statistiques globales</div><div>✅ Types de données</div>
                    <div>✅ Variables manquantes</div><div>✅ Classification auto</div>
                    <div>✅ Comparaison avant/après</div><div>✅ Feature engineering</div>
                    <div>✅ Recommandations ACP</div><div>✅ Préparation ML</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""K
    <div class='footer'>
        <strong>Data Quality Analyzer v3.0</strong> · Analyse complète pour Machine Learning · Feature Engineering · Préparation ACP · Nettoyage Automatisé<br>
        <span style='opacity: 0.6; font-size: 0.8rem;'>Développé pour l'optimisation des pipelines de données</span>
    </div>
""", unsafe_allow_html=True)