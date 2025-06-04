import requests
import threading
import time
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

class TokenManager:
    def __init__(self):
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.token = None
        self.token_lock = threading.Lock()
        self.refresh_token()
        threading.Thread(target=self._scheduled_refresh, daemon=True).start()
    
    def refresh_token(self):
        try:
            with self.token_lock:
                response = requests.post(
                    'https://iam.cloud.ibm.com/identity/token',
                    data={
                        "apikey": self.api_key,
                        "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.token = data["access_token"]
                    return self.token
                else:
                    st.error(f"refresh token error: {response.status_code} - {response.text}")
                    return None
        except Exception as e:
            st.error(f"refresh token error: {str(e)}")
            return None
    
    def get_token(self):
        with self.token_lock:
            return self.token
    
    def _scheduled_refresh(self):
        while True:
            # refresh every 55 minutes
            time.sleep(55 * 60)
            
            try:
                self.refresh_token()
            except Exception as e:
                print(f"refresh token error: {str(e)}")