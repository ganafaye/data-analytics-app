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
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS MINIMALISTE ---
st.markdown("""
    <style>
    /* Import des polices */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Style général */
    .main {
        background: #f8fafc;
        font-family: 'Inter', sans-serif;
    }

    /* En-tête principal minimaliste */
    .main-header {
        background: white;
        padding: 2rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
        border: 1px solid #e2e8f0;
    }

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e293b;
        margin: 0;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main-subtitle {
        color: #64748b;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }

    /* Badges minimalistes */
    .badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 500;
        background: #f1f5f9;
        color: #334155;
        border: 1px solid #e2e8f0;
        margin-right: 0.5rem;
    }

    /* Sidebar minimaliste */
    section[data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid #e2e8f0;
    }

    .sidebar-header {
        padding: 1.5rem;
        border-bottom: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }

    .sidebar-header h3 {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0;
    }

    .sidebar-header p {
        color: #64748b;
        font-size: 0.85rem;
        margin: 0.2rem 0 0 0;
    }

    .sidebar-section {
        padding: 0 1rem;
        margin-bottom: 1.5rem;
    }

    .sidebar-section-title {
        font-size: 0.9rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.8rem;
    }

    /* File uploader minimaliste */
    .stFileUploader {
        border: 1px dashed #cbd5e1;
        border-radius: 12px;
        padding: 0.5rem;
        background: #f8fafc;
    }

    .stFileUploader:hover {
        border-color: #4361ee;
    }

    /* Cartes minimalistes */
    .quality-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }

    .quality-score {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e293b;
        line-height: 1;
    }

    .quality-label {
        color: #64748b;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Badges qualité */
    .quality-badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    .badge-excellent {
        background: #10b981;
        color: white;
    }

    .badge-good {
        background: #4361ee;
        color: white;
    }

    .badge-fair {
        background: #f97316;
        color: white;
    }

    .badge-poor {
        background: #ef4444;
        color: white;
    }

    /* Badges pour types de variables */
    .badge-quantitative {
        background: #10b981;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.7rem;
    }

    .badge-qualitative {
        background: #4361ee;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.7rem;
    }

    .badge-date {
        background: #f97316;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.7rem;
    }

    .badge-target {
        background: #ef4444;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.7rem;
    }

    /* Cartes métriques */
    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1e293b;
    }

    .metric-label {
        color: #64748b;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.3rem;
    }

    /* Timeline minimaliste */
    .timeline-item {
        display: flex;
        align-items: center;
        padding: 1rem;
        background: #f8fafc;
        border-radius: 12px;
        margin-bottom: 0.8rem;
        border-left: 3px solid #4361ee;
    }

    .timeline-icon {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #e2e8f0;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-size: 1rem;
        color: #4361ee;
    }

    /* Progress bars */
    .progress-container {
        background: #e2e8f0;
        height: 6px;
        border-radius: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }

    .progress-bar {
        height: 100%;
        background: #4361ee;
        border-radius: 10px;
    }

    /* Variables grid */
    .variable-item {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 0.5rem;
    }

    .variable-name {
        font-weight: 600;
        color: #1e293b;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.3rem;
    }

    .variable-stats {
        font-size: 0.8rem;
        color: #64748b;
    }

    /* Tabs minimalistes */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: transparent;
        padding: 0;
        border-bottom: 1px solid #e2e8f0;
        border-radius: 0;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 0.7rem 1.2rem;
        font-weight: 500;
        color: #64748b;
        border-bottom: 2px solid transparent;
    }

    .stTabs [aria-selected="true"] {
        color: #4361ee;
        border-bottom: 2px solid #4361ee;
    }

    /* Boutons minimalistes */
    .stButton > button {
        background: white;
        color: #4361ee;
        border: 1px solid #4361ee;
        border-radius: 30px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: #4361ee;
        color: white;
    }

    /* Footer minimaliste */
    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        color: #64748b;
        font-size: 0.85rem;
        border-top: 1px solid #e2e8f0;
    }

    /* Page de chargement */
    .upload-prompt {
        text-align: center;
        padding: 3rem;
        background: white;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
    }

    .upload-prompt h2 {
        color: #1e293b;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
    }

    .upload-prompt p {
        color: #64748b;
        font-size: 0.95rem;
    }

    .feature-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.8rem;
        margin-top: 2rem;
        text-align: left;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    .feature-item {
        color: #1e293b;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .feature-item::before {
        content: "✓";
        color: #10b981;
        font-weight: bold;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.8rem;
        }

        .main-header {
            padding: 1.5rem;
        }
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
        quality_color = "#10b981"
        quality_badge = "badge-excellent"
    elif quality_score >= 75:
        quality_category = "BON"
        quality_color = "#4361ee"
        quality_badge = "badge-good"
    elif quality_score >= 50:
        quality_category = "MOYEN"
        quality_color = "#f97316"
        quality_badge = "badge-fair"
    else:
        quality_category = "FAIBLE"
        quality_color = "#ef4444"
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
                        'priority': 'MOYENNE'
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
                        'priority': 'MOYENNE'
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


# --- EN-TÊTE PRINCIPAL MINIMALISTE ---
st.markdown("""
    <div class="main-header">
        <h1 class="main-title">Data Quality Analyzer</h1>
        <p class="main-subtitle">Analyse intelligente de la qualité des données • Nettoyage & Optimisation</p>
        <div style='display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap;'>
            <span class='badge'>🎯 Classification auto</span>
            <span class='badge'>📊 Feature engineering</span>
            <span class='badge'>🔬 Préparation ACP</span>
            <span class='badge'>💡 Recommandations ML</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR MINIMALISTE ---
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <h3>Analytics Hub</h3>
            <p>Navigation et chargement</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">NAVIGATION</div>
    """, unsafe_allow_html=True)

    if st.button("🏠 Accueil", use_container_width=True):
        st.switch_page("home_page.py")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">CHARGEMENT</div>
    """, unsafe_allow_html=True)

    st.markdown("##### Dataset original")
    file_avant = st.file_uploader(
        "Charger le fichier original",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'pkl', 'txt'],
        key="file_avant",
        label_visibility="collapsed"
    )

    if file_avant:
        type_fichier = detecter_type_fichier(file_avant.name)
        st.caption(f"📄 {type_fichier} • {file_avant.size / 1024:.1f} KB")

    st.markdown("##### Dataset nettoyé")
    file_apres = st.file_uploader(
        "Charger la version nettoyée",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'pkl', 'txt'],
        key="file_apres",
        label_visibility="collapsed"
    )

    if file_apres:
        type_fichier = detecter_type_fichier(file_apres.name)
        st.caption(f"📄 {type_fichier} • {file_apres.size / 1024:.1f} KB")

    st.markdown("Limit 200MB per file • CSV, XLSX", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="sidebar-section">
            <div class="sidebar-section-title">OPTIONS</div>
    """, unsafe_allow_html=True)

    show_details = st.checkbox("Afficher les détails par colonne", value=True)
    threshold_missing = st.slider("Seuil valeurs manquantes (%)", 0, 50, 10)
    show_problem_details = st.checkbox("Afficher les problèmes", value=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --- CORPS PRINCIPAL ---
if file_avant:
    df_avant, error_avant = charger_fichier(file_avant)

    if error_avant:
        st.error(f"Erreur : {error_avant}")
    else:
        with st.spinner("Analyse en cours..."):
            analyse_avant = analyser_qualite_dataset(df_avant, "Original")

        if file_apres:
            df_apres, error_apres = charger_fichier(file_apres)
            if error_apres:
                st.error(f"Erreur : {error_apres}")
                df_apres = None
                analyse_apres = None
                comparaison = None
            else:
                with st.spinner("Analyse en cours..."):
                    analyse_apres = analyser_qualite_dataset(df_apres, "Nettoyé")
                comparaison = comparer_datasets(analyse_avant, analyse_apres)
        else:
            df_apres = None
            analyse_apres = None
            comparaison = None

        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
                <div class='quality-card'>
                    <div class='quality-score'>{analyse_avant['quality_score']:.1f}</div>
                    <div class='quality-label'>Score qualité</div>
                    <div style='margin-top:0.8rem;'>
                        <span class='quality-badge {analyse_avant['quality_badge']}'>
                            {analyse_avant['quality_category']}
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{analyse_avant['total_lignes']:,}</div>
                    <div class='metric-label'>Lignes</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{analyse_avant['total_colonnes']}</div>
                    <div class='metric-label'>Colonnes</div>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
                <div class='metric-card'>
                    <div class='metric-value'>{analyse_avant['memoire']:.2f}</div>
                    <div class='metric-label'>MB</div>
                </div>
            """, unsafe_allow_html=True)

        # Onglets
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📋 Aperçu",
            "🔢 Variables",
            "🔍 Détails",
            "⚠️ Problèmes",
            "📈 Visualisations",
            "💡 Recommandations"
        ])

        with tab1:
            st.markdown('<div class="quality-card">', unsafe_allow_html=True)

            col_stat1, col_stat2 = st.columns(2)

            with col_stat1:
                st.markdown("##### Statistiques globales")
                st.markdown(f"""
                    • **Lignes :** {analyse_avant['total_lignes']:,}
                    • **Colonnes :** {analyse_avant['total_colonnes']}
                    • **Mémoire :** {analyse_avant['memoire']:.2f} MB
                    • **Valeurs manquantes :** {analyse_avant['total_missing']:,} ({analyse_avant['pct_missing']:.1f}%)
                    • **Lignes dupliquées :** {analyse_avant['duplicates']:,} ({analyse_avant['pct_duplicates']:.1f}%)
                """)

            with col_stat2:
                st.markdown("##### Types de données")
                for dtype, count in analyse_avant['dtypes_summary'].items():
                    pct = (count / analyse_avant['total_colonnes']) * 100
                    st.markdown(f"""
                        • **{dtype} :** {count} ({pct:.1f}%)
                        <div class='progress-container'><div class='progress-bar' style='width:{pct}%'></div></div>
                    """, unsafe_allow_html=True)

            if analyse_avant['missing_cols']:
                st.markdown("##### Colonnes avec valeurs manquantes")
                for col, count in list(analyse_avant['missing_cols'].items())[:10]:
                    pct = (count / analyse_avant['total_lignes']) * 100
                    color = "#ef4444" if pct > threshold_missing else "#f97316"
                    st.markdown(f"""
                        • **{col} :** {count:,} ({pct:.1f}%)
                        <div class='progress-container'><div class='progress-bar' style='width:{pct}%; background:{color};'></div></div>
                    """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            col_var1, col_var2 = st.columns(2)

            with col_var1:
                st.markdown('<div class="quality-card">', unsafe_allow_html=True)
                st.markdown("##### Variables Quantitatives")
                if analyse_avant['classification']['quantitative']:
                    for col in analyse_avant['classification']['quantitative'][:10]:
                        stats = next((s for s in analyse_avant['col_stats'] if s['nom'] == col), None)
                        outliers = f" • {stats['pct_outliers']:.1f}% outliers" if stats and 'pct_outliers' in stats else ""
                        st.markdown(f"""
                            <div class='variable-item'>
                                <div class='variable-name'>
                                    {col}
                                    <span class='badge-quantitative'>QN</span>
                                </div>
                                <div class='variable-stats'>
                                    {stats['uniques']} valeurs • min={stats['min']:.1f} • max={stats['max']:.1f}{outliers}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    if len(analyse_avant['classification']['quantitative']) > 10:
                        st.caption(f"... et {len(analyse_avant['classification']['quantitative']) - 10} autres")
                else:
                    st.caption("Aucune variable quantitative")
                st.markdown('</div>', unsafe_allow_html=True)

            with col_var2:
                st.markdown('<div class="quality-card">', unsafe_allow_html=True)
                st.markdown("##### Variables Qualitatives")
                if analyse_avant['classification']['qualitative']:
                    for col in analyse_avant['classification']['qualitative'][:10]:
                        stats = next((s for s in analyse_avant['col_stats'] if s['nom'] == col), None)
                        st.markdown(f"""
                            <div class='variable-item'>
                                <div class='variable-name'>
                                    {col}
                                    <span class='badge-qualitative'>QL</span>
                                </div>
                                <div class='variable-stats'>
                                    {stats['uniques']} catégories • {stats['non_nulles']} non-nulles
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    if len(analyse_avant['classification']['qualitative']) > 10:
                        st.caption(f"... et {len(analyse_avant['classification']['qualitative']) - 10} autres")
                else:
                    st.caption("Aucune variable qualitative")
                st.markdown('</div>', unsafe_allow_html=True)

            if analyse_avant['classification']['dates']:
                st.markdown('<div class="quality-card">', unsafe_allow_html=True)
                st.markdown("##### Variables Date")
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
                st.markdown("##### Cibles potentielles ML")
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
                for stats in analyse_avant['col_stats'][:20]:
                    with st.expander(f"📊 {stats['nom']} ({stats['type']})"):
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
                        color = "#ef4444" if prob['severity'] > 2 else "#f97316" if prob['severity'] > 1 else "#4361ee"
                        st.markdown(f"""
                            <div class='timeline-item' style='border-left-color:{color};'>
                                <div class='timeline-icon'>⚠️</div>
                                <div>
                                    <strong style='color:{color};'>{prob['colonne']}</strong>
                                    <br><span style='color:#64748b;'>{', '.join(prob['issues'])}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.caption(f"🔍 {len(analyse_avant['problem_columns'])} problèmes détectés")
            else:
                st.success("✅ Aucun problème détecté")

        with tab5:
            col_v1, col_v2 = st.columns(2)

            with col_v1:
                type_counts = {
                    'Quantitatives': len(analyse_avant['classification']['quantitative']),
                    'Qualitatives': len(analyse_avant['classification']['qualitative']),
                    'Dates': len(analyse_avant['classification']['dates'])
                }
                fig = px.pie(values=list(type_counts.values()), names=list(type_counts.keys()),
                             title="Types de variables", color_discrete_sequence=['#10b981', '#4361ee', '#f97316'])
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)

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
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.caption("Aucune valeur manquante")

            if len(analyse_avant['classification']['quantitative']) > 1:
                corr_matrix = df_avant[analyse_avant['classification']['quantitative']].corr()
                fig = px.imshow(corr_matrix, text_auto='.2f', aspect="auto",
                                title="Matrice de corrélation", color_continuous_scale='RdBu')
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)

        with tab6:
            st.markdown("##### Recommandations de nettoyage")
            recs_qualite = generer_recommandations_qualite(analyse_avant)
            if recs_qualite:
                for rec in recs_qualite:
                    color = "#ef4444" if rec['priority'] == 'HAUTE' else "#f97316" if rec[
                                                                                          'priority'] == 'MOYENNE' else "#4361ee"
                    st.markdown(f"""
                        <div class='timeline-item' style='border-left-color:{color};'>
                            <div class='timeline-icon'>{rec['icon']}</div>
                            <div>
                                <span style='background:{color}; color:white; padding:0.2rem 0.5rem; border-radius:12px; font-size:0.7rem;'>{rec['priority']}</span>
                                <br><strong>{rec['categorie']}</strong>
                                <br><span style='color:#64748b;'>{rec['message']}</span>
                                <br><span style='color:#4361ee;'>💡 {rec['action']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ Dataset déjà propre")

            st.markdown("##### Feature Engineering recommandé")
            recs_fe = generer_recommandations_feature_engineering(analyse_avant)
            if recs_fe:
                for rec in recs_fe:
                    color = "#ef4444" if rec['priority'] == 'HAUTE' else "#f97316"
                    st.markdown(f"""
                        <div class='timeline-item' style='border-left-color:{color};'>
                            <div class='timeline-icon'>🔧</div>
                            <div>
                                <span style='background:{color}; color:white; padding:0.2rem 0.5rem; border-radius:12px; font-size:0.7rem;'>{rec['priority']}</span>
                                <br><strong>{rec['categorie']} - {rec.get('colonne', 'Général')}</strong>
                                <br><span style='color:#64748b;'>{rec['raison']}</span>
                                <br><span style='color:#4361ee;'>💡 {rec['technique']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            if analyse_avant['classification']['a_convertir']:
                st.markdown("##### Conversions suggérées")
                for conv in analyse_avant['classification']['a_convertir']:
                    st.markdown(f"""
                        <div class='timeline-item' style='border-left-color:#f97316;'>
                            <div class='timeline-icon'>🔄</div>
                            <div>
                                <strong>{conv['colonne']}</strong>
                                <br><span style='color:#64748b;'>{conv['type_actuel']} → {conv['type_suggere']}</span>
                                <br><small>{conv['raison']}</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

        if analyse_apres:
            st.markdown("---")
            st.markdown("## 🔄 Comparaison Original vs Nettoyé")

            col_c1, col_c2, col_c3, col_c4 = st.columns(4)

            with col_c1:
                delta = comparaison['amelioration_score']
                delta_color = "green" if delta > 0 else "red"
                st.metric("Score qualité", f"{analyse_apres['quality_score']:.1f}",
                          f"{'▲' if delta > 0 else '▼'} {abs(delta):.1f}",
                          delta_color=delta_color)

            with col_c2:
                delta = comparaison['reduction_lignes']
                st.metric("Lignes", f"{analyse_apres['total_lignes']:,}",
                          f"▼ {delta}", delta_color="green" if delta > 0 else "red")

            with col_c3:
                delta = comparaison['reduction_missing']
                st.metric("Manquantes", f"{analyse_apres['total_missing']:,}",
                          f"▼ {delta}", delta_color="green" if delta > 0 else "red")

            with col_c4:
                delta = comparaison['reduction_problemes']
                delta_symbol = "▼" if delta > 0 else "▲" if delta < 0 else "="
                st.metric("Problèmes", len(analyse_apres['problem_columns']),
                          f"{delta_symbol} {abs(delta)}" if delta != 0 else "=",
                          delta_color="green" if delta > 0 else "red" if delta < 0 else "gray")

else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div class='upload-prompt'>
                <span style='font-size:4rem;'>📊</span>
                <h2>Chargez un dataset pour commencer</h2>
                <p>Analyse complète • Nettoyage • Feature Engineering • ML</p>
                <div class='feature-grid'>
                    <div class='feature-item'>Statistiques globales</div>
                    <div class='feature-item'>Types de données</div>
                    <div class='feature-item'>Variables manquantes</div>
                    <div class='feature-item'>Classification auto</div>
                    <div class='feature-item'>Comparaison avant/après</div>
                    <div class='feature-item'>Feature engineering</div>
                    <div class='feature-item'>Recommandations ACP</div>
                    <div class='feature-item'>Préparation ML</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("""
    <div class='footer'>
        <strong>Data Quality Analyzer v2.0</strong> • Analyse complète pour Machine Learning
    </div>
""", unsafe_allow_html=True)