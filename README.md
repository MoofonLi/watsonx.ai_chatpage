##  Overview
This is a Streamlit-based chat application that integrates with IBM watsonx.ai LLM services.
### Environment Setup (Please download Python 3.11 first)
#### Mac
```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
#### Windows
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Running the Application
```bash
streamlit run app.py
```

### Environment Configuration
The application requires these environment variables (see .env_template):
- `WATSONX_API_KEY`: IBM Cloud API key for authentication
- `LLM_API_URL`: watsonx.ai deployment endpoint URL for streaming chat completion