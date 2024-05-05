import streamlit as st
from streamlit_option_menu import option_menu
from chatbot import chat_bot

def main():
    # Sidebar menu
    with st.sidebar:
        choice = option_menu("Menú", ['HeyFTP'], 
            icons=['file-text'], menu_icon="list", default_index=0)

    if choice == "HeyFTP":
        chat_bot()

if __name__ == "__main__":
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []
    
    main()