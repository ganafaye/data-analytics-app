import streamlit as st


def apply_custom_style():
    """Design Glassmorphism et typographie moderne."""
    st.markdown("""
        <style>
            /* Import d'une police élégante */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

            html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
            }

            /* Masquer la navigation native */
            [data-testid="stSidebarNav"] { display: none; }

            /* Bouton Login : Effet Glass avec Gradient */
            div[data-testid="stSidebar"] div[data-testid="stPopover"] > button {
                background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
                color: white !important;
                border: none !important;
                padding: 12px !important;
                border-radius: 15px !important;
                font-weight: 600 !important;
                letter-spacing: 0.5px !important;
                box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
                transition: all 0.3s ease-in-out !important;
            }

            div[data-testid="stSidebar"] div[data-testid="stPopover"] > button:hover {
                transform: scale(1.02) !important;
                box-shadow: 0 6px 20px rgba(168, 85, 247, 0.4) !important;
            }

            /* Style des inputs à l'intérieur du popover */
            div[data-testid="stPopoverContent"] {
                background: rgba(255, 255, 255, 0.95) !important;
                backdrop-filter: blur(10px) !important;
                border-radius: 20px !important;
                border: 1px solid rgba(255, 255, 255, 0.18) !important;
            }
        </style>
    """, unsafe_allow_html=True)


def is_authorized():
    return st.session_state.get("is_logged_in", False)


def login_sidebar():
    """Interface de connexion avec design épuré et badge néon."""
    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    # Titre minimaliste avec icône
    st.sidebar.markdown("""
        <div style='padding: 10px 0px; margin-bottom: 20px;'>
            <h3 style='color: #1e293b; margin: 0; font-weight: 700;'>🛡️ Terminal d'accès</h3>
            <p style='color: #94a3b8; font-size: 0.75rem;'>Sécurisé par Gana Faye</p>
        </div>
    """, unsafe_allow_html=True)

    if not is_authorized():
        with st.sidebar.popover("🔑 Ouvrir la session"):
            st.markdown("#### Identification")
            email = st.text_input("Email", placeholder="admin@datalab.sn", key="email_auth")
            if st.button("Authentification", use_container_width=True):
                # CORRECTION ICI : On pointe sur st.secrets["auth"]["allowed_emails"]
                try:
                    allowed_list = st.secrets["auth"]["allowed_emails"]
                    if email in allowed_list:
                        st.session_state["is_logged_in"] = True
                        st.session_state["user_email"] = email
                        st.rerun()
                    else:
                        st.error("Accès refusé : email non autorisé.")
                except KeyError:
                    st.error("Erreur de configuration : section [auth] introuvable.")
    else:
        # BADGE DE SESSION TYPE "DASHBOARD"
        st.sidebar.markdown(f"""
            <div style='background: #ffffff; padding: 20px; border-radius: 20px; border: 1px solid #f1f5f9; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05);'>
                <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 10px;'>
                    <div style='background: #22c55e; width: 8px; height: 8px; border-radius: 50%; box-shadow: 0 0 10px #22c55e;'></div>
                    <span style='font-size: 0.65rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px;'>En ligne</span>
                </div>
                <p style='margin: 0; font-size: 0.9rem; font-weight: 600; color: #1e293b; word-break: break-all;'>{st.session_state['user_email']}</p>
            </div>
            <br>
        """, unsafe_allow_html=True)

        # Bouton déconnexion discret
        if st.sidebar.button("Terminer la session", use_container_width=True):
            st.session_state["is_logged_in"] = False
            st.rerun()