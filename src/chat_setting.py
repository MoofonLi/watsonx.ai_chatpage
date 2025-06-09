import os
import requests
import json
from dotenv import load_dotenv
import streamlit as st
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

load_dotenv()

class ChatSetting:
    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.deployment_id = os.getenv("LLM_DEPLOYMENT_ID")
        
        if not self.api_key or not self.deployment_id:
            raise ValueError("Missing WATSONX_API_KEY or LLM_DEPLOYMENT_ID")
        
        # 初始化 IAM Authenticator
        self.authenticator = IAMAuthenticator(
            apikey=self.api_key,
            url='https://iam.cloud.ibm.com/identity/token'
        )
        
        # API URL
        self.api_url = f"https://eu-de.ml.cloud.ibm.com/ml/v4/deployments/{self.deployment_id}/ai_service_stream?version=2021-05-01"
            
    def _get_headers(self):
        """獲取包含認證 token 的 headers"""
        try:
            # IAMAuthenticator 會自動處理 token 獲取和刷新
            token = self.authenticator.token_manager.get_token()
            
            return {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        except Exception as e:
            st.error(f"Failed to get authentication token: {str(e)}")
            return None
    
    def generate_response(self, user_message: str) -> str:
        """生成完整回應（非串流）"""
        try:
            # 使用串流方法但收集完整結果
            full_response = ""
            for response_chunk in self.generate_response_stream(user_message):
                full_response = response_chunk
            
            return full_response
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return "抱歉，處理您的請求時出現錯誤。"

    def generate_response_stream(self, user_message: str):
        """生成串流回應 - 返回生成器供 Streamlit 即時顯示"""
        try:
            headers = self._get_headers()
            if not headers:
                yield "無法獲取認證 token，請稍後再試。"
                return
            
            # 構建 payload
            payload = {
                "messages": [
                    {
                        "role": "user", 
                        "content": user_message
                    }
                ]
            }
            
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                stream=True,
                timeout=30  # 加上 timeout
            )
            
            if response.status_code == 401:
                # Token 可能過期，IAMAuthenticator 會自動刷新
                # 重新獲取 headers 並重試
                headers = self._get_headers()
                if headers:
                    response = requests.post(
                        self.api_url,
                        json=payload,
                        headers=headers,
                        stream=True,
                        timeout=30
                    )
            
            if response.status_code != 200:
                yield f"API Error: {response.status_code} - {response.text}"
                return
            
            # 處理 streaming response，即時 yield 每個 chunk
            collected_response = ""
            
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    
                    if line_text.startswith("data: "):
                        try:
                            json_str = line_text[6:]
                            
                            if json_str.strip() == "[DONE]":
                                break
                                
                            data = json.loads(json_str)
                            
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    collected_response += content
                                    # 即時 yield 新內容
                                    yield collected_response
                                    
                        except json.JSONDecodeError:
                            continue
            
            # 如果沒有收到任何內容
            if not collected_response:
                yield "Sorry, I couldn't generate a response."
            
        except Exception as e:
            yield f"抱歉，處理您的請求時出現錯誤: {str(e)}"