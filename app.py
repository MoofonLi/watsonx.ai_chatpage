import streamlit as st
from src.chat_page import chat_page
from src.chat_setting import ChatSetting

def main():
    st.set_page_config(
        page_title="watsonx.ai 聊天系統",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.session_state.chat_setting = ChatSetting()

    # 呼叫頁面
    chat_page()

if __name__ == "__main__":
    main()