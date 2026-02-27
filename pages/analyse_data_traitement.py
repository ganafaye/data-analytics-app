import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import re
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Data Quality Analyzer | Analyse de données",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INTÉGRATION DES GOOGLE MATERIAL ICONS ---
st.markdown("""
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Outlined" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons+Sharp" rel="stylesheet">
""", unsafe_allow_html=True)


# --- FONCTION POUR LES ICÔNES GOOGLE ---
def google_icon(name, variant="outlined", size=24, color=None, gradient=False, className=""):
    """Génère une icône Google Material avec style"""
    classes = f"material-icons-{variant} {className}"
    if gradient:
        classes += " gradient-icon"

    style = f"font-size: {size}px; line-height: 1; vertical-align: middle;"
    if color and not gradient:
        style += f" color: {color};"

    return f"<span class='{classes}' style='{style}'>{name}</span>"


def icon_text(name, text, variant="outlined", size=20, color=None, spacing="8px"):
    """Combine icône et texte"""
    return f"""
    <span style='display: inline-flex; align-items: center; gap: {spacing};'>
        {google_icon(name, variant, size, color)}
        <span>{text}</span>
    </span>
    """


# --- MAPPING DES ICÔNES POUR L'APPLICATION ---
ICON_MAP = {
    # Navigation & Actions
    "dashboard": "dashboard",
    "upload": "cloud_upload",
    "download": "cloud_download",
    "save": "save",
    "delete": "delete",
    "edit": "edit",
    "refresh": "refresh",
    "search": "search",
    "filter": "filter_alt",
    "settings": "settings",
    "add": "add",
    "remove": "remove",
    "close": "close",
    "menu": "menu",

    # Analytics & Data
    "analytics": "analytics",
    "chart": "bar_chart",
    "pie_chart": "pie_chart",
    "line_chart": "show_chart",
    "table": "table_chart",
    "data": "data_usage",
    "database": "storage",
    "insights": "insights",
    "trending": "trending_up",
    "correlation": "scatter_plot",
    "distribution": "stacked_bar_chart",

    # Types de variables
    "numerical": "123",
    "categorical": "category",
    "datetime": "calendar_today",
    "text": "text_fields",
    "boolean": "check_box",
    "target": "track_changes",
    "feature": "token",
    "id": "badge",

    # Qualité des données
    "quality": "verified",
    "score": "stars",
    "excellent": "star",
    "good": "thumb_up",
    "average": "remove",
    "poor": "warning",
    "missing": "highlight_off",
    "duplicate": "content_copy",
    "outlier": "emergency",
    "error": "error",
    "warning": "warning",
    "info": "info",
    "success": "check_circle",

    # Actions de traitement
    "clean": "cleaning_services",
    "transform": "transform",
    "normalize": "straighten",
    "scale": "straighten",
    "encode": "code",
    "impute": "healing",
    "drop": "delete_sweep",
    "merge": "merge",
    "split": "split",
    "sort": "sort",
    "group": "group_work",

    # Machine Learning
    "ml": "smart_toy",
    "train": "fitness_center",
    "predict": "preview",
    "evaluate": "fact_check",
    "pca": "scatter_plot",
    "cluster": "bubble_chart",
    "classification": "category",
    "regression": "show_chart",

    # Métriques
    "rows": "table_rows",
    "columns": "view_column",
    "memory": "memory",
    "percentage": "percent",
    "count": "numbers",

    # Statuts
    "pending": "pending",
    "processing": "autorenew",
    "completed": "task_alt",
    "failed": "error",
    "paused": "pause_circle",

    # UI Elements
    "expand": "expand_more",
    "collapse": "expand_less",
    "more": "more_vert",
    "fullscreen": "fullscreen",
    "exit_fullscreen": "fullscreen_exit",
    "home": "home",
    "back": "arrow_back",
    "forward": "arrow_forward",
    "up": "arrow_upward",
    "down": "arrow_downward",

    # Fichiers
    "file": "description",
    "folder": "folder",
    "csv": "table_chart",
    "excel": "table_chart",
    "json": "data_object",
    "report": "summarize",
    "export": "file_upload",
    "import": "file_download",

    # Divers
    "calendar": "calendar_today",
    "clock": "schedule",
    "flag": "flag",
    "pin": "push_pin",
    "link": "link",
    "lock": "lock",
    "key": "key",
    "email": "email",
    "phone": "phone",
    "location": "location_on",
    "star": "star",
    "favorite": "favorite",
    "award": "emoji_events",
}

# --- STYLE CSS AMÉLIORÉ AVEC SUPPORT DES ICÔNES GOOGLE ---
st.markdown("""
    <style>
    /* Import des polices */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Style des icônes Google Material */
    .material-icons, .material-icons-outlined, .material-icons-round, .material-icons-sharp {
        font-family: 'Material Icons';
        font-weight: normal;
        font-style: normal;
        font-size: 24px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
        font-feature-settings: 'liga';
        vertical-align: middle;
        transition: all 0.3s ease;
    }

    .material-icons-outlined { font-family: 'Material Icons Outlined'; }
    .material-icons-round { font-family: 'Material Icons Round'; }
    .material-icons-sharp { font-family: 'Material Icons Sharp'; }

    /* Effet de gradient pour les icônes */
    .gradient-icon {
        background: linear-gradient(135deg, #667eea, #764ba2, #9f7aea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        background-size: 200% 200%;
        animation: gradientFlow 3s ease infinite;
    }

    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Animations pour les icônes */
    .icon-pulse {
        animation: iconPulse 2s ease infinite;
    }

    @keyframes iconPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }

    .icon-rotate {
        animation: iconRotate 2s linear infinite;
    }

    @keyframes iconRotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .icon-bounce {
        animation: iconBounce 1s ease infinite;
    }

    @keyframes iconBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }

    .icon-shake {
        animation: iconShake 0.5s ease infinite;
    }

    @keyframes iconShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-3px); }
        75% { transform: translateX(3px); }
    }

    /* Style des icônes dans les cartes */
    .metric-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 48px;
        height: 48px;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }

    .metric-icon:hover {
        transform: scale(1.1) rotate(5deg);
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
    }

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
        content: 'analytics';
        font-family: 'Material Icons';
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
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .main-subtitle {
        color: #4a5568;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 300;
        position: relative;
        z-index: 1;
        display: flex;
        align-items: center;
        gap: 8px;
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
        content: 'folder';
        font-family: 'Material Icons';
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
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
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
        display: flex;
        align-items: center;
        gap: 8px;
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
        display: inline-flex;
        align-items: center;
        gap: 6px;
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
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

    .badge-qualitative {
        background: linear-gradient(135deg, #667eea 0%, #5a67d8 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 30px;
        font-size: 0.7rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

    .badge-date {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 30px;
        font-size: 0.7rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(237, 137, 54, 0.2);
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }

    .badge-target {
        background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 30px;
        font-size: 0.7rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(229, 62, 62, 0.2);
        display: inline-flex;
        align-items: center;
        gap: 4px;
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

    .metric-icon-large {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        color: #667eea;
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
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
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

    .timeline-icon .material-icons-outlined {
        color: white;
        font-size: 24px;
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
        display: flex;
        align-items: center;
        gap: 8px;
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

    .stTabs [aria-selected="true"] .material-icons-outlined {
        color: white;
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
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
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
        display: flex;
        align-items: center;
        gap: 12px;
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
        display: flex;
        align-items: center;
        gap: 8px;
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

    </style>
""", unsafe_allow_html=True)


# --- FONCTIONS D'ANALYSE DE DONNÉES (inchangées) ---
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
            'pct_nulles': (df[col].isnull().sum() / total_lignes) * 100,
            'uniques': df[col].nunique(),
            'pct_uniques': (df[col].nunique() / total_lignes) * 100
        }

        if col in classification['quantitative']:
            stats['min'] = df[col].min()
            stats['max'] = df[col].max()
            stats['mean'] = df[col].mean()
            stats['std'] = df[col].std()
            stats['skew'] = df[col].skew()

            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
            stats['outliers'] = outliers
            stats['pct_outliers'] = (outliers / total_lignes) * 100

        col_stats.append(stats)

    missing_values = df.isnull().sum()
    missing_cols = missing_values[missing_values > 0]
    total_missing = missing_values.sum()
    pct_missing = (total_missing / (total_lignes * total_colonnes)) * 100

    duplicates = df.duplicated().sum()
    pct_duplicates = (duplicates / total_lignes) * 100

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
        if df[stats['nom']].apply(type).nunique() > 1:
            issues.append("Types mixtes")
        if 'outliers' in stats and stats['pct_outliers'] > 5:
            issues.append(f"{stats['pct_outliers']:.1f}% outliers")
        if 'skew' in stats and abs(stats['skew']) > 1:
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
        messages.append(
            ("check_circle", "#10b981", f"Score qualité amélioré de {comparaison['amelioration_score']:.1f} points"))
    else:
        messages.append(("error", "#ef4444", "Le score qualité n'a pas augmenté"))

    if comparaison['reduction_missing'] > 0:
        messages.append(
            ("check_circle", "#10b981", f"Valeurs manquantes réduites de {comparaison['reduction_missing']}"))
    elif comparaison['reduction_missing'] < 0:
        messages.append(
            ("warning", "#f59e0b", f"Nouvelles valeurs manquantes: {abs(comparaison['reduction_missing'])}"))

    if comparaison['reduction_duplicates'] > 0:
        messages.append(("check_circle", "#10b981", f"Doublons réduits de {comparaison['reduction_duplicates']}"))

    if comparaison['reduction_problemes'] > 0:
        messages.append(("check_circle", "#10b981", f"Problèmes résolus: {comparaison['reduction_problemes']}"))
    elif comparaison['reduction_problemes'] < 0:
        messages.append(("error", "#ef4444", f"Nouveaux problèmes: {abs(comparaison['reduction_problemes'])}"))

    return messages


def generer_recommandations_feature_engineering(analyse):
    recommandations = []
    if analyse['classification']['quantitative']:
        for col in analyse['classification']['quantitative'][:5]:
            stats = next((s for s in analyse['col_stats'] if s['nom'] == col), None)
            if stats:
                if stats['std'] > 10:
                    recommandations.append({
                        'type': 'feature_engineering',
                        'categorie': 'Normalisation',
                        'colonne': col,
                        'technique': 'StandardScaler ou MinMaxScaler',
                        'raison': f"Grande échelle (std={stats['std']:.2f})",
                        'impact': 'Améliore la convergence des modèles',
                        'pour_ACP': True,
                        'priority': 'MOYENNE',
                        'icon': 'straighten'
                    })

                if 'pct_outliers' in stats and stats['pct_outliers'] > 5:
                    recommandations.append({
                        'type': 'feature_engineering',
                        'categorie': 'Outliers',
                        'colonne': col,
                        'technique': 'Winsorisation ou transformation logarithmique',
                        'raison': f"{stats['pct_outliers']:.1f}% d'outliers",
                        'impact': 'Réduit l\'influence des valeurs extrêmes',
                        'pour_ACP': True,
                        'priority': 'MOYENNE',
                        'icon': 'emergency'
                    })

                if 'skew' in stats and abs(stats['skew']) > 1:
                    transformation = 'log' if stats['skew'] > 1 else 'square' if stats['skew'] < -1 else 'box-cox'
                    recommandations.append({
                        'type': 'feature_engineering',
                        'categorie': 'Transformation',
                        'colonne': col,
                        'technique': f'Transformation {transformation}',
                        'raison': f"Asymétrie = {stats['skew']:.2f}",
                        'impact': 'Rend la distribution plus normale',
                        'pour_ACP': True,
                        'priority': 'MOYENNE',
                        'icon': 'show_chart'
                    })

    if len(analyse['classification']['quantitative']) >= 3:
        recommandations.append({
            'type': 'acp',
            'categorie': 'ACP',
            'technique': 'Analyse en Composantes Principales',
            'raison': f"{len(analyse['classification']['quantitative'])} variables quantitatives",
            'impact': 'Réduit la dimension et décorrèle les variables',
            'variables': analyse['classification']['quantitative'][:5],
            'priority': 'HAUTE',
            'icon': 'scatter_plot'
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
            'icon': 'highlight_off'
        })

    if analyse['pct_duplicates'] > 1:
        recommandations.append({
            'priority': 'HAUTE' if analyse['pct_duplicates'] > 5 else 'MOYENNE',
            'categorie': 'Doublons',
            'message': f"{analyse['duplicates']} lignes dupliquées ({analyse['pct_duplicates']:.1f}%)",
            'action': "Supprimer les lignes dupliquées",
            'icon': 'content_copy'
        })

    for prob in analyse['problem_columns']:
        for issue in prob['issues']:
            if 'manquantes' in issue:
                recommandations.append({
                    'priority': 'MOYENNE',
                    'categorie': f"Colonne '{prob['colonne']}'",
                    'message': issue,
                    'action': f"Traiter les valeurs manquantes",
                    'icon': 'warning'
                })
            elif 'Constante' in issue:
                recommandations.append({
                    'priority': 'BASSE',
                    'categorie': f"Colonne '{prob['colonne']}'",
                    'message': "Colonne constante",
                    'action': f"Envisager de supprimer",
                    'icon': 'remove'
                })
            elif 'outliers' in issue:
                recommandations.append({
                    'priority': 'MOYENNE',
                    'categorie': f"Colonne '{prob['colonne']}'",
                    'message': issue,
                    'action': "Appliquer une transformation ou winsorisation",
                    'icon': 'emergency'
                })
            elif 'Asymétrie' in issue:
                recommandations.append({
                    'priority': 'MOYENNE',
                    'categorie': f"Colonne '{prob['colonne']}'",
                    'message': issue,
                    'action': "Appliquer une transformation logarithmique",
                    'icon': 'show_chart'
                })

    return recommandations


# --- EN-TÊTE PRINCIPAL AVEC ICÔNES GOOGLE ---
st.markdown(f"""
    <div class="main-header floating shine">
        <h1 class="main-title">
            {google_icon('analytics', variant='sharp', size=40, gradient=True)}
            Data Quality Analyzer
        </h1>
        <p class="main-subtitle">
            {google_icon('insights', size=20, color='#667eea')}
            Analyse intelligente de la qualité des données · Nettoyage & Optimisation · Feature Engineering
        </p>
        <div style='display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap;'>
            <span class='badge-excellent quality-badge'>
                {google_icon('category', size=16)} Classification auto
            </span>
            <span class='badge-good quality-badge'>
                {google_icon('build', size=16)} Feature engineering
            </span>
            <span class='badge-fair quality-badge'>
                {google_icon('scatter_plot', size=16)} Préparation ACP
            </span>
            <span class='badge-poor quality-badge'>
                {google_icon('lightbulb', size=16)} Recommandations ML
            </span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR AVEC ICÔNES GOOGLE ---
with st.sidebar:
    st.markdown(f"""
        <div class="sidebar-header">
            <h3>
                {google_icon('folder_open', variant='sharp', size=32, gradient=True)}
                Chargement
            </h3>
            <p>Importez vos datasets</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"{google_icon('cloud_upload', size=20)} **Dataset original**", unsafe_allow_html=True)
    file_avant = st.file_uploader(
        "Charger le fichier original (obligatoire)",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'pkl', 'txt'],
        key="file_avant",
        help="Dataset avant nettoyage",
        label_visibility="collapsed"
    )

    if file_avant:
        type_fichier = detecter_type_fichier(file_avant.name)
        icon_name = 'table_chart' if type_fichier in ['CSV',
                                                      'Excel'] else 'data_object' if type_fichier == 'JSON' else 'description'
        st.info(f"{google_icon(icon_name, size=18)} Original : {type_fichier}", icon="📄")

    st.markdown("---")

    st.markdown(f"{google_icon('auto_awesome', size=20)} **Dataset nettoyé**", unsafe_allow_html=True)
    file_apres = st.file_uploader(
        "Charger la version nettoyée (optionnel)",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'pkl', 'txt'],
        key="file_apres",
        help="Version nettoyée à comparer avec l'original",
        label_visibility="collapsed"
    )

    if file_apres:
        type_fichier = detecter_type_fichier(file_apres.name)
        icon_name = 'table_chart' if type_fichier in ['CSV',
                                                      'Excel'] else 'data_object' if type_fichier == 'JSON' else 'description'
        st.info(f"{google_icon(icon_name, size=18)} Nettoyé : {type_fichier}", icon="✨")

    st.markdown("---")

    st.markdown(f"{google_icon('settings', size=20)} **Options**", unsafe_allow_html=True)
    show_details = st.checkbox("Afficher les détails par colonne", value=True)
    threshold_missing = st.slider("Seuil d'alerte valeurs manquantes (%)", 0, 50, 10)
    show_problem_details = st.checkbox("Afficher les détails des problèmes", value=True)

if file_avant:
    df_avant, error_avant = charger_fichier(file_avant)

    if error_avant:
        st.error(f"{google_icon('error', size=20)} Erreur chargement original : {error_avant}", icon="🚨")
    else:
        with st.spinner(f"{google_icon('autorenew', size=20, className='icon-rotate')} Analyse du dataset original..."):
            analyse_avant = analyser_qualite_dataset(df_avant, "Original")

        if file_apres:
            df_apres, error_apres = charger_fichier(file_apres)
            if error_apres:
                st.error(f"{google_icon('error', size=20)} Erreur chargement nettoyé : {error_apres}", icon="🚨")
                df_apres = None
                analyse_apres = None
                comparaison = None
            else:
                with st.spinner(
                        f"{google_icon('autorenew', size=20, className='icon-rotate')} Analyse du dataset nettoyé..."):
                    analyse_apres = analyser_qualite_dataset(df_apres, "Nettoyé")
                comparaison = comparer_datasets(analyse_avant, analyse_apres)
        else:
            df_apres = None
            analyse_apres = None
            comparaison = None

        st.markdown(f"## {google_icon('dashboard', size=28)} Dataset Original - Tableau de bord qualité",
                    unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
                <div class='quality-card'>
                    <div style='display: flex; align-items: center; gap: 16px;'>
                        <div class='metric-icon'>{google_icon('stars', size=32, gradient=True)}</div>
                        <div>
                            <div class='quality-score'>{analyse_avant['quality_score']:.1f}</div>
                            <div class='quality-label'>Score qualité</div>
                        </div>
                    </div>
                    <div style='margin-top:1rem;'>
                        <span class='quality-badge {analyse_avant['quality_badge']}'>
                            {google_icon('check', size=16)} {analyse_avant['quality_category']}
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-icon-large'>{google_icon('table_rows', size=40, color='#667eea')}</div>
                    <div class='metric-value-sm'>{analyse_avant['total_lignes']:,}</div>
                    <div class='metric-label-sm'>{google_icon('table_rows', size=16)} Lignes</div>
                    <div class='progress-container'><div class='progress-bar' style='width:100%'></div></div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-icon-large'>{google_icon('view_column', size=40, color='#667eea')}</div>
                    <div class='metric-value-sm'>{analyse_avant['total_colonnes']}</div>
                    <div class='metric-label-sm'>{google_icon('view_column', size=16)} Colonnes</div>
                    <div class='progress-container'><div class='progress-bar' style='width:100%'></div></div>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-icon-large'>{google_icon('memory', size=40, color='#667eea')}</div>
                    <div class='metric-value-sm'>{analyse_avant['memoire']:.2f}</div>
                    <div class='metric-label-sm'>{google_icon('memory', size=16)} MB</div>
                    <div class='progress-container'><div class='progress-bar' style='width:{min(100, analyse_avant['memoire'])}%'></div></div>
                </div>
            """, unsafe_allow_html=True)

        # Création des onglets avec icônes
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            f"{google_icon('table_view', size=18)} Aperçu général",
            f"{google_icon('category', size=18)} Classification",
            f"{google_icon('view_column', size=18)} Détails",
            f"{google_icon('warning', size=18)} Problèmes",
            f"{google_icon('insights', size=18)} Visualisations",
            f"{google_icon('lightbulb', size=18)} Recommandations"
        ])

        with tab1:
            st.markdown('<div class="quality-card">', unsafe_allow_html=True)
            col_stat1, col_stat2 = st.columns(2)

            with col_stat1:
                st.markdown(f"### {google_icon('analytics', size=24)} Statistiques globales", unsafe_allow_html=True)
                st.markdown(f"""
                    * {google_icon('table_rows', size=16)} **Lignes :** {analyse_avant['total_lignes']:,}
                    * {google_icon('view_column', size=16)} **Colonnes :** {analyse_avant['total_colonnes']}
                    * {google_icon('memory', size=16)} **Mémoire :** {analyse_avant['memoire']:.2f} MB
                    * {google_icon('highlight_off', size=16)} **Valeurs manquantes :** {analyse_avant['total_missing']:,} ({analyse_avant['pct_missing']:.1f}%)
                    * {google_icon('content_copy', size=16)} **Lignes dupliquées :** {analyse_avant['duplicates']:,} ({analyse_avant['pct_duplicates']:.1f}%)
                """, unsafe_allow_html=True)

            with col_stat2:
                st.markdown(f"### {google_icon('data_usage', size=24)} Types de données", unsafe_allow_html=True)
                for dtype, count in analyse_avant['dtypes_summary'].items():
                    pct = (count / analyse_avant['total_colonnes']) * 100
                    st.markdown(f"""
                        * {google_icon('code', size=16)} **{dtype} :** {count} ({pct:.1f}%)
                        <div class='progress-container'><div class='progress-bar' style='width:{pct}%'></div></div>
                    """, unsafe_allow_html=True)

            if analyse_avant['missing_cols']:
                st.markdown(f"### {google_icon('warning', size=24, color='#e53e3e')} Colonnes avec valeurs manquantes",
                            unsafe_allow_html=True)
                for col, count in list(analyse_avant['missing_cols'].items())[:10]:
                    pct = (count / analyse_avant['total_lignes']) * 100
                    color = "#e53e3e" if pct > threshold_missing else "#ed8936"
                    st.markdown(f"""
                        * {google_icon('highlight_off', size=16, color=color)} **{col} :** {count:,} ({pct:.1f}%)
                        <div class='progress-container'><div class='progress-bar' style='width:{pct}%; background:{color};'></div></div>
                    """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            col_var1, col_var2 = st.columns(2)

            with col_var1:
                st.markdown('<div class="quality-card">', unsafe_allow_html=True)
                st.markdown(f"### {google_icon('123', size=24)} Variables Quantitatives", unsafe_allow_html=True)
                if analyse_avant['classification']['quantitative']:
                    st.markdown(f"**{len(analyse_avant['classification']['quantitative'])} variables**")
                    for col in analyse_avant['classification']['quantitative'][:10]:
                        stats = next((s for s in analyse_avant['col_stats'] if s['nom'] == col), None)
                        outliers = f" · {stats['pct_outliers']:.1f}% outliers" if stats and 'pct_outliers' in stats else ""
                        st.markdown(f"""
                            <div class='variable-item'>
                                <div class='variable-name'>
                                    {google_icon('123', size=16, color='#48bb78')} {col}
                                    <span class='badge-quantitative'>{google_icon('123', size=12)} QN</span>
                                </div>
                                <div class='variable-stats'>
                                    {stats['uniques']} valeurs · min={stats['min']:.1f} · max={stats['max']:.1f}{outliers}
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
                st.markdown(f"### {google_icon('category', size=24)} Variables Qualitatives", unsafe_allow_html=True)
                if analyse_avant['classification']['qualitative']:
                    st.markdown(f"**{len(analyse_avant['classification']['qualitative'])} variables**")
                    for col in analyse_avant['classification']['qualitative'][:10]:
                        stats = next((s for s in analyse_avant['col_stats'] if s['nom'] == col), None)
                        st.markdown(f"""
                            <div class='variable-item'>
                                <div class='variable-name'>
                                    {google_icon('category', size=16, color='#667eea')} {col}
                                    <span class='badge-qualitative'>{google_icon('category', size=12)} QL</span>
                                </div>
                                <div class='variable-stats'>
                                    {stats['uniques']} catégories · {stats['non_nulles']} non-nulles
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
                st.markdown(f"### {google_icon('calendar_today', size=24)} Variables Date", unsafe_allow_html=True)
                for col in analyse_avant['classification']['dates']:
                    st.markdown(f"""
                        <div class='variable-item'>
                            <div class='variable-name'>
                                {google_icon('calendar_today', size=16, color='#ed8936')} {col}
                                <span class='badge-date'>{google_icon('calendar_today', size=12)} Date</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            if analyse_avant['classification']['target_potential']:
                st.markdown('<div class="quality-card">', unsafe_allow_html=True)
                st.markdown(f"### {google_icon('track_changes', size=24)} Cibles potentielles ML",
                            unsafe_allow_html=True)
                for target in analyse_avant['classification']['target_potential']:
                    st.markdown(f"""
                        <div class='variable-item'>
                            <div class='variable-name'>
                                {google_icon('track_changes', size=16, color='#e53e3e')} {target['colonne']}
                                <span class='badge-target'>{google_icon('flag', size=12)} {target['type']}</span>
                            </div>
                            <div class='variable-stats'>{target['raison']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            if show_details:
                for stats in analyse_avant['col_stats'][:20]:
                    icon_name = '123' if stats['classification'] == 'quantitative' else 'category' if stats[
                                                                                                          'classification'] == 'qualitative' else 'calendar_today'
                    with st.expander(f"{google_icon(icon_name, size=20)} {stats['nom']} ({stats['type']})"):
                        col_d1, col_d2, col_d3 = st.columns(3)

                        with col_d1:
                            st.metric("Non-nulles", f"{stats['non_nulles']:,}")
                            st.metric("Nulles", f"{stats['nulles']:,} ({stats['pct_nulles']:.1f}%)")

                        with col_d2:
                            st.metric("Valeurs uniques", f"{stats['uniques']:,}")
                            st.metric("Taux unicité", f"{stats['pct_uniques']:.1f}%")

                        with col_d3:
                            if 'min' in stats:
                                st.metric("Min", f"{stats['min']:.2f}")
                                st.metric("Max", f"{stats['max']:.2f}")
                                st.metric("Moyenne", f"{stats['mean']:.2f}")
                                if 'outliers' in stats:
                                    st.metric("Outliers", f"{stats['outliers']} ({stats['pct_outliers']:.1f}%)")

        with tab4:
            if analyse_avant['problem_columns']:
                if show_problem_details:
                    for prob in analyse_avant['problem_columns']:
                        color = "#e53e3e" if prob['severity'] > 2 else "#ed8936" if prob['severity'] > 1 else "#667eea"
                        st.markdown(f"""
                            <div class='timeline-item' style='border-left-color:{color};'>
                                <div class='timeline-icon'>{google_icon('warning', size=24, color='white')}</div>
                                <div>
                                    <strong style='color:{color};'>{prob['colonne']}</strong>
                                    <br><span style='color:#4a5568;'>{', '.join(prob['issues'])}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info(
                        f"{google_icon('info', size=20)} {len(analyse_avant['problem_columns'])} problèmes détectés (masqués)",
                        icon="ℹ️")
            else:
                st.success(f"{google_icon('check_circle', size=20)} Aucun problème détecté !", icon="✅")

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
            st.markdown(f"### {google_icon('cleaning_services', size=24)} Recommandations de nettoyage",
                        unsafe_allow_html=True)
            recs_qualite = generer_recommandations_qualite(analyse_avant)
            if recs_qualite:
                for rec in recs_qualite:
                    color = "#e53e3e" if rec['priority'] == 'HAUTE' else "#ed8936" if rec[
                                                                                          'priority'] == 'MOYENNE' else "#667eea"
                    st.markdown(f"""
                        <div class='timeline-item' style='border-left-color:{color};'>
                            <div class='timeline-icon'>{google_icon(rec['icon'], size=24, color='white')}</div>
                            <div>
                                <span style='background:{color}; color:white; padding:0.2rem 0.5rem; border-radius:12px; font-size:0.7rem; display:inline-flex; align-items:center; gap:4px;'>
                                    {google_icon('priority_high', size=12)} {rec['priority']}
                                </span>
                                <br><strong>{rec['categorie']}</strong>
                                <br><span style='color:#4a5568;'>{rec['message']}</span>
                                <br><span style='color:#667eea; display:flex; align-items:center; gap:4px;'>
                                    {google_icon('lightbulb', size=16)} {rec['action']}
                                </span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.success(f"{google_icon('check_circle', size=20)} Dataset déjà propre !", icon="✅")

            st.markdown(f"### {google_icon('build', size=24)} Feature Engineering recommandé", unsafe_allow_html=True)
            recs_fe = generer_recommandations_feature_engineering(analyse_avant)
            if recs_fe:
                for rec in recs_fe:
                    color = "#e53e3e" if rec['priority'] == 'HAUTE' else "#ed8936"
                    acp_badge = f"{google_icon('check_circle', size=12)} Compatible ACP" if rec.get('pour_ACP',
                                                                                                    False) else f"{google_icon('warning', size=12)} Non ACP"
                    st.markdown(f"""
                        <div class='timeline-item' style='border-left-color:{color};'>
                            <div class='timeline-icon'>{google_icon(rec.get('icon', 'build'), size=24, color='white')}</div>
                            <div>
                                <span style='background:{color}; color:white; padding:0.2rem 0.5rem; border-radius:12px; font-size:0.7rem; display:inline-flex; align-items:center; gap:4px;'>
                                    {google_icon('priority_high', size=12)} {rec['priority']}
                                </span>
                                <span style='margin-left:0.5rem; font-size:0.7rem; display:inline-flex; align-items:center; gap:4px;'>
                                    {google_icon('check_circle' if rec.get('pour_ACP', False) else 'warning', size=12)} {acp_badge}
                                </span>
                                <br><strong>{rec['categorie']} - {rec.get('colonne', 'Général')}</strong>
                                <br><span style='color:#4a5568;'>{rec['raison']}</span>
                                <br><span style='color:#667eea; display:flex; align-items:center; gap:4px;'>
                                    {google_icon('lightbulb', size=16)} {rec['technique']}
                                </span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            if analyse_avant['classification']['a_convertir']:
                st.markdown(f"### {google_icon('transform', size=24)} Conversions suggérées", unsafe_allow_html=True)
                for conv in analyse_avant['classification']['a_convertir']:
                    st.markdown(f"""
                        <div class='timeline-item' style='border-left-color:#ed8936;'>
                            <div class='timeline-icon'>{google_icon('transform', size=24, color='white')}</div>
                            <div>
                                <strong>{conv['colonne']}</strong>
                                <br><span style='color:#4a5568;'>{conv['type_actuel']} → {conv['type_suggere']}</span>
                                <br><small>{conv['raison']}</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

        if analyse_apres:
            st.markdown("---")
            st.markdown(f"## {google_icon('compare_arrows', size=28)} Comparaison Original vs Nettoyé",
                        unsafe_allow_html=True)

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

            with st.expander(f"{google_icon('summarize', size=20)} Voir le bilan détaillé du nettoyage",
                             expanded=False):
                messages = verifier_nettoyage(comparaison)
                for icon_name, color, msg in messages:
                    st.markdown(f"""
                        <div style='background:white; padding:1rem; border-radius:12px; border-left:4px solid {color}; margin-bottom:0.5rem;'>
                            <div style='display:flex; align-items:center; gap:0.5rem;'>
                                {google_icon(icon_name, size=24, color=color)}
                                <span style='color:#4a5568; font-size:0.9rem;'>{msg}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                if show_problem_details and analyse_apres['problem_columns']:
                    st.markdown(f"### {google_icon('warning', size=20)} Problèmes restants dans le dataset nettoyé",
                                unsafe_allow_html=True)
                    for prob in analyse_apres['problem_columns'][:5]:
                        color = "#e53e3e" if prob['severity'] > 2 else "#ed8936" if prob['severity'] > 1 else "#667eea"
                        st.markdown(f"""
                            <div class='timeline-item' style='border-left-color:{color};'>
                                <div class='timeline-icon'>{google_icon('warning', size=24, color='white')}</div>
                                <div>
                                    <strong style='color:{color};'>{prob['colonne']}</strong>
                                    <br><span style='color:#4a5568;'>{', '.join(prob['issues'])}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                    if len(analyse_apres['problem_columns']) > 5:
                        st.info(f"... et {len(analyse_apres['problem_columns']) - 5} autres problèmes")

            st.markdown(f"### {google_icon('insights', size=24)} Visualisation de la progression",
                        unsafe_allow_html=True)

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

else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div style='text-align:center; padding:3rem; background:white; border-radius:30px; box-shadow:0 20px 40px rgba(0,0,0,0.1);'>
                <div style='font-size:5rem; margin-bottom:1rem;'>{google_icon('analytics', size=80, gradient=True)}</div>
                <h2>Chargez un dataset pour commencer</h2>
                <p style='color:#666;'>Analyse complète · Nettoyage · Feature Engineering · ML</p>
                <div style='display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:2rem; text-align:left;'>
                    <div>{google_icon('check_circle', size=16, color='#48bb78')} Statistiques globales</div>
                    <div>{google_icon('check_circle', size=16, color='#48bb78')} Types de données</div>
                    <div>{google_icon('check_circle', size=16, color='#48bb78')} Variables manquantes</div>
                    <div>{google_icon('check_circle', size=16, color='#48bb78')} Classification auto</div>
                    <div>{google_icon('check_circle', size=16, color='#48bb78')} Comparaison avant/après</div>
                    <div>{google_icon('check_circle', size=16, color='#48bb78')} Feature engineering</div>
                    <div>{google_icon('check_circle', size=16, color='#48bb78')} Recommandations ACP</div>
                    <div>{google_icon('check_circle', size=16, color='#48bb78')} Préparation ML</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown(f"""
    <div class='footer'>
        <strong>Data Quality Analyzer v2.0</strong> · Analyse complète pour Machine Learning · Feature Engineering · Préparation ACP<br>
        <span style='opacity: 0.6; font-size: 0.8rem; display: flex; align-items: center; justify-content: center; gap: 4px;'>
            {google_icon('code', size=14)} Développé pour l'optimisation des pipelines de données
        </span>
    </div>
""", unsafe_allow_html=True)