import streamlit as st
from src.chat_page import chat_test_page
from src.token_manager import TokenManager

def main():
    st.set_page_config(
        page_title="watsonx.ai 聊天系統",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 初始化 Token Manager
    if 'token_manager' not in st.session_state:
        st.session_state.token_manager = TokenManager()
        if not st.session_state.token_manager.get_token():
            st.error("無法初始化 Token Manager")
            return

    # 呼叫頁面
    chat_test_page()

if __name__ == "__main__":
    main()
