import streamlit as st


def apply_custom_style():
    """Style pour masquer la navigation native et épurer le header."""
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] { display: none; }

            /* Style pour le conteneur du header de connexion */
            .auth-header {
                display: flex;
                justify-content: flex-end;
                align-items: center;
                gap: 10px;
                padding: 10px;
                background-color: #f8fafc;
                border-radius: 12px;
                margin-bottom: 20px;
                border: 1px solid #e2e8f0;
            }

            .stButton > button { width: 100%; border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)


def is_authorized():
    """Vérifie l'état de connexion."""
    return st.session_state.get("is_logged_in", False)


def login_header():
    """Affiche le formulaire de connexion dans le header de la page principale."""

    # Création d'un espace en haut de la page
    col_title, col_auth = st.columns([2, 1])

    with col_title:
        st.subheader("🚀 Gana's Datalab")

    with col_auth:
        if not is_authorized():
            # Formulaire compact dans la colonne de droite
            email = st.text_input("Accès réservé", placeholder="votre@email.com", label_visibility="collapsed",
                                  key="email_auth")
            if st.button("Se connecter 🔐"):
                if email in st.secrets["auth"]["allowed_emails"]:
                    st.session_state["is_logged_in"] = True
                    st.session_state["user_email"] = email
                    st.rerun()
                else:
                    st.error("Email non autorisé")
        else:
            # Affichage du profil si connecté
            st.markdown(f"🟢 **{st.session_state['user_email']}**")
            if st.button("Déconnexion"):
                st.session_state["is_logged_in"] = False
                st.rerun()
    st.markdown("---")