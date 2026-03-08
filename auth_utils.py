import streamlit as st


def apply_custom_style():
    """Épure l'interface et prépare la sidebar."""
    st.markdown("""
        <style>
            /* Supprime l'espace blanc inutile en haut */
            .block-container {
                padding-top: 1rem !important;
            }

            /* Masque la navigation par défaut pour utiliser tes boutons */
            [data-testid="stSidebarNav"] { display: none; }

            /* Style pour que le popover occupe bien la largeur de la sidebar */
            div[data-testid="stSidebar"] div[data-testid="stPopover"] > button {
                width: 100% !important;
                border-radius: 10px !important;
                border: 1px solid #2563eb !important;
                color: #2563eb !important;
            }
        </style>
    """, unsafe_allow_html=True)


def is_authorized():
    """Vérifie si l'utilisateur a passé la barrière de l'email."""
    return st.session_state.get("is_logged_in", False)


def login_sidebar():
    """Affiche le menu de connexion escamotable dans la barre latérale."""
    st.sidebar.title("🔐 Accès")

    if not is_authorized():
        # Utilisation du popover pour cacher le formulaire par défaut
        with st.sidebar.popover("S'identifier"):
            st.markdown("### Connexion")
            email = st.text_input("Votre email", placeholder="nom@exemple.com", key="email_auth")
            if st.button("Valider l'accès", use_container_width=True):
                if email in st.secrets["auth"]["allowed_emails"]:
                    st.session_state["is_logged_in"] = True
                    st.session_state["user_email"] = email
                    st.rerun()
                else:
                    st.error("Email non autorisé")
        st.sidebar.info("L'accès aux outils IA nécessite une autorisation.")
    else:
        # Affichage du statut si connecté
        st.sidebar.success(f"Connecté : \n\n{st.session_state['user_email']}")
        if st.sidebar.button("Se déconnecter", type="primary", use_container_width=True):
            st.session_state["is_logged_in"] = False
            st.rerun()