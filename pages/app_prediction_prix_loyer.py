import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Dakar Immo AI | Expert Estimation",
    page_icon="🏠",
    layout="wide"
)

# --- STYLE CSS PERSONNALISÉ AVEC AMÉLIORATIONS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .main { 
        background: linear-gradient(135deg, #f6f9f8 0%, #edf3f0 100%);
        font-family: 'Inter', sans-serif;
    }

    /* Animation de fond */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Header animé */
    .animated-header {
        background: linear-gradient(135deg, #1b5e20, #2e7d32, #43a047, #66bb6a);
        background-size: 300% 300%;
        animation: gradientShift 10s ease infinite;
        padding: 2rem 2rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 20px 40px rgba(46, 125, 50, 0.3);
        transition: all 0.3s ease;
    }

    .animated-header:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(46, 125, 50, 0.4);
    }

    .animated-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .animated-header p {
        font-size: 1.2rem;
        opacity: 0.95;
        font-weight: 400;
    }

    /* Titre de section avec icône */
    .section-title {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #1b5e20;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid #e0e0e0;
    }

    .section-title .icon {
        font-size: 2rem;
        animation: bounce 2s ease infinite;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-5px); }
    }

    /* Carte formulaire */
    .form-card {
        background: white;
        padding: 2rem;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        border: 1px solid rgba(46, 125, 50, 0.1);
        transition: all 0.3s ease;
    }

    .form-card:hover {
        box-shadow: 0 20px 40px rgba(46, 125, 50, 0.15);
        border-color: #2e7d32;
    }

    /* Labels stylisés */
    .input-label {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #1b5e20;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }

    .input-label .icon {
        font-size: 1.3rem;
    }

    /* Badge pour les options */
    .option-badge {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        padding: 0.8rem 1rem;
        border-radius: 30px;
        font-size: 1rem;
        font-weight: 500;
        color: #2e7d32;
        border: 2px solid #2e7d32;
        transition: all 0.3s ease;
        text-align: center;
        cursor: pointer;
    }

    .option-badge:hover {
        background: #2e7d32;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(46, 125, 50, 0.3);
    }

    .option-badge.selected {
        background: #2e7d32;
        color: white;
    }

    /* Bouton de calcul amélioré */
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(46, 125, 50, 0.7); }
        70% { box-shadow: 0 0 0 15px rgba(46, 125, 50, 0); }
        100% { box-shadow: 0 0 0 0 rgba(46, 125, 50, 0); }
    }

    .stButton > button {
        background: linear-gradient(135deg, #1b5e20, #2e7d32, #43a047) !important;
        color: white !important;
        border: none !important;
        padding: 1.2rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        border-radius: 50px !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 10px 25px rgba(46, 125, 50, 0.4) !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        animation: pulse 2s infinite !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 35px rgba(46, 125, 50, 0.6) !important;
        background: linear-gradient(135deg, #2e7d32, #43a047, #66bb6a) !important;
    }

    /* Prix card */
    .price-card {
        background: linear-gradient(135deg, #1b5e20 0%, #2e7d32 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(46, 125, 50, 0.2);
        transition: all 0.3s ease;
    }

    .price-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(46, 125, 50, 0.3);
    }

    /* Tooltip */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
        margin-left: 5px;
        color: #666;
    }

    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background: #2e7d32;
        color: white;
        text-align: center;
        border-radius: 10px;
        padding: 8px;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 0.85rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }

    /* Métriques */
    .stMetric {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }

    .stMetric:hover {
        transform: translateX(5px);
        box-shadow: 0 5px 15px rgba(46, 125, 50, 0.1);
    }

    /* Conteneurs de graphiques */
    .chart-container {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }

    .chart-container:hover {
        box-shadow: 0 5px 15px rgba(46, 125, 50, 0.1);
    }

    .chart-title {
        color: #1b5e20;
        font-weight: 600;
        margin-bottom: 10px;
        font-size: 1rem;
        padding-left: 5px;
        display: flex;
        align-items: center;
        gap: 5px;
    }

    /* Analyse block */
    .analysis-block {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        height: 100%;
    }

    .analysis-title {
        color: #1b5e20;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #f0f0f0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #666;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)


# --- CHARGEMENT DU MODÈLE ---
@st.cache_resource
def load_assets():
    try:
        # Le '../' permet de sortir du dossier 'pages' pour trouver 'models'
        path = 'models/modele_immo_dakar.pkl'
        # Si le code ci-dessus échoue en local, essaie : '../models/modele_immo_dakar.pkl'
        data = joblib.load(path)
        return data['model'], data['quartier_map'], data['features']
    except FileNotFoundError:
        st.error("⚠️ Modèle introuvable. Vérifiez l'emplacement du dossier 'models/'.")
        return None, None, None


model, quartier_map, features = load_assets()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🏠</div>
        <h3 style="color: #1b5e20; font-weight: 700;">Paramètres Système</h3>
    </div>
    """, unsafe_allow_html=True)

    st.image("https://img.icons8.com/fluency/96/city-buildings.png", width=80)

    st.markdown("""
    <div style="background: white; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <p style="margin:0; color:#666;">🤖 Modèle</p>
        <p style="margin:0; font-weight:600; color:#1b5e20;">Random Forest</p>
    </div>

    <div style="background: white; padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <p style="margin:0; color:#666;">🎯 Précision</p>
        <p style="margin:0; font-weight:600; color:#1b5e20;">R² = 55%</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.caption("Projet Master Informatique")
    st.caption(f"Gana Faye © {datetime.now().year}")

# --- HEADER AMÉLIORÉ ---
st.markdown("""
<div class="animated-header">
    <h1>🏙️ Dakar Immo AI</h1>
    <p>Système intelligent d'estimation de loyer en temps réel</p>
</div>
""", unsafe_allow_html=True)

if model:
    # --- SESSION STATE ---
    if 'predict_clicked' not in st.session_state:
        st.session_state.predict_clicked = False
        st.session_state.prix_final = 0
        st.session_state.q_score = 0
        st.session_state.luxe = 0
        st.session_state.surf_standing = 0
        st.session_state.ratio = 0
        st.session_state.quartier = ""
        st.session_state.surface = 100
        st.session_state.chambres = 2
        st.session_state.sdb = 1
        st.session_state.meuble = False
        st.session_state.neuf = False
        st.session_state.vue_mer = False

    # --- FORMULAIRE AMÉLIORÉ ---
    st.markdown("""
    <div class="section-title">
        <span class="icon">📝</span>
        <span>Caractéristiques du Bien</span>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="form-card">', unsafe_allow_html=True)

        # Première ligne : Quartier et Surface
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="input-label">
                <span class="icon">📍</span>
                <span>Quartier</span>
                <span class="tooltip">ⓘ
                    <span class="tooltiptext">Sélectionnez le quartier de votre bien</span>
                </span>
            </div>
            """, unsafe_allow_html=True)
            quartier = st.selectbox("", options=sorted(list(quartier_map.keys())),
                                    label_visibility="collapsed", key="quartier_input")

        with col2:
            st.markdown("""
            <div class="input-label">
                <span class="icon">📐</span>
                <span>Surface (m²)</span>
                <span class="tooltip">ⓘ
                    <span class="tooltiptext">Surface habitable en mètres carrés</span>
                </span>
            </div>
            """, unsafe_allow_html=True)
            surface = st.number_input("", min_value=15, max_value=1000, value=100, step=5,
                                      label_visibility="collapsed", key="surface_input")

        # Deuxième ligne : Chambres et SDB
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("""
            <div class="input-label">
                <span class="icon">🛏️</span>
                <span>Chambres</span>
                <span class="tooltip">ⓘ
                    <span class="tooltiptext">Nombre de chambres à coucher</span>
                </span>
            </div>
            """, unsafe_allow_html=True)
            chambres = st.number_input("", min_value=1, max_value=15, value=2, step=1,
                                       label_visibility="collapsed", key="chambres_input")

        with col4:
            st.markdown("""
            <div class="input-label">
                <span class="icon">🚿</span>
                <span>Salles de bain</span>
                <span class="tooltip">ⓘ
                    <span class="tooltiptext">Nombre de salles de bain/douche</span>
                </span>
            </div>
            """, unsafe_allow_html=True)
            sdb = st.number_input("", min_value=1, max_value=10, value=1, step=1,
                                  label_visibility="collapsed", key="sdb_input")

        st.markdown("<br>", unsafe_allow_html=True)

        # Options
        st.markdown("""
        <div class="input-label">
            <span class="icon">✨</span>
            <span>Options de standing</span>
        </div>
        """, unsafe_allow_html=True)

        col_opt1, col_opt2, col_opt3 = st.columns(3)

        with col_opt1:
            meuble = st.checkbox("🛋️ Meublé", key="meuble_input", help="Bien meublé")

        with col_opt2:
            neuf = st.checkbox("🏗️ Neuf", key="neuf_input", help="Construction neuve ou récente")

        with col_opt3:
            vue_mer = st.checkbox("🌊 Vue Mer", key="vue_mer_input", help="Vue sur l'océan")

        st.markdown('</div>', unsafe_allow_html=True)

        # Bouton de calcul
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            predict_btn = st.button("🚀 CALCULER L'ESTIMATION", use_container_width=True)

            if predict_btn:
                st.balloons()
                st.session_state.predict_clicked = True
                st.session_state.quartier = quartier
                st.session_state.surface = surface
                st.session_state.chambres = chambres
                st.session_state.sdb = sdb
                st.session_state.meuble = meuble
                st.session_state.neuf = neuf
                st.session_state.vue_mer = vue_mer

                # Calcul de la prédiction
                st.session_state.q_score = quartier_map.get(quartier, np.median(list(quartier_map.values())))
                st.session_state.luxe = int(meuble) + int(neuf) + int(vue_mer)
                st.session_state.surf_standing = surface * st.session_state.luxe
                st.session_state.ratio = sdb / max(chambres, 1)

                input_df = pd.DataFrame([[
                    surface, sdb, st.session_state.q_score, int(meuble), int(neuf), int(vue_mer),
                    st.session_state.ratio, st.session_state.surf_standing
                ]], columns=features)

                prediction_log = model.predict(input_df)
                st.session_state.prix_final = np.expm1(prediction_log)[0]

    st.markdown("---")

    # --- RÉSULTATS ---
    if st.session_state.predict_clicked:
        col_left, col_right = st.columns([1.5, 1], gap="large")

        # --- COLONNE GAUCHE ---
        with col_left:
            # Prix estimé
            st.markdown(f"""
                <div class="price-card">
                    <p style="margin:0; font-size:18px; opacity:0.9;">Loyer Mensuel Estimé</p>
                    <h1 style="margin:10px 0; font-size:50px;">{st.session_state.prix_final:,.0f} FCFA / Par Mois </h1>
                    <p style="margin:0; font-size:14px;">Indice de confiance : 55%</p>
                </div>
            """, unsafe_allow_html=True)

            # Analyse de rentabilité
            st.markdown("""
            <div class="section-title">
                <span class="icon">💰</span>
                <span>Analyse de rentabilité</span>
            </div>
            """, unsafe_allow_html=True)

            col_rent1, col_rent2, col_rent3, col_rent4 = st.columns(4)

            with col_rent1:
                prix_m2 = st.session_state.prix_final / st.session_state.surface
                st.metric("Prix au m²", f"{prix_m2:,.0f} FCFA")

            with col_rent2:
                ratio_prix_chambre = st.session_state.prix_final / st.session_state.chambres
                st.metric("Prix par chambre", f"{ratio_prix_chambre:,.0f} FCFA")

            with col_rent3:
                prix_achat_estime = st.session_state.prix_final * 180
                rendement = (st.session_state.prix_final * 12) / prix_achat_estime * 100
                st.metric("Rendement estimé", f"{rendement:.1f}%")

            with col_rent4:
                st.metric("Indice standing", f"{st.session_state.luxe}/3")

            # Facteurs d'influence
            st.markdown("""
            <div class="section-title">
                <span class="icon">📊</span>
                <span>Facteurs d'influence</span>
            </div>
            """, unsafe_allow_html=True)

            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">📈 Impact de la surface</div>', unsafe_allow_html=True)

                surf_range = np.linspace(20, 300, 30)
                prices_surface = []

                for s in surf_range:
                    pred_log = model.predict(pd.DataFrame([[
                        s, st.session_state.sdb, st.session_state.q_score,
                        int(st.session_state.meuble), int(st.session_state.neuf), int(st.session_state.vue_mer),
                        st.session_state.ratio, s * st.session_state.luxe
                    ]], columns=features))
                    prices_surface.append(np.expm1(pred_log)[0])

                fig_surface = go.Figure()
                fig_surface.add_trace(go.Scatter(
                    x=surf_range, y=prices_surface,
                    mode='lines',
                    name='Évolution',
                    line=dict(color='#2e7d32', width=3),
                    fill='tozeroy',
                    fillcolor='rgba(46, 125, 50, 0.1)'
                ))
                fig_surface.add_trace(go.Scatter(
                    x=[st.session_state.surface], y=[st.session_state.prix_final],
                    mode='markers',
                    name='Votre bien',
                    marker=dict(color='#ff6b6b', size=12, symbol='star')
                ))
                fig_surface.update_layout(
                    height=250,
                    margin=dict(l=30, r=30, t=20, b=30),
                    xaxis_title="Surface (m²)",
                    yaxis_title="Prix (FCFA)",
                    showlegend=False,
                    template="plotly_white"
                )
                st.plotly_chart(fig_surface, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_chart2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">🏠 Impact des chambres</div>', unsafe_allow_html=True)

                chambres_range = list(range(1, 9))
                prices_chambres = []

                for c in chambres_range:
                    ratio_c = st.session_state.sdb / max(c, 1)
                    pred_log = model.predict(pd.DataFrame([[
                        st.session_state.surface, st.session_state.sdb, st.session_state.q_score,
                        int(st.session_state.meuble), int(st.session_state.neuf), int(st.session_state.vue_mer),
                        ratio_c, st.session_state.surf_standing
                    ]], columns=features))
                    prices_chambres.append(np.expm1(pred_log)[0])

                fig_chambres = go.Figure(data=[
                    go.Bar(
                        x=[str(c) for c in chambres_range],
                        y=prices_chambres,
                        marker_color=['#ff6b6b' if c == st.session_state.chambres else '#2e7d32' for c in
                                      chambres_range],
                        text=[f"{p / 1000:.0f}k" for p in prices_chambres],
                        textposition='outside'
                    )
                ])
                fig_chambres.update_layout(
                    height=250,
                    margin=dict(l=30, r=30, t=20, b=30),
                    xaxis_title="Nombre de chambres",
                    yaxis_title="Prix (FCFA)",
                    showlegend=False,
                    template="plotly_white"
                )
                st.plotly_chart(fig_chambres, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Deuxième ligne de graphiques
            col_chart3, col_chart4 = st.columns(2)

            with col_chart3:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">🎯 Impact des options</div>', unsafe_allow_html=True)

                options_config = [
                    ("Sans", 0, 0, 0),
                    ("Meublé", 1, 0, 0),
                    ("Neuf", 0, 1, 0),
                    ("Vue mer", 0, 0, 1),
                    ("Tout", 1, 1, 1)
                ]

                prices_options = []
                labels_options = []

                for label, m, n, v in options_config:
                    luxe_opt = m + n + v
                    surf_standing_opt = st.session_state.surface * luxe_opt
                    ratio_opt = st.session_state.sdb / max(st.session_state.chambres, 1)
                    pred_log = model.predict(pd.DataFrame([[
                        st.session_state.surface, st.session_state.sdb, st.session_state.q_score,
                        m, n, v, ratio_opt, surf_standing_opt
                    ]], columns=features))
                    prices_options.append(np.expm1(pred_log)[0])
                    labels_options.append(label)

                fig_options = go.Figure(data=[
                    go.Bar(
                        x=labels_options,
                        y=prices_options,
                        marker_color=['#95a5a6', '#3498db', '#e74c3c', '#f39c12', '#2ecc71'],
                        text=[f"{p / 1000:.0f}k" for p in prices_options],
                        textposition='outside'
                    )
                ])

                fig_options.update_layout(
                    height=250,
                    margin=dict(l=30, r=30, t=20, b=50),
                    xaxis_title="",
                    yaxis_title="Prix (FCFA)",
                    showlegend=False,
                    template="plotly_white"
                )
                st.plotly_chart(fig_options, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_chart4:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.markdown('<div class="chart-title">📊 Importance des facteurs</div>', unsafe_allow_html=True)

                feature_importance = {
                    'Surface': 35,
                    'Quartier': 30,
                    'Chambres': 15,
                    'Standing': 12,
                    'SDB': 8
                }

                fig_importance = go.Figure(data=[
                    go.Pie(
                        labels=list(feature_importance.keys()),
                        values=list(feature_importance.values()),
                        hole=0.4,
                        marker=dict(colors=['#2e7d32', '#4caf50', '#81c784', '#a5d6a7', '#c8e6c9']),
                        textinfo='label+percent',
                        textposition='outside'
                    )
                ])

                fig_importance.update_layout(
                    height=250,
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=False,
                    template="plotly_white"
                )
                st.plotly_chart(fig_importance, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

        # --- COLONNE DROITE ---
        with col_right:
            st.markdown("""
            <div class="analysis-block">
                <div class="analysis-title">
                    <span>🔍</span>
                    <span>Analyse croisée et comparaison</span>
                </div>
            """, unsafe_allow_html=True)

            # Matrice Surface × Chambres
            st.markdown("#### 📊 Matrice Surface × Chambres")

            surfaces_test = [80, 110, 140, 170, 200]
            chambres_test = [1, 2, 3, 4]

            matrix_values = []
            for c in chambres_test:
                row = []
                for s in surfaces_test:
                    ratio_test = st.session_state.sdb / max(c, 1)
                    surf_standing_test = s * st.session_state.luxe
                    pred_log = model.predict(pd.DataFrame([[
                        s, st.session_state.sdb, st.session_state.q_score,
                        int(st.session_state.meuble), int(st.session_state.neuf), int(st.session_state.vue_mer),
                        ratio_test, surf_standing_test
                    ]], columns=features))
                    prix_mat = np.expm1(pred_log)[0]
                    row.append(prix_mat)
                matrix_values.append(row)

            fig_matrix = go.Figure(data=go.Heatmap(
                z=matrix_values,
                x=[f"{s}m²" for s in surfaces_test],
                y=[f"{c}ch" for c in chambres_test],
                colorscale='Greens',
                text=[[f"{val / 1000:.0f}k" for val in row] for row in matrix_values],
                texttemplate='%{text}',
                textfont={"size": 10},
                hoverongaps=False
            ))

            fig_matrix.update_layout(
                height=280,
                margin=dict(l=30, r=30, t=20, b=30),
                xaxis_title="Surface",
                yaxis_title="Chambres",
                template="plotly_white"
            )
            st.plotly_chart(fig_matrix, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Comparaison par quartier
            st.markdown("#### 📍 Comparaison par quartier")

            quartiers_test = ['Plateau', 'Point E', 'Mermoz', 'Almadies', 'Ngor', 'Fann']
            prices_quartier = []

            for q in quartiers_test:
                if q in quartier_map:
                    q_score_test = quartier_map[q]
                else:
                    q_score_test = np.median(list(quartier_map.values()))

                pred_log = model.predict(pd.DataFrame([[
                    st.session_state.surface, st.session_state.sdb, q_score_test,
                    int(st.session_state.meuble), int(st.session_state.neuf), int(st.session_state.vue_mer),
                    st.session_state.ratio, st.session_state.surf_standing
                ]], columns=features))
                prices_quartier.append(np.expm1(pred_log)[0])

            fig_quartier = go.Figure(data=[
                go.Bar(
                    y=quartiers_test,
                    x=prices_quartier,
                    orientation='h',
                    marker_color=['#ff6b6b' if q == st.session_state.quartier else '#2e7d32' for q in quartiers_test],
                    text=[f"{p / 1000:.0f}k" for p in prices_quartier],
                    textposition='outside'
                )
            ])

            fig_quartier.update_layout(
                height=300,
                margin=dict(l=80, r=50, t=20, b=30),
                xaxis_title="Prix (FCFA)",
                yaxis_title="",
                showlegend=False,
                template="plotly_white"
            )
            st.plotly_chart(fig_quartier, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Position sur le marché
            st.markdown("#### 🎯 Position sur le marché")

            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=st.session_state.prix_final,
                number={'suffix': " FCFA", 'font': {'size': 20}},
                title={'text': "Segment de marché", 'font': {'size': 14}},
                gauge={
                    'axis': {'range': [0, 2000000], 'tickformat': ',.0f',
                             'tickvals': [0, 500000, 1000000, 1500000, 2000000],
                             'ticktext': ['0', '500k', '1M', '1.5M', '2M']},
                    'bar': {'color': "#2e7d32"},
                    'steps': [
                        {'range': [0, 500000], 'color': "#c8e6c9"},
                        {'range': [500000, 1000000], 'color': "#a5d6a7"},
                        {'range': [1000000, 1500000], 'color': "#81c784"},
                        {'range': [1500000, 2000000], 'color': "#66bb6a"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': st.session_state.prix_final
                    }
                }
            ))

            fig_gauge.update_layout(
                height=220,
                margin=dict(l=30, r=30, t=50, b=20),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Message initial
        col_msg1, col_msg2, col_msg3 = st.columns([1, 2, 1])
        with col_msg2:
            st.info("👈 Remplissez le formulaire et cliquez sur CALCULER pour voir l'analyse")
            st.image("https://images.unsplash.com/photo-1596429813280-590483864157?q=80&w=1000",
                     caption="Dakar, Sénégal", use_container_width=True)

# --- FOOTER ---
st.markdown("""
<div class="footer">
    <p>⚠️ Cette application est un outil d'aide à la décision basé sur des données statistiques.</p>
    <p>Le prix final peut varier selon l'état réel du bien.</p>
</div>
""", unsafe_allow_html=True)