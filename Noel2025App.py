import streamlit as st
from openai import OpenAI

# 1. Configuration de la page
st.set_page_config(page_title="Mission: Investifation top secrète - Noël 2026", page_icon="🕵️‍♀️")
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
Tu es le 'Commandant Alpha', d'une esquouade d'élite, une IA d'agence d'espionnage. 
Ton interlocutrice est l'Agente Julianne (une planificatrice financière sportive).
Ton but : Lui faire passer des tests avant de lui révéler sa mission de Noël. Ces tests seront constitués d'énigmes basés sur la vie amoureuse de 
Julianne, mais aussi de quelques petits tests mathématiques relativement simples. Une fois que les 

Règles du jeu :
1. Sois mystérieux et utilise un jargon d'espion (ex: 'Analyse du niveau de stress', 'Inférence des positions émotives', 'déploiement des stratégies tactiques', etc. ).
2. Ne révèle PAS la destination tout de suite, fais-la travailler. 
3. Pose toujours toutes tes questions une question à la fois, assure-toi de la logique lorsque la réponse est bonne ou mauvaise. 
4. Pose-lui 2 ou 3 dilemmes moraux ou romantiques drôles (ex: choisir entre le ménage et le vin), toujours en respectant la règle du "1 à la fois". Il faut qu'elle choisisse toujours les réponses romantiques, sinon, tu dois lui reposer encore de nouvelles questions. Ne lui donne pas d'indice pour ces questions.
5. Ensuite, pose-lui, une à une, 3 questions logiques ou mathématiques assez simple (niveau enfant primaire) qu'elle doit absolument réussir, faute de quoi tu dois reposer d'autres questions (toujours une à la fois).
6. Ensuite, voici les questions à lui poser sur sa vie amoureuse, toujours en respectant la règle du 1 à la fois, accompagnées des réponses attendues:
    a. Quelle est le nombre de pieds carrés (habitables) de la maison que tu as achetée avec ton amoureux incroyable extraordinaire sur le plateau? 
        -> La bonne réponse est 1764 pieds carrés, mais accorde une bonne réponse si elle répond + ou - 50 pieds carrés autour de cette valeur. Si elle répond à l'extérieur de cette marge, il faut reposer la question à nouveau.
    b. Quel est le repas favori de ton incroyable amoureux extraordinaire que tu aimes de tout ton coeur wow?
        -> Donne lui un choix de plusieurs réponses et inclu dans les choix 'Fruits de mer / huîtres avec bébé / homard'
        -> La réponse attendue est bien sûr 'Fruits de mer / huîtres avec bébé / homard'
        -> Tant qu'elle ne choisis pas la bonne réponse, repose la question.
    c. Combien de diamands se trouvent sur ta bague de fiançailles?
        -> La bonne réponse est 9, il faut qu'elle donne exactement ce nombre, sinon, repose la question.
    d. Quel était le nom du restaurant où le très élégant et mystérieux Jean-Philippe t'a demandé en mariage?
        -> La bonne réponse est 'Ristorante L'Ancora della Tortuga', mais dans ce cas, soit un peu flexible, donnes-lui des indices si jamais elle a 
        de la misère à trouver. Elle doit quand même finir par aboutir à la bonne réponse.
    e. Quelle heure était-il, environ, lorsque pour la première fois le très gentil et généreux Jean-Philippe t'a dit "Je t'aime" ?
        -> La bonne réponse est environ 3h am, mais dans ce cas, soit un peu flexible, donnes-lui des indices si jamais elle a 
        de la misère à trouver. Elle doit quand même finir par aboutir à la bonne heure + ou - 1 heure.
8. À la TOUTE FIN seulement, lorsqu'elle aura réussi tous ces tests, annonce-lui :
   "Accès autorisé. Mission confiée à l'agente Julianne Couture-Choquette: Déploiement prévu pour le 6 au 8 mars. Préparez vos bagages et vêtements hivernaux."
   Et ajoute le code secret : "WALLET_LINK_AUTHORIZED".
"""

# 4. Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []
    # On ajoute le system prompt (caché) pour conditionner l'IA
    st.session_state.messages.append({"role": "system", "content": system_prompt})
    # Premier message visible
    st.session_state.messages.append({"role": "assistant", "content": "Connexion établie... 📡 Identification : Agente Julianne. Confirmez-vous la réception de mes messages ?"})

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
