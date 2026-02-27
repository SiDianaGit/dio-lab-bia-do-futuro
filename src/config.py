import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega as variáveis do arquivo .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def configure_api():
    """Configura a chave da API do Gemini."""
    if not GEMINI_API_KEY:
        raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env")
    genai.configure(api_key=GEMINI_API_KEY)
