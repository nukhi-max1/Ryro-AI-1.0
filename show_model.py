import os
from groq import Groq
from dotenv import load_dotenv

# Memastikan API Key terbaca dari file .env
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("--- DAFTAR MODEL YANG TERSEDIA ---")
try:
    models = client.models.list()
    for model in models.data:
        print(f"Model ID: {model.id}")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")