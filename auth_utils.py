import streamlit as st


def apply_custom_style():
    """Réduction maximale de l'espace et style du bouton de login."""
    st.markdown("""
        <style>
            /* Supprime l'espace blanc géant en haut */
            .block-container {
                padding-top: 1rem !important;
                padding-bottom: 0rem !important;
            }

            /* Masque le menu natif */
            [data-testid="stSidebarNav"] { display: none; }

            /* Style pour le bouton popover pour qu'il ressemble à une icône de profil */
            div[data-testid="stPopover"] > button {
                border-radius: 50% !important;
                width: 45px !important;
                height: 45px !important;
                display: flex;
                align-items: center;
                justify-content: center;
                border: 1px solid #e2e8f0 !important;
                background-color: #f8fafc !important;
            }
        </style>
    """, unsafe_allow_html=True)


def login_header():
    """Header avec menu de connexion escamotable (Popover)."""
    # On aligne le titre et l'icône sur une seule ligne
    col_title, col_auth = st.columns([0.9, 0.1])

    with col_title:
        st.markdown("")

    with col_auth:
        if not st.session_state.get("is_logged_in", False):
            # Onglet escamotable avec icône cadenas/profil
            with st.popover("👤"):
                st.markdown("#### Connexion")
                email = st.text_input("Email autorisé", placeholder="nom@exemple.com", key="email_auth")
                if st.button("Valider l'accès", use_container_width=True):
                    if email in st.secrets["auth"]["allowed_emails"]:
                        st.session_state["is_logged_in"] = True
                        st.session_state["user_email"] = email
                        st.success("Accès accordé !")
                        st.rerun()
                    else:
                        st.error("Email non autorisé")
        else:
            # Menu de profil si connecté
            with st.popover("🟢"):
                st.markdown(f"**Session :** \n\n {st.session_state['user_email']}")
                if st.button("Se déconnecter", type="primary", use_container_width=True):
                    st.session_state["is_logged_in"] = False
                    st.rerun()

    st.markdown("")