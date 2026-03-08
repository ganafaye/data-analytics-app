import streamlit as st

def local_css():
    st.markdown("""
        <style>
            /* 1. Masquer la navigation native de la sidebar (la liste des fichiers) */
            [data-testid="stSidebarNav"] {
                display: none;
            }

            /* 2. Supprimer l'espace vide en haut de la page */
            .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
            }

            /* 3. Style pour tes titres de catégories dans la sidebar */
            .sidebar-section-title {
                font-weight: 700;
                color: #1e293b;
                margin-top: 1.5rem;
                margin-bottom: 0.5rem;
                padding-left: 0.5rem;
                border-left: 4px solid #2563eb; /* Petite barre bleue verticale */
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            /* 4. Style pour les boutons de la sidebar (plus compacts) */
            .stButton > button {
                border-radius: 8px;
                text-align: left;
                padding: 0.5rem 1rem;
                border: 1px solid #e2e8f0;
                background-color: white;
                transition: all 0.3s ease;
            }

            .stButton > button:hover {
                border-color: #2563eb;
                color: #2563eb;
                background-color: #f8fafc;
            }
        </style>
    """, unsafe_allow_html=True)

# Appel de la fonction
local_css()