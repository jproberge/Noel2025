import streamlit as st
import time

# Config de la page
st.set_page_config(page_title="Mission: Top Secret", page_icon="🕵️‍♀️")

# Titre stylisé
st.title("📟 Terminal de Mission v2.0")

# Initialiser l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Premier message du bot
    st.session_state.messages.append({"role": "assistant", "content": "Identité confirmée. Agent Julianne, êtes-vous prête pour votre briefing ?"})

# Afficher les messages précédents
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Logique de réponse
if prompt := st.chat_input("Votre réponse..."):
    # Afficher le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse du bot (Logique simple ou arbres de décision)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # --- ICI TA LOGIQUE DE JEU ---
        if "oui" in prompt.lower() or "prête" in prompt.lower():
            response = "Excellent. Voici le dilemme : Si vous aviez 800$ et un weekend, choisiriez-vous A) Un nouvel aspirateur ou B) Une escapade de luxe ?"
        elif "b" in prompt.lower() or "escapade" in prompt.lower():
            response = "Bon choix. Analyse des paramètres... Destination trouvée : Lac-à-l'Eau-Claire. Génération du laissez-passer..."
            # C'est ici que tu mettras le lien vers le Wallet
        else:
            response = "Réponse non reconnue par le protocole. Veuillez réessayer."
        # -----------------------------

        # Effet de frappe "typewriter" pour faire cool
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
