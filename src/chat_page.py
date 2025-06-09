import streamlit as st

def chat_page():
    st.title("聊天助手")

    # Initialize chat components
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Create chat interface
    chat_container = st.container()

    # Display conversation history
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("輸入您的問題"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # 創建一個空的容器來放置即時更新的文字
            message_placeholder = st.empty()
            
            try:
                # 使用 streaming 生成回應
                full_response = ""
                
                for response_chunk in st.session_state.chat_setting.generate_response_stream(prompt):
                    full_response = response_chunk
                    # 即時更新顯示的內容
                    message_placeholder.markdown(full_response + "▌")  # 加上游標效果
                
                # 移除游標，顯示最終結果
                message_placeholder.markdown(full_response)
                
                # 儲存完整回應到對話歷史
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                error_msg = f"處理請求時出錯: {str(e)}"
                message_placeholder.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})