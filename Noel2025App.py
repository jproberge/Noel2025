import streamlit as st
from openai import OpenAI

# 1. Configuration de la page
st.set_page_config(page_title="Mission: Top Secret", page_icon="🕵️‍♀️")
st.title("📟 Terminal de Mission v2.1")

# 2. Gestion de la clé API (via les secrets Streamlit pour la sécurité)
# Si tu testes en local, tu peux mettre ta clé en dur ici temporairement, 
# mais sur le cloud, utilise st.secrets["OPENAI_API_KEY"]
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    # Fallback pour test local rapide (à ne pas commiter sur GitHub!)
    client = OpenAI(api_key="TA-CLE-ICI-POUR-TESTER")

# 3. LE CERVEAU : Le System Prompt (C'est ici que tu définis le jeu)
# On définit le comportement de l'IA. Elle ne doit pas dire qu'elle est une IA.
system_prompt = """
Tu es le 'Commandant Alpha', une IA d'agence d'espionnage. 
Ton interlocutrice est l'Agent Julianne (une planificatrice financière sportive).
Ton but : Lui faire passer un test de calibration avant de lui révéler sa mission de Noël.

Règles du jeu :
1. Sois mystérieux, un peu drôle, et utilise un jargon d'espion (ex: 'Recalibrage des capteurs', 'Analyse du niveau de stress').
2. Ne révèle PAS la destination tout de suite. Fais-la travailler un peu.
3. Pose-lui 2 ou 3 dilemmes moraux ou romantiques drôles (ex: choisir entre le ménage et le vin).
4. Si elle répond bien (réponses relax/fun), valide l'étape.
5. À la TOUTE FIN seulement, quand tu juges qu'elle est prête, annonce-lui :
   "Accès autorisé. Destination : Auberge du Lac-à-l'Eau-Claire. Préparez vos bagages pour le [Tes Dates]."
   Et ajoute le code secret : "WALLET_LINK_AUTHORIZED".
"""

# 4. Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []
    # On ajoute le system prompt (caché) pour conditionner l'IA
    st.session_state.messages.append({"role": "system", "content": system_prompt})
    # Premier message visible
    st.session_state.messages.append({"role": "assistant", "content": "Connexion établie... 📡 Identification : Agent Julianne. Confirmez-vous la réception ?"})

# 5. Affichage de la conversation (On cache le system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. Boucle de chat principale
if prompt := st.chat_input("Votre réponse..."):
    # Afficher le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Appel à l'API OpenAI
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # On envoie tout l'historique pour qu'il ait le contexte
        stream = client.chat.completions.create(
            model="gpt-4o-mini", # Ou gpt-3.5-turbo (moins cher et suffisant)
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        
        # Réception du flux (effet machine à écrire)
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                full_response += chunk.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
        
        # 7. Détection de la fin du jeu (Le Trigger)
        if "WALLET_LINK_AUTHORIZED" in full_response:
            st.success("🎉 MISSION DÉVERROUILLÉE !")
            st.link_button("Télécharger le Laisser-Passer (Wallet)", "TON_LIEN_PASS2U")
            st.balloons() # Petit effet festif Streamlit

    # Sauvegarder la réponse de l'IA
    st.session_state.messages.append({"role": "assistant", "content": full_response})
