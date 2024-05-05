import streamlit as st
from streamlit_option_menu import option_menu
from chatbot import chat_bot

def main():
# Sidebar image
    st.sidebar.image('img/Hey_Banco.svg')

    # Sidebar menu
    with st.sidebar:
        choice = option_menu("", ['Hey, Now'], 
            icons=['robot'], menu_icon="list", default_index=0,
            styles={
        "container": {"padding": "5!important", "background-color": "#fcec02"},
        "icon": {"color": "#231f20", "font-size": "25px"}, 
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "color": "#231f20"},
        "nav-link-selected": {"background-color": "#fcec02"},}
            )

    if choice == "Hey, Now":
        chat_bot()

# Execute main and stating message states for the session
if __name__ == "__main__":
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []
    
    main()