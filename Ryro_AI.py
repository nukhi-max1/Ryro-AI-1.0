import streamlit as st
import time
from ui_config import set_ryro_theme
from brain import get_ryro_response
import io
from fpdf import FPDF
import google.generativeai as genai 
from PIL import Image # Library tambahan untuk memproses gambar dengan aman

# --- KONFIGURASI GEMINI VISION ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def analitik_gambar(prompt, image_bytes):
    """Fungsi Vision menggunakan PIL Image (Jauh lebih stabil dan anti-error 404)"""
    try:
        # Menyambungkan konfigurasi dari menu Settings secara real-time
        generation_config = {
            "temperature": st.session_state.temperature,
            "max_output_tokens": st.session_state.max_tokens,
        }
        
        # Menerapkan parameter dan System Prompt ke model Vision
        model = genai.GenerativeModel(
            'gemini-2.5-flash',
            generation_config=generation_config,
            system_instruction=st.session_state.system_prompt
        )
        
        # Mengubah bytes menjadi objek gambar PIL (Mime-type terdeteksi otomatis)
        img = Image.open(io.BytesIO(image_bytes))
        
        # Jalankan generasi konten
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"❌ Error saat membaca gambar: {e}\n\n*Tips: Pastikan kamu sudah menjalankan 'pip install -U google-generativeai' di terminal.*"

# --- HANDLER PERINTAH ---
def handle_commands(command):
    # 1. Perintah Help
    if command == "!help":
        st.sidebar.info("Command Tersedia:\n!reset - Hapus semua chat\n!status - Cek info sistem\n!export - Download chat (.txt)\n!export_pdf - Download PDF")
        return True
        
    # 2. Perintah Reset
    elif command == "!reset":
        st.session_state.messages = []
        st.rerun()
        return True
        
    # 3. Perintah Status
    elif command == "!status":
        st.toast("Ryro AI: System Online - Glassmorphism Active")
        return True
        
    # 4. Perintah Export TXT
    elif command == "!export":
        chat_data = st.session_state.get('messages', [])
        if not chat_data:
            st.warning("Tidak ada chat untuk diexport!")
        else:
            export_text = ""
            for msg in chat_data:
                export_text += f"{msg['role'].upper()}: {msg['content']}\n\n"
            
            buffer = io.StringIO(export_text)
            st.download_button(
                label="📥 Download Chat (.txt)",
                data=buffer.getvalue(),
                file_name="Ryro_Export.txt",
                mime="text/plain"
            )

    # 5. Perintah Debug
    elif command == "!debug":
        msg_count = len(st.session_state.get('messages', []))
        log_content = f"""RYRO AI - SYSTEM DEBUG LOG
-----------------------------
Timestamp: 24 May 2026
Chat History count: {msg_count}
Session State: ACTIVE
Glassmorphism Status: ENABLED
System Version: 1.0.4-Stable
-----------------------------
All systems nominal.
"""
        buffer = io.StringIO(log_content)
        st.download_button(
            label="🛠️ Download Debug Log (.txt)",
            data=buffer.getvalue(),
            file_name="Ryro_Debug_Log.txt",
            mime="text/plain"
        )
        st.success("Diagnosa selesai. Klik tombol di atas untuk unduh log.")
        return True
    
    # 6. Perintah Export PDF
    elif command == "!export_pdf":
        chat_data = st.session_state.get('messages', [])
        if not chat_data:
            st.warning("Tidak ada chat untuk diexport!")
        else:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Ryro AI - Transcript Export", ln=True, align='C')
            pdf.ln(10)
            
            pdf.set_font("Arial", size=12)
            for msg in chat_data:
                role = msg['role'].upper()
                content = msg['content']
                pdf.multi_cell(0, 10, txt=f"{role}: {content}".encode('latin-1', 'replace').decode('latin-1'))
                pdf.ln(2)
            
            pdf_bytes = pdf.output(dest='S')
            
            if isinstance(pdf_bytes, bytearray):
                pdf_bytes = bytes(pdf_bytes)
            
            st.download_button(
                label="📄 Unduh Laporan PDF",
                data=pdf_bytes,
                file_name="Ryro_Report.pdf",
                mime="application/pdf"
            )
        return True

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Ryro AI",
    layout="wide",
    initial_sidebar_state="expanded" 
)

set_ryro_theme()

# --- INISIALISASI SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inisialisasi variabel fitur Settings agar nilainya menetap di memori session
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "Kamu adalah Ryro AI, sebuah kecerdasan buatan dengan gaya kepribadian Cyberpunk yang asyik, solutif, ringkas, dan panggil user dengan sebutan Bro atau Kh."
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 2048

# --- SIDEBAR TERPUSAT ---
with st.sidebar:
    st.title("Ryro Terminal")
    st.markdown("---")
    
    with st.expander("ℹ️ Daftar Perintah Cepat"):
        st.caption("Ketik di kolom chat:")
        st.markdown("- `!help` - Bantuan\n- `!reset` - Hapus chat\n- `!export` - Unduh TXT\n- `!export_pdf` - Unduh PDF\n- `!debug` - Cek Log")
    
    if st.button("🔄 Reset Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    if st.button("📋 Copy History", use_container_width=True):
        if st.session_state.messages:
            chat_text = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.messages])
            st.code(chat_text, language=None)
            st.toast("Silakan copy teks di atas!")
        else:
            st.warning("Chat kosong.")
            
    st.markdown("---")
    st.info("Status: **Online**")
    st.write("Vision: Gemini 2.5 Active")

# --- MAIN UI ---
status_placeholder = st.empty()

def stream_response(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.05)

def update_status(mode="active"):
    if mode == "thinking":
        status_placeholder.markdown('<div class="status-container"><div class="led led-orange led-pulse"></div>Ryro sedang berpikir...</div>', unsafe_allow_html=True)
    elif mode == "vision":
        status_placeholder.markdown('<div class="status-container"><div class="led led-purple led-pulse"></div>Ryro sedang menganalisis gambar...</div>', unsafe_allow_html=True)
    elif mode == "active":
        status_placeholder.markdown('<div class="status-container"><div class="led led-blue"></div>Ryro siap.</div>', unsafe_allow_html=True)
    else:
        status_placeholder.markdown('<div class="status-container"><div class="led led-gray"></div>Ryro offline / Error.</div>', unsafe_allow_html=True)

update_status(mode="active")
st.title("Ryro AI")

# TAMPILKAN HISTORY CHAT
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "image_bytes" in msg and msg["image_bytes"]:
            st.image(msg["image_bytes"], width=300)

# --- PANEL KONTROL (Model Selector & Hapus Chat Sejajar) ---
col_brain, col_clear = st.columns([8.7, 1.3]) # Dibuat lebih lebar karena kolom settings dipindah

with col_brain:
    brain_options = ["Brain V1 Claude Haiku", "Brain V2 Fast Model", "Brain V3 Ryro Ultimate", "Brain V4 (Gemini Veo)"]
    selected_brain = st.selectbox("Pillow Otak:", brain_options, label_visibility="collapsed")
    st.session_state.current_brain = selected_brain

with col_clear:
    if st.button("🗑️", help="Bersihkan semua history chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- FLOATING SETTINGS POPOVER (Pojok Kanan Bawah & Minimalis) ---
st.markdown("""
<style>
/* Memaksa elemen Popover melayang fixed di layar kanan bawah */
div[data-testid="stPopover"] {
    position: fixed !important;
    bottom: 100px !important; /* Diberi jarak ke atas biar ga numpuk chat_input bar */
    right: 35px !important;
    z-index: 999999 !important;
}
/* Mengubah tombol bawaan popover jadi bulat minimalis ber-glow */
div[data-testid="stPopover"] button {
    border-radius: 50% !important;
    width: 50px !important;
    height: 50px !important;
    padding: 0 !important;
    background-color: #1a1c23 !important;
    border: 2px solid #00a8ff !important;
    color: #00a8ff !important;
    font-size: 20px !important;
    box-shadow: 0 4px 15px rgba(0, 168, 255, 0.3) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}
div[data-testid="stPopover"] button:hover {
    transform: scale(1.1) !important;
    box-shadow: 0 0 20px rgba(0, 168, 255, 0.6) !important;
    background-color: #00a8ff !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

with st.popover("⚙️"):
    st.markdown("### 🛠️ Ryro Settings")
    st.session_state["system_prompt"] = st.text_area(
        "System Prompt", 
        value=st.session_state.get("system_prompt", "Lo adalah Ryro..."),
        height=150
    )
    st.session_state["temperature"] = st.slider(
        "Temperature", 0.0, 1.0, 
        value=st.session_state.get("temperature", 0.7)
    )
    st.session_state["max_tokens"] = st.number_input(
        "Max Tokens", 
        value=st.session_state.get("max_tokens", 2048)
    )

# --- AREA INPUT (Terintegrasi Attachment Minimalis) ---
chat_box = st.chat_input(
    "Perintah / Tanya Ryro di sini...", 
    key="user_input", 
    accept_file=True, 
    file_type=["png", "jpg", "jpeg"]
)

# --- PROSES LOGIKA UTAMA ---
if chat_box:
    # Mengambil properti teks dan file dari objek chat_input versi baru
    prompt = chat_box.text
    files = chat_box.get("files", [])
    
    # 1. Cek perintah sistem
    if prompt and prompt.startswith("!"):
        if handle_commands(prompt.lower()):
            st.stop()
            
    # 2. Ambil bytes gambar jika diupload melalui icon minimalis di chat bar
    img_bytes = None
    if files:
        img_bytes = files[0].getvalue() # Mengambil file pertama yang dilampirkan
        
    # Antisipasi kalau user kirim gambar tapi lupa ngetik teks perintah
    if img_bytes and not prompt:
        prompt = "Jelaskan atau analisis gambar ini."
            
    # 3. Simpan ke history UI lokal (Termasuk metadata gambarnya jika ada)
    st.session_state.messages.append({"role": "user", "content": prompt, "image_bytes": img_bytes})
    with st.chat_message("user"):
        st.markdown(prompt)
        if img_bytes:
            st.image(img_bytes, width=300)

    # 4. Tentukan Mode Respon & Kirim Data
    if img_bytes:
        update_status(mode="vision")
        response = analitik_gambar(prompt, img_bytes)
    else:
        update_status(mode="thinking")
        
        # [PENTING] Sanitasi data history sebelum dikirim ke model teks (Mencegah Error 400 Bad Request)
        # Menghapus key 'image_bytes' agar struktur JSON murni teks 'role' dan 'content' saja
        clean_history = [
            {"role": msg["role"], "content": msg["content"]} 
            for msg in st.session_state.messages[-20:]
        ]
        
        response = get_ryro_response(prompt, clean_history, selected_brain)
        
    update_status(mode="active")
    
    # 5. Tampilkan balasan
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write_stream(stream_response(response))
