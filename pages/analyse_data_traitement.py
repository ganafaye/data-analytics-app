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
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons+Outlined">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons+Round">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons+Sharp">

    <style>
    /* Style de base pour les icônes */
    .material-icons, .material-icons-outlined, .material-icons-round, .material-icons-sharp {
        font-family: 'Material Icons' !important;
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
    }

    .material-icons-outlined { font-family: 'Material Icons Outlined' !important; }
    .material-icons-round { font-family: 'Material Icons Round' !important; }
    .material-icons-sharp { font-family: 'Material Icons Sharp' !important; }

    /* Animation pour le chargement */
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .spin {
        animation: spin 2s linear infinite;
        display: inline-block;
    }

    /* Style général */
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

    /* En-tête principal */
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 2rem 2.5rem;
        border-radius: 30px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
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

    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ff6b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
        font-family: 'Plus Jakarta Sans', sans-serif;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .main-subtitle {
        color: #4a5568;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 300;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: white !important;
        border-right: 1px solid rgba(102, 126, 234, 0.2);
        box-shadow: 5px 0 30px rgba(0, 0, 0, 0.03);
    }

    section[data-testid="stSidebar"] > div {
        background: white;
    }

    /* Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-right: 0.5rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
    }

    .badge-excellent {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
    }

    .badge-good {
        background: linear-gradient(135deg, #667eea 0%, #5a67d8 100%);
        color: white;
    }

    .badge-fair {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        color: white;
    }

    .badge-poor {
        background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
        color: white;
    }

    /* Timeline */
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
        flex-shrink: 0;
    }

    /* Variable item */
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
        margin-bottom: 0.5rem;
    }

    .variable-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.1);
        border-color: #667eea;
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

    /* Progress bar */
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

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.8rem;
        background: white;
        padding: 0.8rem;
        border-radius: 60px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin-bottom: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 40px;
        padding: 0.7rem 1.8rem;
        font-weight: 500;
        color: #4a5568;
        transition: all 0.3s ease;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
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

    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.2rem;
        }
        .main-subtitle {
            font-size: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)


# --- FONCTION POUR LES ICÔNES ---
def icon(name, variant="outlined", size=24, color=None, spin=False):
    """Génère une icône Google Material"""
    classes = f"material-icons-{variant}"
    if spin:
        classes += " spin"

    style = f"font-size: {size}px; line-height: 1; vertical-align: middle;"
    if color:
        style += f" color: {color};"

    return f"<i class='{classes}' style='{style}'>{name}</i>"


# --- FONCTIONS D'ANALYSE DE DONNÉES ---
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


# --- EN-TÊTE PRINCIPAL ---
st.markdown(f"""
    <div class="main-header">
        <h1 class="main-title">
            {icon('analytics', variant='sharp', size=40)} Data Quality Analyzer
        </h1>
        <p class="main-subtitle">
            {icon('insights', size=20, color='#667eea')} Analyse intelligente de la qualité des données · Nettoyage & Optimisation · Feature Engineering
        </p>
        <div style='display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap;'>
            <span class='badge badge-excellent'>{icon('category', size=16)} Classification auto</span>
            <span class='badge badge-good'>{icon('build', size=16)} Feature engineering</span>
            <span class='badge badge-fair'>{icon('scatter_plot', size=16)} Préparation ACP</span>
            <span class='badge badge-poor'>{icon('lightbulb', size=16)} Recommandations ML</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); 
                    padding: 2rem 1.5rem; border-radius: 0 0 30px 30px; 
                    margin-bottom: 1.5rem; text-align: center;'>
            <h3 style='font-size: 1.8rem; font-weight: 700; margin: 0; 
                       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       display: flex; align-items: center; justify-content: center; gap: 8px;'>
                {icon('folder_open', variant='sharp', size=32)} Chargement
            </h3>
            <p style='opacity: 0.8; font-size: 0.95rem; color: #718096;'>Importez vos datasets</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<h3 style='display: flex; align-items: center; gap: 8px;'>{icon('cloud_upload', size=20)} Dataset original</h3>",
        unsafe_allow_html=True)
    file_avant = st.file_uploader(
        "Charger le fichier original",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'pkl', 'txt'],
        key="file_avant",
        label_visibility="collapsed"
    )

    if file_avant:
        type_fichier = detecter_type_fichier(file_avant.name)
        st.info(f"{icon('table_chart', size=18)} Original : {type_fichier}")

    st.markdown("---")

    st.markdown(
        f"<h3 style='display: flex; align-items: center; gap: 8px;'>{icon('auto_awesome', size=20)} Dataset nettoyé</h3>",
        unsafe_allow_html=True)
    file_apres = st.file_uploader(
        "Charger la version nettoyée",
        type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'pkl', 'txt'],
        key="file_apres",
        label_visibility="collapsed"
    )

    if file_apres:
        type_fichier = detecter_type_fichier(file_apres.name)
        st.info(f"{icon('table_chart', size=18)} Nettoyé : {type_fichier}")

    st.markdown("---")

    st.markdown(f"<h3 style='display: flex; align-items: center; gap: 8px;'>{icon('settings', size=20)} Options</h3>",
                unsafe_allow_html=True)
    show_details = st.checkbox("Afficher les détails par colonne", value=True)
    threshold_missing = st.slider("Seuil d'alerte valeurs manquantes (%)", 0, 50, 10)
    show_problem_details = st.checkbox("Afficher les détails des problèmes", value=True)

# --- CORPS PRINCIPAL ---
if file_avant:
    df_avant, error_avant = charger_fichier(file_avant)

    if error_avant:
        st.error(f"{icon('error', size=20)} Erreur chargement original : {error_avant}")
    else:
        with st.spinner(f"Analyse du dataset original..."):
            analyse_avant = analyser_qualite_dataset(df_avant, "Original")

        if file_apres:
            df_apres, error_apres = charger_fichier(file_apres)
            if error_apres:
                st.error(f"{icon('error', size=20)} Erreur chargement nettoyé : {error_apres}")
                df_apres = None
                analyse_apres = None
                comparaison = None
            else:
                with st.spinner(f"Analyse du dataset nettoyé..."):
                    analyse_apres = analyser_qualite_dataset(df_apres, "Nettoyé")
                comparaison = comparer_datasets(analyse_avant, analyse_apres)
        else:
            df_apres = None
            analyse_apres = None
            comparaison = None

        st.markdown(f"## {icon('dashboard', size=28)} Dataset Original - Tableau de bord qualité",
                    unsafe_allow_html=True)

        # Métriques principales
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
                <div style='background: white; padding: 1.5rem; border-radius: 25px; 
                            box-shadow: 0 10px 30px rgba(0,0,0,0.05);'>
                    <div style='display: flex; align-items: center; gap: 16px;'>
                        <div style='width: 48px; height: 48px; border-radius: 24px; 
                                    background: linear-gradient(135deg, rgba(102,126,234,0.1), rgba(118,75,162,0.1));
                                    display: flex; align-items: center; justify-content: center;'>
                            {icon('stars', variant='sharp', size=32, color='#667eea')}
                        </div>
                        <div>
                            <div style='font-size: 3rem; font-weight: 800; 
                                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                                {analyse_avant['quality_score']:.1f}
                            </div>
                            <div style='color: #718096; font-size: 0.9rem; text-transform: uppercase;'>Score qualité</div>
                        </div>
                    </div>
                    <div style='margin-top: 1rem;'>
                        <span class='badge {analyse_avant['quality_badge']}'>
                            {icon('check', size=16)} {analyse_avant['quality_category']}
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div style='background: white; padding: 1.5rem; border-radius: 20px; text-align: center;
                            box-shadow: 0 8px 20px rgba(0,0,0,0.03); height: 100%;'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem; color: #667eea;'>
                        {icon('table_rows', size=40, color='#667eea')}
                    </div>
                    <div style='font-size: 2rem; font-weight: 700; color: #2d3748;'>{analyse_avant['total_lignes']:,}</div>
                    <div style='color: #718096; font-size: 0.8rem; text-transform: uppercase; 
                                display: flex; align-items: center; justify-content: center; gap: 4px;'>
                        {icon('table_rows', size=16)} Lignes
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div style='background: white; padding: 1.5rem; border-radius: 20px; text-align: center;
                            box-shadow: 0 8px 20px rgba(0,0,0,0.03); height: 100%;'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem; color: #667eea;'>
                        {icon('view_column', size=40, color='#667eea')}
                    </div>
                    <div style='font-size: 2rem; font-weight: 700; color: #2d3748;'>{analyse_avant['total_colonnes']}</div>
                    <div style='color: #718096; font-size: 0.8rem; text-transform: uppercase;
                                display: flex; align-items: center; justify-content: center; gap: 4px;'>
                        {icon('view_column', size=16)} Colonnes
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
                <div style='background: white; padding: 1.5rem; border-radius: 20px; text-align: center;
                            box-shadow: 0 8px 20px rgba(0,0,0,0.03); height: 100%;'>
                    <div style='font-size: 2.5rem; margin-bottom: 0.5rem; color: #667eea;'>
                        {icon('memory', size=40, color='#667eea')}
                    </div>
                    <div style='font-size: 2rem; font-weight: 700; color: #2d3748;'>{analyse_avant['memoire']:.2f}</div>
                    <div style='color: #718096; font-size: 0.8rem; text-transform: uppercase;
                                display: flex; align-items: center; justify-content: center; gap: 4px;'>
                        {icon('memory', size=16)} MB
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Onglets
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            f"{icon('table_view', size=18)} Aperçu général",
            f"{icon('category', size=18)} Classification",
            f"{icon('view_column', size=18)} Détails",
            f"{icon('warning', size=18)} Problèmes",
            f"{icon('insights', size=18)} Visualisations",
            f"{icon('lightbulb', size=18)} Recommandations"
        ])

        with tab1:
            st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 25px;">',
                        unsafe_allow_html=True)
            col_stat1, col_stat2 = st.columns(2)

            with col_stat1:
                st.markdown(f"### {icon('analytics', size=24)} Statistiques globales", unsafe_allow_html=True)
                st.markdown(f"""
                    * {icon('table_rows', size=16)} **Lignes :** {analyse_avant['total_lignes']:,}
                    * {icon('view_column', size=16)} **Colonnes :** {analyse_avant['total_colonnes']}
                    * {icon('memory', size=16)} **Mémoire :** {analyse_avant['memoire']:.2f} MB
                    * {icon('highlight_off', size=16)} **Valeurs manquantes :** {analyse_avant['total_missing']:,} ({analyse_avant['pct_missing']:.1f}%)
                    * {icon('content_copy', size=16)} **Lignes dupliquées :** {analyse_avant['duplicates']:,} ({analyse_avant['pct_duplicates']:.1f}%)
                """, unsafe_allow_html=True)

            with col_stat2:
                st.markdown(f"### {icon('data_usage', size=24)} Types de données", unsafe_allow_html=True)
                for dtype, count in analyse_avant['dtypes_summary'].items():
                    pct = (count / analyse_avant['total_colonnes']) * 100
                    st.markdown(f"""
                        * {icon('code', size=16)} **{dtype} :** {count} ({pct:.1f}%)
                        <div class='progress-container'><div class='progress-bar' style='width:{pct}%'></div></div>
                    """, unsafe_allow_html=True)

            if analyse_avant['missing_cols']:
                st.markdown(f"### {icon('warning', size=24, color='#e53e3e')} Colonnes avec valeurs manquantes",
                            unsafe_allow_html=True)
                for col, count in list(analyse_avant['missing_cols'].items())[:10]:
                    pct = (count / analyse_avant['total_lignes']) * 100
                    color = "#e53e3e" if pct > threshold_missing else "#ed8936"
                    st.markdown(f"""
                        * {icon('highlight_off', size=16, color=color)} **{col} :** {count:,} ({pct:.1f}%)
                        <div class='progress-container'><div class='progress-bar' style='width:{pct}%; background:{color};'></div></div>
                    """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            col_var1, col_var2 = st.columns(2)

            with col_var1:
                st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 25px;">',
                            unsafe_allow_html=True)
                st.markdown(f"### {icon('123', size=24)} Variables Quantitatives", unsafe_allow_html=True)
                if analyse_avant['classification']['quantitative']:
                    st.markdown(f"**{len(analyse_avant['classification']['quantitative'])} variables**")
                    for col in analyse_avant['classification']['quantitative'][:10]:
                        stats = next((s for s in analyse_avant['col_stats'] if s['nom'] == col), None)
                        outliers = f" · {stats['pct_outliers']:.1f}% outliers" if stats and 'pct_outliers' in stats else ""
                        st.markdown(f"""
                            <div class='variable-item'>
                                <div class='variable-name'>
                                    {icon('123', size=16, color='#48bb78')} {col}
                                    <span style='background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
                                                color: white; padding: 0.3rem 0.8rem; border-radius: 30px;
                                                font-size: 0.7rem; display: inline-flex; align-items: center; gap: 4px;'>
                                        {icon('123', size=12)} QN
                                    </span>
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
                st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 25px;">',
                            unsafe_allow_html=True)
                st.markdown(f"### {icon('category', size=24)} Variables Qualitatives", unsafe_allow_html=True)
                if analyse_avant['classification']['qualitative']:
                    st.markdown(f"**{len(analyse_avant['classification']['qualitative'])} variables**")
                    for col in analyse_avant['classification']['qualitative'][:10]:
                        stats = next((s for s in analyse_avant['col_stats'] if s['nom'] == col), None)
                        st.markdown(f"""
                            <div class='variable-item'>
                                <div class='variable-name'>
                                    {icon('category', size=16, color='#667eea')} {col}
                                    <span style='background: linear-gradient(135deg, #667eea 0%, #5a67d8 100%);
                                                color: white; padding: 0.3rem 0.8rem; border-radius: 30px;
                                                font-size: 0.7rem; display: inline-flex; align-items: center; gap: 4px;'>
                                        {icon('category', size=12)} QL
                                    </span>
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
                st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 25px; margin-top: 1rem;">',
                            unsafe_allow_html=True)
                st.markdown(f"### {icon('calendar_today', size=24)} Variables Date", unsafe_allow_html=True)
                for col in analyse_avant['classification']['dates']:
                    st.markdown(f"""
                        <div class='variable-item'>
                            <div class='variable-name'>
                                {icon('calendar_today', size=16, color='#ed8936')} {col}
                                <span style='background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
                                            color: white; padding: 0.3rem 0.8rem; border-radius: 30px;
                                            font-size: 0.7rem; display: inline-flex; align-items: center; gap: 4px;'>
                                    {icon('calendar_today', size=12)} Date
                                </span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            if analyse_avant['classification']['target_potential']:
                st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 25px; margin-top: 1rem;">',
                            unsafe_allow_html=True)
                st.markdown(f"### {icon('track_changes', size=24)} Cibles potentielles ML", unsafe_allow_html=True)
                for target in analyse_avant['classification']['target_potential']:
                    st.markdown(f"""
                        <div class='variable-item'>
                            <div class='variable-name'>
                                {icon('track_changes', size=16, color='#e53e3e')} {target['colonne']}
                                <span style='background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%);
                                            color: white; padding: 0.3rem 0.8rem; border-radius: 30px;
                                            font-size: 0.7rem; display: inline-flex; align-items: center; gap: 4px;'>
                                    {icon('flag', size=12)} {target['type']}
                                </span>
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
                    with st.expander(f"{icon(icon_name, size=20)} {stats['nom']} ({stats['type']})"):
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
                                <div class='timeline-icon'>{icon('warning', size=24, color='white')}</div>
                                <div>
                                    <strong style='color:{color};'>{prob['colonne']}</strong>
                                    <br><span style='color:#4a5568;'>{', '.join(prob['issues'])}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info(
                        f"{icon('info', size=20)} {len(analyse_avant['problem_columns'])} problèmes détectés (masqués)")
            else:
                st.success(f"{icon('check_circle', size=20)} Aucun problème détecté !")

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
                    st.info("Aucune valeur manquante")

            if len(analyse_avant['classification']['quantitative']) > 1:
                corr_matrix = df_avant[analyse_avant['classification']['quantitative']].corr()
                fig = px.imshow(corr_matrix, text_auto='.2f', aspect="auto",
                                title="Matrice de corrélation", color_continuous_scale='RdBu')
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)

        with tab6:
            st.markdown(f"### {icon('cleaning_services', size=24)} Recommandations de nettoyage",
                        unsafe_allow_html=True)
            recs_qualite = generer_recommandations_qualite(analyse_avant)
            if recs_qualite:
                for rec in recs_qualite:
                    color = "#e53e3e" if rec['priority'] == 'HAUTE' else "#ed8936" if rec[
                                                                                          'priority'] == 'MOYENNE' else "#667eea"
                    st.markdown(f"""
                        <div class='timeline-item' style='border-left-color:{color};'>
                            <div class='timeline-icon'>{icon(rec['icon'], size=24, color='white')}</div>
                            <div>
                                <span style='background:{color}; color:white; padding:0.2rem 0.5rem; border-radius:12px; font-size:0.7rem; display:inline-flex; align-items:center; gap:4px;'>
                                    {icon('priority_high', size=12)} {rec['priority']}
                                </span>
                                <br><strong>{rec['categorie']}</strong>
                                <br><span style='color:#4a5568;'>{rec['message']}</span>
                                <br><span style='color:#667eea; display:flex; align-items:center; gap:4px;'>
                                    {icon('lightbulb', size=16)} {rec['action']}
                                </span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.success(f"{icon('check_circle', size=20)} Dataset déjà propre !")

            st.markdown(f"### {icon('build', size=24)} Feature Engineering recommandé", unsafe_allow_html=True)
            recs_fe = generer_recommandations_feature_engineering(analyse_avant)
            if recs_fe:
                for rec in recs_fe:
                    color = "#e53e3e" if rec['priority'] == 'HAUTE' else "#ed8936"
                    st.markdown(f"""
                        <div class='timeline-item' style='border-left-color:{color};'>
                            <div class='timeline-icon'>{icon(rec.get('icon', 'build'), size=24, color='white')}</div>
                            <div>
                                <span style='background:{color}; color:white; padding:0.2rem 0.5rem; border-radius:12px; font-size:0.7rem; display:inline-flex; align-items:center; gap:4px;'>
                                    {icon('priority_high', size=12)} {rec['priority']}
                                </span>
                                <span style='margin-left:0.5rem; font-size:0.7rem; display:inline-flex; align-items:center; gap:4px;'>
                                    {icon('check_circle' if rec.get('pour_ACP', False) else 'warning', size=12)} 
                                    {'Compatible ACP' if rec.get('pour_ACP', False) else 'Non ACP'}
                                </span>
                                <br><strong>{rec['categorie']} - {rec.get('colonne', 'Général')}</strong>
                                <br><span style='color:#4a5568;'>{rec['raison']}</span>
                                <br><span style='color:#667eea; display:flex; align-items:center; gap:4px;'>
                                    {icon('lightbulb', size=16)} {rec['technique']}
                                </span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

            if analyse_avant['classification']['a_convertir']:
                st.markdown(f"### {icon('transform', size=24)} Conversions suggérées", unsafe_allow_html=True)
                for conv in analyse_avant['classification']['a_convertir']:
                    st.markdown(f"""
                        <div class='timeline-item' style='border-left-color:#ed8936;'>
                            <div class='timeline-icon'>{icon('transform', size=24, color='white')}</div>
                            <div>
                                <strong>{conv['colonne']}</strong>
                                <br><span style='color:#4a5568;'>{conv['type_actuel']} → {conv['type_suggere']}</span>
                                <br><small>{conv['raison']}</small>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

        if analyse_apres:
            st.markdown("---")
            st.markdown(f"## {icon('compare_arrows', size=28)} Comparaison Original vs Nettoyé", unsafe_allow_html=True)

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

            with st.expander(f"{icon('summarize', size=20)} Voir le bilan détaillé du nettoyage"):
                messages = verifier_nettoyage(comparaison)
                for icon_name, color, msg in messages:
                    st.markdown(f"""
                        <div style='background:white; padding:1rem; border-radius:12px; border-left:4px solid {color}; margin-bottom:0.5rem;'>
                            <div style='display:flex; align-items:center; gap:0.5rem;'>
                                {icon(icon_name, size=24, color=color)}
                                <span style='color:#4a5568; font-size:0.9rem;'>{msg}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                if show_problem_details and analyse_apres['problem_columns']:
                    st.markdown(f"### {icon('warning', size=20)} Problèmes restants dans le dataset nettoyé",
                                unsafe_allow_html=True)
                    for prob in analyse_apres['problem_columns'][:5]:
                        color = "#e53e3e" if prob['severity'] > 2 else "#ed8936" if prob['severity'] > 1 else "#667eea"
                        st.markdown(f"""
                            <div class='timeline-item' style='border-left-color:{color};'>
                                <div class='timeline-icon'>{icon('warning', size=24, color='white')}</div>
                                <div>
                                    <strong style='color:{color};'>{prob['colonne']}</strong>
                                    <br><span style='color:#4a5568;'>{', '.join(prob['issues'])}</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                    if len(analyse_apres['problem_columns']) > 5:
                        st.info(f"... et {len(analyse_apres['problem_columns']) - 5} autres problèmes")

            st.markdown(f"### {icon('insights', size=24)} Visualisation de la progression", unsafe_allow_html=True)

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

            st.plotly_chart(fig_progress, use_container_width=True)

else:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
            <div style='text-align:center; padding:3rem; background:white; border-radius:30px; box-shadow:0 20px 40px rgba(0,0,0,0.1);'>
                <div style='font-size:5rem; margin-bottom:1rem;'>{icon('analytics', size=80, color='#667eea')}</div>
                <h2>Chargez un dataset pour commencer</h2>
                <p style='color:#666;'>Analyse complète · Nettoyage · Feature Engineering · ML</p>
                <div style='display:grid; grid-template-columns:1fr 1fr; gap:1rem; margin-top:2rem; text-align:left;'>
                    <div>{icon('check_circle', size=16, color='#48bb78')} Statistiques globales</div>
                    <div>{icon('check_circle', size=16, color='#48bb78')} Types de données</div>
                    <div>{icon('check_circle', size=16, color='#48bb78')} Variables manquantes</div>
                    <div>{icon('check_circle', size=16, color='#48bb78')} Classification auto</div>
                    <div>{icon('check_circle', size=16, color='#48bb78')} Comparaison avant/après</div>
                    <div>{icon('check_circle', size=16, color='#48bb78')} Feature engineering</div>
                    <div>{icon('check_circle', size=16, color='#48bb78')} Recommandations ACP</div>
                    <div>{icon('check_circle', size=16, color='#48bb78')} Préparation ML</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
    <div class='footer'>
        <strong>Data Quality Analyzer v2.0</strong> · Analyse complète pour Machine Learning · Feature Engineering · Préparation ACP<br>
        <span style='opacity: 0.6; font-size: 0.8rem; display: flex; align-items: center; justify-content: center; gap: 4px;'>
            {icon('code', size=14)} Développé pour l'optimisation des pipelines de données
        </span>
    </div>
""", unsafe_allow_html=True)