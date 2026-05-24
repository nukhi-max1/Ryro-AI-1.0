import base64
import os
import streamlit as st  # Untuk baca data dari Settings UI
from groq import Groq
from dotenv import load_dotenv
from google import genai
from google.genai import types
from datetime import datetime  # FITUR BARU: Buat baca waktu
import pytz  # FITUR BARU: Buat konversi ke zona waktu lokal (WIB)

load_dotenv()

# Inisialisasi client Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Inisialisasi client Gemini (Versi SDK Baru)
gemini_client = genai.Client(
    http_options={"api_version": "v1beta"},
    api_key=os.environ.get("GEMINI_API_KEY")
)

# Persona Ryro (Default fallback jika terjadi error di UI)
DEFAULT_SYSTEM_PROMPT = "Lo adalah Ryro, entitas AI dengan karakter dingin, efisien, dan logis. Lo tidak melakukan basa-basi, tidak perlu memberikan salam pembuka yang ramah, dan tidak perlu memberikan apresiasi yang tidak perlu. Tugas lo adalah memberikan solusi teknis yang akurat, singkat, dan tepat sasaran. Lo adalah perpanjangan tangan dari user untuk menyelesaikan tugas-tugas complexes."

def get_config():
    """Fungsi helper buat narik data konfigurasi + update WAKTU REAL-TIME secara live"""
    sys_prompt = st.session_state.get("system_prompt", DEFAULT_SYSTEM_PROMPT)
    temp = st.session_state.get("temperature", 0.5)
    max_tok = st.session_state.get("max_tokens", 2048)
    
    # --- PROSES INJEKSI WAKTU REAL-TIME ---
    tz_wib = pytz.timezone("Asia/Jakarta")
    waktu_sekarang = datetime.now(tz_wib).strftime("%A, %d %B %Y | %H:%M:%S WIB")
    
    # Gabungkan prompt asli dari UI dengan info waktu saat ini
    sys_prompt_with_time = (
        f"{sys_prompt}\n\n"
        f"[INFO SISTEM REAL-TIME]\n"
        f"Waktu Sekarang: {waktu_sekarang}\n"
        f"Gunakan info waktu di atas jika user menanyakan jam, hari, atau tanggal saat ini."
    )
    # --------------------------------------
    
    return sys_prompt_with_time, temp, max_tok

def clean_history_for_groq(history):
    """Fungsi helper untuk membersihkan parameter non-teks sebelum dikirim ke Groq"""
    cleaned = []
    for msg in history:
        cleaned.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    return cleaned

def call_llama3(prompt, history):
    sys_prompt, temp, max_tok = get_config()
    cleaned_history = clean_history_for_groq(history)
    
    messages = [{"role": "system", "content": sys_prompt}] + cleaned_history
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages, 
        temperature=temp,
        max_tokens=max_tok
    )
    return response.choices[0].message.content

def call_fast_model(prompt, history):
    sys_prompt, temp, max_tok = get_config()
    cleaned_history = clean_history_for_groq(history)
    
    messages = [{"role": "system", "content": sys_prompt}] + cleaned_history
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=messages,
        temperature=temp,
        max_tokens=max_tok
    )
    return response.choices[0].message.content

# Tool untuk membuat video (Kuas/Tim Produksi)
def generate_video_via_veo(prompt: str):
    """
    PENTING: Gunakan fungsi ini SELALU setiap kali pengguna meminta untuk 
    membuat, men-generate, atau membikinkan sebuah video. 
    """
    print(f"Memicu pembuatan video dengan prompt: {prompt}")
    return "Video sedang diproses... [URL_VIDEO_NANTINYA]"

tools = [generate_video_via_veo]

def encode_image_to_base64(uploaded_file):
    """Mengubah file gambar ke format base64 agar bisa dibaca model"""
    bytes_data = uploaded_file.getvalue()
    return base64.b64encode(bytes_data).decode('utf-8')

def analitik_gambar(prompt, image_bytes):
    """Mengirim gambar ke Gemini versi baru untuk dianalisis"""
    sys_prompt, temp, max_tok = get_config()
    
    config = types.GenerateContentConfig(
        system_instruction=sys_prompt,
        temperature=temp,
        max_output_tokens=max_tok
    )
    
    response = gemini_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type='image/jpeg',
            ),
            prompt
        ],
        config=config
    )
    return response.text

# Handler Chat Utama (Gabungan Gemini & Tool Call)
def chat_session_handler(user_input, history):
    sys_prompt, temp, max_tok = get_config()
    
    contents = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        if "content" in msg:
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    config = types.GenerateContentConfig(
        system_instruction=sys_prompt,
        temperature=temp,
        max_output_tokens=max_tok,
        tools=tools 
    )

    response = gemini_client.models.generate_content(
        model='gemini-2.5-pro',
        contents=contents,
        config=config 
    )
    
    if response.candidates and response.candidates[0].content.parts and response.candidates[0].content.parts[0].function_call:
        function_call = response.candidates[0].content.parts[0].function_call
        if function_call.name == "generate_video_via_veo":
            veo_prompt = type(function_call).to_dict(function_call)["args"]["prompt"]
            hasil = generate_video_via_veo(veo_prompt)
            return hasil
            
    return response.text

# Fungsi utama penentu router brain
def get_ryro_response(prompt, history, brain_type):
    if brain_type == "Brain V1 Claude Haiku" or brain_type == "Brain v1 (Llama 3)":
        return call_llama3(prompt, history)
    elif brain_type == "Brain V2 Fast Model" or brain_type == "Brain v2 (Fast Model)":
        return call_fast_model(prompt, history)
    elif brain_type == "Brain V4 (Gemini Veo)":
        return chat_session_handler(prompt, history)
    else:
        # Default/Brain V3 Ryro Ultimate
        sys_prompt, temp, max_tok = get_config()
        cleaned_history = clean_history_for_groq(history)
        
        messages = [{"role": "system", "content": sys_prompt}] + cleaned_history
        
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=temp,
            max_tokens=max_tok
        )
        return chat_completion.choices[0].message.content
