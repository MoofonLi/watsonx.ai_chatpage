import streamlit as st
from src.chat_page import chat_page
from src.chat_setting import ChatSetting

def main():
    st.set_page_config(
        page_title="watsonx.ai 聊天系統",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 初始化 WatsonX Client
    if 'watsonx_client' not in st.session_state:
        try:
            st.session_state.chat_setting = ChatSetting()
        except Exception as e:
            st.error(f"無法初始化 WatsonX Client: {str(e)}")
            return

    # 呼叫頁面
    chat_page()

if __name__ == "__main__":
    main()