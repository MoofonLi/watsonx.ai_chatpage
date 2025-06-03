import requests
import streamlit as st
import os
import json


class Assistant:
    def __init__(self, token_manager=None):
        self.token_manager = token_manager
        
        # API settings from .env
        self.url = os.getenv("LLM_API_URL")
        
        if not self.url:
            st.error("LLM_API_URL not found in environment variables")
    
    def _get_headers(self):
        token = self.token_manager.get_token()
        
        if not token:
            st.error("Unable to get WatsonX API Token")
            return None
            
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    
    def find_relevant_context(self, query: str) -> str:
        # API 已包含 RAG，返回空字符串
        return ""
    
    def generate_response(self, context: str, user_message: str) -> str:
        """Generate response using WatsonX LLM API"""
        headers = self._get_headers()
        if not headers:
            return None
        
        # 簡單的請求結構，因為 API 已經包含 prompt
        payload = {
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
        
        try:
            response = requests.post(self.url, json=payload, headers=headers, stream=True)
            
            if response.status_code != 200:
                st.error(f"API Error: {response.status_code}")
                return None
            
            # Handle streaming response
            collected_response = ""
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    if line_text.startswith("data: "):
                        try:
                            data = json.loads(line_text[6:])  # Remove "data: " prefix
                            
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                content = delta.get("content", "")
                                collected_response += content
                                
                        except json.JSONDecodeError:
                            continue
            
            return collected_response.strip() if collected_response else None
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None