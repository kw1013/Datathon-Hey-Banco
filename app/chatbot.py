import streamlit as st
from data_pipeline import extract_topic, extract_sentiment
import time

def display_chatbot_conversation():
    for message in st.session_state.chatbot_messages:
        if message["sender"] == "User":
            st.write(f"Tu: {message['message']}")
        elif message["sender"] == "Chatbot":
            st.write(f"Hey,: {message['message']}")

def generate_response(user_input, topic, sentiment):
    # Determine custom text based on sentiment
    if sentiment == 'Positive':
        cust_text = 'muchas gracias por tu comentario'
    elif sentiment == 'Neutral':
        cust_text = 'hemos notado que has comentado'
    elif sentiment == 'Negative':
        cust_text = 'queremos ayudarte'
    
    sys_message = f"Hey, {cust_text} sobre {topic}. Queremos asegurarnos de que tengas la mejor experiencia, ¿tienes alguna pregunta?"

    for word in sys_message.split():
        yield word + ' '
        time.sleep(0.07)

def chat_bot():
    # Information about the discussion forum
    st.header('MVP: Hey, Now')
    st.subheader('Uso de manera proactiva en Twitter')

    logo_assistant = 'img/logo_hey_now.jpg'
    logo_user = 'img/logox.jpg'

    # Display chat messages from history on app rerun
    for message in st.session_state.chatbot_messages:
        if message['sender'] == 'assistant':
            with st.chat_message(message["sender"], avatar=logo_assistant):
                st.markdown(message["message"])
        elif message['sender'] == 'user':
            with st.chat_message(message["sender"], avatar=logo_user):
                st.markdown(message["message"])

    # Welcoming message
    if not st.session_state.chatbot_messages:
        with st.chat_message('assistant', avatar=logo_assistant):
            st.write(f"Esperando a tweet...")

    # Define use input
    user_input = st.chat_input("Tweet...")

    if user_input:
        # Add user message to the session state
        st.session_state.chatbot_messages.append({"sender": "User", "message": user_input})

        # Extract topic and sentiment
        topic = extract_topic(user_input)
        sentiment = extract_sentiment(user_input)

        # Generate a response from the chatbot (dummy response for illustration)
        bot_response = generate_response(user_input, topic, sentiment)

        st.session_state.chatbot_messages.append({"sender": "user", "message": user_input})

        # Display message in chat message container
        with st.chat_message('user', avatar=logo_user):
            st.write(user_input)

        # Display bot response in chat message container
        with st.chat_message('assistant', avatar=logo_assistant):
            bot_response = st.write_stream(generate_response(user_input, topic, sentiment))

        # Add bot response to the session state
        st.session_state.chatbot_messages.append({"sender": "assistant", "message": bot_response})