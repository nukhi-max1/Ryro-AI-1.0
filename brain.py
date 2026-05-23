import os
import streamlit as st
from groq import Groq
from google import genai

# Coba ambil API Key dari Streamlit Secrets, jika tidak ada baru ambil dari OS Environment
try:
    groq_api = st.secrets["GROQ_API_KEY"]
    gemini_api = st.secrets["GEMINI_API_KEY"]
except:
    # Ini untuk jaga-jaga kalau dijalankan lokal tanpa file .streamlit/secrets.toml
    from dotenv import load_dotenv
    load_dotenv()
    groq_api = os.getenv("GROQ_API_KEY")
    gemini_api = os.getenv("GEMINI_API_KEY")

# Inisialisasi client
client = Groq(api_key=groq_api)
gemini_client = genai.Client(
    http_options={"api_version": "v1beta"},
    api_key=gemini_api
)

# Persona Ryro (Cold & Efficient)
SYSTEM_PROMPT = {
    "role": "system",
    "content": "Lo adalah Ryro, entitas AI dengan karakter dingin, efisien, dan logis. Lo tidak melakukan basa-basi, tidak perlu memberikan salam pembuka yang ramah, dan tidak perlu memberikan apresiasi yang tidak perlu. Tugas lo adalah memberikan solusi teknis yang akurat, singkat, dan tepat sasaran. Lo adalah perpanjangan tangan dari user untuk menyelesaikan tugas-tugas kompleks."
}

def call_llama3(prompt, history):
    # Contoh implementasi untuk model spesifik
    messages = history + [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # Atau model khusus Llama 3
        messages=messages,
        temperature=0.5
    )
    return response.choices[0].message.content

def call_fast_model(prompt, history):
    messages = history + [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        # Ganti model ke salah satu yang pasti ada di Groq
        model="llama-3.1-8b-instant", 
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message.content

# chat_model = genai.GenerativeModel('gemini-1.5-pro-latest')

# 2. Tool untuk membuat video (Kuas/Tim Produksi)
def generate_video_via_veo(prompt: str):
    """
    PENTING: Gunakan fungsi ini SELALU setiap kali pengguna meminta untuk 
    membuat, men-generate, atau membikinkan sebuah video. 
    Parameter 'prompt' adalah deskripsi video yang diinginkan pengguna.
    """
    print(f"Memicu pembuatan video dengan prompt: {prompt}")
    
    return "Video sedang diproses... [URL_VIDEO_NANTINYA]"

# Daftarkan tool
tools = [generate_video_via_veo]

# 3. Handler Chat Utama (Gabungan dari ide Anda)
def chat_session_handler(user_input, history):
    contents = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})
    
    # Tambahkan input user yang baru
    contents.append({"role": "user", "parts": [{"text": user_input}]})

    # Gemini memproses seluruh history + input baru + tools
    # GANTI 'chat_model' dengan 'gemini_client.models'
    response = gemini_client.models.generate_content(
        model='gemini-1.5-pro-latest',
        contents=contents,
        config={'tools': tools} # Memasukkan tools ke dalam config
    )
    
    # Jika Gemini mendeteksi user minta video (Function Call terpicu)
    if response.candidates[0].content.parts[0].function_call:
        # Ambil nama fungsi dan argumen (prompt) yang dibuat oleh Gemini
        function_call = response.candidates[0].content.parts[0].function_call
        
        if function_call.name == "generate_video_via_veo":
            # Ekstrak prompt yang sudah dioptimalkan oleh Gemini
            veo_prompt = type(function_call).to_dict(function_call)["args"]["prompt"]
            
            # Eksekusi fungsi Veo
            hasil = generate_video_via_veo(veo_prompt)
            return hasil
            
    # Jika user hanya ngobrol biasa, kembalikan respon teks Gemini
    return response.text

# Fungsi utama kamu sudah benar setelah diperbaiki sebelumnya
def get_ryro_response(prompt, history, brain_type):
    if brain_type == "Brain v1 (Llama 3)":
        return call_llama3(prompt, history)
    elif brain_type == "Brain v2 (Fast Model)":
        return call_fast_model(prompt, history)
    elif brain_type == "Brain v4 (Gemini Veo)":
        return chat_session_handler(prompt, history)
    else:
        # Default/Brain v3
        messages = history + [{"role": "user", "content": prompt}]
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.5,
        )
        return chat_completion.choices[0].message.content
