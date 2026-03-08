import streamlit as st


def apply_custom_style():
    """Réduit l'espace en haut et masque le menu natif."""
    st.markdown("""
        <style>
            /* Supprime la marge géante du haut */
            .block-container {
                padding-top: 0.5rem !important;
                padding-bottom: 0rem !important;
            }
            /* Masque la liste des fichiers dans la sidebar */
            [data-testid="stSidebarNav"] { display: none; }

            /* Style du bouton popover pour qu'il soit discret */
            div[data-testid="stPopover"] > button {
                border-radius: 20px !important;
                border: 1px solid #e2e8f0 !important;
                padding: 0px 15px !important;
                height: 35px !important;
            }
        </style>
    """, unsafe_allow_html=True)


def is_authorized():
    return st.session_state.get("is_logged_in", False)


def login_header():
    """Header compact avec popover à droite."""
    col1, col2 = st.columns([0.85, 0.15])

    with col1:
        st.subheader("")

    with col2:
        if not is_authorized():
            with st.popover("🔑 Login"):
                email = st.text_input("Email", placeholder="nom@exemple.com", key="email_auth")
                if st.button("Valider", use_container_width=True):
                    if email in st.secrets["auth"]["allowed_emails"]:
                        st.session_state["is_logged_in"] = True
                        st.session_state["user_email"] = email
                        st.rerun()
                    else:
                        st.error("Email refusé")
        else:
            with st.popover("👤"):
                st.write(f"Connecté: {st.session_state['user_email']}")
                if st.button("Déconnexion", type="primary", use_container_width=True):
                    st.session_state["is_logged_in"] = False
                    st.rerun()
    st.markdown("")