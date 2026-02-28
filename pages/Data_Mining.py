import streamlit as st
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris, load_breast_cancer, load_wine, load_digits
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Configuration de la page
st.set_page_config(
    page_title="PCA Learning Lab | Apprentissage de l'ACP",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS SPECTACULAIRE ---
st.markdown("""
    <style>
    /* Import des polices */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    /* Style général */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Conteneur principal */
    .main-header {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 30px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.3);
    }

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.02em;
    }

    .main-subtitle {
        color: #4b5563;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }

    /* Cartes de section */
    .section-card {
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s ease;
    }

    .section-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .section-title span {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }

    /* Cartes métriques */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255,255,255,0.2);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1;
    }

    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.02em;
        margin-top: 0.3rem;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 30px;
        font-size: 0.8rem;
        font-weight: 600;
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }

    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #f9fafb 0%, #ffffff 100%);
        padding: 1.2rem;
        border-radius: 16px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }

    .info-title {
        font-weight: 600;
        color: #374151;
        margin-bottom: 0.3rem;
    }

    .info-text {
        color: #6b7280;
        font-size: 0.9rem;
    }

    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 2px dotted #667eea;
        cursor: help;
    }

    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: white;
        padding: 0.5rem;
        border-radius: 50px;
        border: 1px solid #e5e7eb;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 30px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        color: #4b5563;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: rgba(255,255,255,0.8);
        font-size: 0.9rem;
        margin-top: 2rem;
    }

    /* Animations */
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }

    .floating {
        animation: float 3s ease-in-out infinite;
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

# --- EN-TÊTE SPECTACULAIRE ---
st.markdown("""
    <div class="main-header floating">
        <h1 class="main-title">📊 PCA Learning Lab</h1>
        <p class="main-subtitle">Explorez et comprenez l'Analyse en Composantes Principales de manière interactive</p>
        <div style='display: flex; gap: 0.5rem; margin-top: 1rem;'>
            <span class='badge'>🎓 Apprentissage automatique</span>
            <span class='badge'>📉 Réduction de dimension</span>
            <span class='badge'>🔬 Visualisation de données</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR ÉLÉGANTE ---
with st.sidebar:
    st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                   padding: 2rem; border-radius: 20px; margin-bottom: 2rem; color: white;'>
            <h3 style='margin:0; font-size:1.8rem;'>🎛️ Contrôle</h3>
            <p style='opacity:0.9; margin:0.3rem 0 0 0;'>Paramètres de l'ACP</p>
        </div>
    """, unsafe_allow_html=True)

    # Sélection du dataset
    dataset_choice = st.selectbox(
        "📁 Choisir un dataset",
        ["Iris (Classification fleurs)",
         "Breast Cancer (Médical)",
         "Wine (Vins)",
         "Digits (Chiffres manuscrits)"]
    )

    # Mapping des datasets
    datasets = {
        "Iris (Classification fleurs)": load_iris(),
        "Breast Cancer (Médical)": load_breast_cancer(),
        "Wine (Vins)": load_wine(),
        "Digits (Chiffres manuscrits)": load_digits()
    }

    data_obj = datasets[dataset_choice]

    # Informations sur le dataset
    st.markdown("---")
    st.markdown(f"""
        <div class='info-box'>
            <div class='info-title'>📊 Informations dataset</div>
            <div class='info-text'>• Échantillons: {data_obj.data.shape[0]}</div>
            <div class='info-text'>• Features: {data_obj.data.shape[1]}</div>
            <div class='info-text'>• Classes: {len(data_obj.target_names)}</div>
        </div>
    """, unsafe_allow_html=True)

    # Paramètres PCA
    st.markdown("---")
    st.markdown("### ⚙️ Paramètres ACP")

    n_components = st.slider(
        "Nombre de composantes",
        min_value=2,
        max_value=min(10, data_obj.data.shape[1]),
        value=2,
        help="Plus de composantes = plus d'information mais visualisation plus complexe"
    )

    scale_data = st.checkbox("Standardiser les données", value=True,
                             help="Recommandé quand les variables ont des échelles différentes")

    show_original = st.checkbox("Afficher données originales", value=True)
    show_pca = st.checkbox("Afficher projection PCA", value=True)

# --- PRÉPARATION DES DONNÉES ---
df = pd.DataFrame(data_obj.data, columns=data_obj.feature_names)
df['Classe'] = data_obj.target_names[data_obj.target]

# Standardisation
if scale_data:
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_obj.data)
else:
    data_scaled = data_obj.data

# ACP
pca = PCA(n_components=n_components)
components = pca.fit_transform(data_scaled)

# DataFrame pour visualisation
pca_columns = [f'PC{i + 1}' for i in range(n_components)]
df_pca = pd.DataFrame(data=components, columns=pca_columns)
df_pca['Classe'] = data_obj.target_names[data_obj.target]

# Calcul des métriques
var_explained = pca.explained_variance_ratio_ * 100
cumsum_var = np.cumsum(var_explained)

# --- SECTION 1 : APERÇU DES DONNÉES ---
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
        <div class="section-title">
            <span>📋</span> Aperçu des données originales
        </div>
    """, unsafe_allow_html=True)

    col_data1, col_data2 = st.columns([2, 1])

    with col_data1:
        if show_original:
            st.dataframe(
                df.head(10),
                width='stretch',
                height=300
            )

    with col_data2:
        # Statistiques rapides
        st.markdown("### 📊 Statistiques descriptives")

        # Moyennes par classe
        stats_df = df.groupby('Classe').mean().round(2)

        st.markdown(f"""
            <div style='background: #f9fafb; padding: 1rem; border-radius: 12px;'>
                <p style='margin:0; color:#4b5563;'><strong>Moyennes par classe:</strong></p>
                <div style='margin-top:0.5rem; font-size:0.9rem;'>
                    {stats_df.iloc[:, :3].to_html(classes='table', border=0)}
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 2 : VISUALISATION PCA ---
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
        <div class="section-title">
            <span>📈</span> Projection PCA
        </div>
    """, unsafe_allow_html=True)

    if show_pca:
        if n_components >= 2:
            # Visualisation 2D
            col_viz1, col_viz2 = st.columns([2, 1])

            with col_viz1:
                fig = px.scatter(
                    df_pca,
                    x='PC1',
                    y='PC2',
                    color='Classe',
                    title=f"Projection des données sur les 2 premières composantes",
                    labels={'PC1': f'PC1 ({var_explained[0]:.1f}%)',
                            'PC2': f'PC2 ({var_explained[1]:.1f}%)'},
                    template="plotly_white",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )

                fig.update_traces(marker=dict(size=8, line=dict(width=1, color='white')))
                fig.update_layout(
                    height=500,
                    hovermode='closest',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family="Space Grotesk")
                )

                st.plotly_chart(fig, width='stretch')

            with col_viz2:
                # Métriques
                st.markdown("### 📊 Variance expliquée")

                # Graphique en barres
                fig_var = go.Figure()
                fig_var.add_trace(go.Bar(
                    x=[f'PC{i + 1}' for i in range(n_components)],
                    y=var_explained,
                    marker_color='#667eea',
                    text=[f"{v:.1f}%" for v in var_explained],
                    textposition='outside'
                ))

                fig_var.update_layout(
                    height=250,
                    showlegend=False,
                    margin=dict(l=0, r=0, t=0, b=0),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    yaxis_title="Variance (%)"
                )

                st.plotly_chart(fig_var, width='stretch')

                # Carte de métriques
                st.markdown(f"""
                    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-top: 1rem;'>
                        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                  padding: 1rem; border-radius: 12px; color: white; text-align: center;'>
                            <div style='font-size: 0.8rem; opacity:0.9;'>Total info</div>
                            <div style='font-size: 1.5rem; font-weight:700;'>{cumsum_var[n_components - 1]:.1f}%</div>
                        </div>
                        <div style='background: #f9fafb; padding: 1rem; border-radius: 12px; text-align: center;'>
                            <div style='font-size: 0.8rem; color:#6b7280;'>Composantes</div>
                            <div style='font-size: 1.5rem; font-weight:700; color:#374151;'>{n_components}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 3 : ANALYSE APPROFONDIE ---
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
        <div class="section-title">
            <span>🔬</span> Analyse approfondie
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Variance cumulée", "🎯 Loadings", "💡 Interprétation"])

    with tab1:
        col_var1, col_var2 = st.columns([2, 1])

        with col_var1:
            # Graphique de variance cumulée
            fig_cumsum = go.Figure()

            # Barres individuelles
            fig_cumsum.add_trace(go.Bar(
                x=[f'PC{i + 1}' for i in range(n_components)],
                y=var_explained,
                name='Variance individuelle',
                marker_color='rgba(102, 126, 234, 0.5)',
                text=[f"{v:.1f}%" for v in var_explained],
                textposition='inside'
            ))

            # Ligne cumulative
            fig_cumsum.add_trace(go.Scatter(
                x=[f'PC{i + 1}' for i in range(n_components)],
                y=cumsum_var,
                name='Variance cumulée',
                line=dict(color='#e74c3c', width=3),
                mode='lines+markers',
                yaxis='y2'
            ))

            fig_cumsum.update_layout(
                title="Variance expliquée par composante",
                xaxis_title="Composantes",
                yaxis_title="Variance (%)",
                yaxis2=dict(
                    title="Variance cumulée (%)",
                    overlaying='y',
                    side='right',
                    range=[0, 100]
                ),
                height=400,
                hovermode='x unified',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
            )

            st.plotly_chart(fig_cumsum, width='stretch')

        with col_var2:
            # Recommandations
            n_95 = np.argmax(cumsum_var >= 95) + 1 if any(cumsum_var >= 95) else n_components
            n_90 = np.argmax(cumsum_var >= 90) + 1 if any(cumsum_var >= 90) else n_components

            st.markdown(f"""
                <div style='background: white; padding: 1.5rem; border-radius: 16px; border: 1px solid #e5e7eb;'>
                    <h4 style='margin-top:0; color:#374151;'>🎯 Recommandations</h4>

                    <div style='margin: 1.5rem 0;'>
                        <div style='display: flex; justify-content: space-between; margin-bottom:0.3rem;'>
                            <span style='color:#6b7280;'>Pour 90% d'info:</span>
                            <span style='font-weight:700; color:#10b981;'>{n_90} composantes</span>
                        </div>
                        <div style='background:#f3f4f6; height:6px; border-radius:3px;'>
                            <div style='background:#10b981; width:{n_90 / n_components * 100}%; height:6px; border-radius:3px;'></div>
                        </div>
                    </div>

                    <div style='margin: 1.5rem 0;'>
                        <div style='display: flex; justify-content: space-between; margin-bottom:0.3rem;'>
                            <span style='color:#6b7280;'>Pour 95% d'info:</span>
                            <span style='font-weight:700; color:#667eea;'>{n_95} composantes</span>
                        </div>
                        <div style='background:#f3f4f6; height:6px; border-radius:3px;'>
                            <div style='background:#667eea; width:{n_95 / n_components * 100}%; height:6px; border-radius:3px;'></div>
                        </div>
                    </div>

                    <div style='background:#f9fafb; padding:1rem; border-radius:12px; margin-top:1rem;'>
                        <p style='margin:0; color:#4b5563; font-size:0.9rem;'>
                            💡 Avec {n_90} composantes, vous conservez {cumsum_var[n_90 - 1]:.1f}% de l'information
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    with tab2:
        # Loadings (contribution des variables)
        loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
        loading_df = pd.DataFrame(
            loadings,
            columns=[f'PC{i + 1}' for i in range(n_components)],
            index=data_obj.feature_names[:10]  # Limiter pour lisibilité
        )

        fig_loadings = go.Figure()

        for i in range(min(3, n_components)):  # Top 3 composantes
            fig_loadings.add_trace(go.Bar(
                name=f'PC{i + 1}',
                x=loading_df.index,
                y=loading_df[f'PC{i + 1}'],
                text=loading_df[f'PC{i + 1}'].round(2),
                textposition='outside'
            ))

        fig_loadings.update_layout(
            title="Contribution des variables (loadings)",
            xaxis_title="Variables",
            yaxis_title="Loading",
            barmode='group',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig_loadings, width='stretch')

        st.markdown("""
            <div class='info-box'>
                <div class='info-title'>📖 Interprétation des loadings</div>
                <div class='info-text'>Les loadings indiquent la contribution de chaque variable originale aux composantes principales. 
                Plus la valeur absolue est élevée, plus la variable influence la composante.</div>
            </div>
        """, unsafe_allow_html=True)

    with tab3:
        col_int1, col_int2 = st.columns(2)

        with col_int1:
            st.markdown("""
                <div style='background: white; padding: 1.5rem; border-radius: 16px; height: 100%;'>
                    <h4 style='color:#374151; margin-top:0;'>🔍 Qu'est-ce que l'ACP ?</h4>
                    <p style='color:#4b5563; line-height:1.6;'>
                        L'Analyse en Composantes Principales (ACP) est une technique de réduction de dimension 
                        qui transforme des variables possiblement corrélées en un ensemble de variables 
                        linéairement indépendantes appelées composantes principales.
                    </p>
                    <ul style='color:#6b7280;'>
                        <li>📊 Réduit la dimensionnalité</li>
                        <li>🔬 Préserve le maximum d'information</li>
                        <li>📈 Facilite la visualisation</li>
                        <li>🎯 Identifie les patterns cachés</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        with col_int2:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          padding: 1.5rem; border-radius: 16px; height: 100%; color: white;'>
                    <h4 style='color:white; margin-top:0;'>✨ Résultats pour ce dataset</h4>
                    <p style='opacity:0.9;'>
                        • {data_obj.data.shape[1]} dimensions originales réduites à {n_components} dimensions<br>
                        • {cumsum_var[n_components - 1]:.1f}% de variance conservée<br>
                        • {data_obj.data.shape[0]} échantillons analysés<br>
                        • {len(data_obj.target_names)} classes distinctes
                    </p>
                    <div style='margin-top:1rem; background:rgba(255,255,255,0.2); padding:1rem; border-radius:12px;'>
                        <strong>🎓 Conclusion:</strong><br>
                        {'Les données sont bien séparables dans cet espace réduit' if cumsum_var[0] > 50 else 'Les données nécessitent plus de composantes pour une bonne séparation'}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 4 : SANKEYS ET COMPARAISONS ---
if n_components >= 2:
    with st.container():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("""
            <div class="section-title">
                <span>🔄</span> Comparaison avant/après ACP
            </div>
        """, unsafe_allow_html=True)

        col_comp1, col_comp2 = st.columns(2)

        with col_comp1:
            # Matrice de corrélation originale
            corr_matrix = df.iloc[:, :-1].corr()

            fig_corr = px.imshow(
                corr_matrix,
                text_auto='.2f',
                aspect="auto",
                color_continuous_scale='RdBu',
                title="Corrélations originales"
            )

            fig_corr.update_layout(height=400)
            st.plotly_chart(fig_corr, width='stretch')

        with col_comp2:
            # Matrice de corrélation des composantes (devrait être diagonale)
            corr_pca = df_pca.iloc[:, :-1].corr()

            fig_corr_pca = px.imshow(
                corr_pca,
                text_auto='.2f',
                aspect="auto",
                color_continuous_scale='RdBu',
                title="Corrélations après ACP (indépendance)"
            )

            fig_corr_pca.update_layout(height=400)
            st.plotly_chart(fig_corr_pca, width='stretch')

        st.markdown("""
            <div class='info-box'>
                <div class='info-title'>📌 Observation clé</div>
                <div class='info-text'>Les composantes principales sont décorrélées (matrice presque diagonale), 
                contrairement aux variables originales qui peuvent être corrélées entre elles.</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 5 : EXERCICES INTERACTIFS ---
with st.container():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("""
        <div class="section-title">
            <span>✏️</span> Testez vos connaissances
        </div>
    """, unsafe_allow_html=True)

    col_exo1, col_exo2 = st.columns(2)

    with col_exo1:
        st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 16px;'>
                <h4 style='color:#374151; margin-top:0;'>Question 1</h4>
                <p style='color:#4b5563;'>Quel pourcentage de variance est expliqué par la première composante ?</p>
            </div>
        """, unsafe_allow_html=True)

        answer1 = st.number_input("Votre réponse (%)", min_value=0.0, max_value=100.0, step=0.1)
        if answer1 > 0:
            if abs(answer1 - var_explained[0]) < 1:
                st.success("✅ Correct !")
            else:
                st.error(f"❌ Pas tout à fait. La bonne réponse est {var_explained[0]:.1f}%")

    with col_exo2:
        st.markdown("""
            <div style='background: white; padding: 1.5rem; border-radius: 16px;'>
                <h4 style='color:#374151; margin-top:0;'>Question 2</h4>
                <p style='color:#4b5563;'>Combien de composantes faut-il pour conserver 90% de l'information ?</p>
            </div>
        """, unsafe_allow_html=True)

        answer2 = st.number_input("Nombre de composantes", min_value=1, max_value=n_components, step=1)
        if answer2 > 0:
            if answer2 == n_90:
                st.success("✅ Correct !")
            else:
                st.error(f"❌ Il faut {n_90} composantes pour atteindre 90%")

    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
    <div class='footer'>
        <strong>PCA Learning Lab</strong> · Exploration interactive de l'Analyse en Composantes Principales<br>
        <span style='opacity: 0.6; font-size: 0.8rem;'>Développé pour l'apprentissage et la compréhension de l'ACP</span>
    </div>
""", unsafe_allow_html=True)