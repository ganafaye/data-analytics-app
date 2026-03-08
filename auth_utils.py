import streamlit as st


def apply_custom_style():
    """Style pour masquer la navigation native et épurer le header."""
    st.markdown("""
            <style>
                /* 1. SUPPRIMER LE VIDE EN HAUT DE PAGE */
                .block-container {
                    padding-top: 1rem !important; /* Réduit la marge du haut */
                    padding-bottom: 0rem !important;
                    max-width: 95% !important; /* Utilise mieux la largeur de l'écran */
                }

                /* 2. MASQUER LE MENU NATIF */
                [data-testid="stSidebarNav"] { display: none; }

                /* 3. STYLE COMPACT POUR LE HEADER AUTH */
                .auth-header-container {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 5px 15px;
                    background-color: #ffffff;
                    border-bottom: 1px solid #e2e8f0;
                    margin-bottom: 20px;
                }

                /* 4. REDUIRE LA TAILLE DES INPUTS DANS LE HEADER */
                div[data-testid="stHorizontalBlock"] {
                    align-items: center;
                }
            </style>
        """, unsafe_allow_html=True)


def is_authorized():
    """Vérifie l'état de connexion."""
    return st.session_state.get("is_logged_in", False)


def login_header():
    """Affiche un header très fin avec logo à gauche et login à droite."""
    # On crée 3 colonnes : Titre (large), Vide (milieu), Login (étroit)
    col_title, col_spacer, col_auth = st.columns([2, 1, 1.5])

    with col_title:
        st.markdown("")

    with col_auth:
        if not is_authorized():
            # On utilise un container pour grouper l'input et le bouton
            c1, c2 = st.columns([2, 1])
            with c1:
                email = st.text_input("Accès", placeholder="Email", label_visibility="collapsed", key="email_auth")
            with c2:
                btn = st.button("Log 🔐")

            if btn:
                if email in st.secrets["auth"]["allowed_emails"]:
                    st.session_state["is_logged_in"] = True
                    st.session_state["user_email"] = email
                    st.rerun()
                else:
                    st.error("Inconnu")
        else:
            c1, c2 = st.columns([2, 1])
            with c1:
                st.caption(f"🟢 {st.session_state['user_email']}")
            with c2:
                if st.button("S'en aller"):
                    st.session_state["is_logged_in"] = False
                    st.rerun()
    st.markdown("---")  # Ligne de séparation fine