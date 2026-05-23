import streamlit as st
import time
from ui_config import set_ryro_theme
from brain import get_ryro_response
import io
from fpdf import FPDF

def handle_commands(command):
    # Gabungkan semua perintah di sini
    
    # 1. Perintah Help
    if command == "!help":
        st.sidebar.info("Command Tersedia:\n!reset - Hapus semua chat\n!status - Cek info sistem\n!export - Download chat (.txt)")
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
        
    # 4. Perintah Export
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

    elif command == "!debug":
        # 1. Kumpulkan data diagnostik
        msg_count = len(st.session_state.get('messages', []))
        log_content = f"""RYRO AI - SYSTEM DEBUG LOG
-----------------------------
Timestamp: 22 May 2026
Chat History count: {msg_count}
Session State: ACTIVE
Glassmorphism Status: ENABLED
System Version: 1.0.4-Stable
-----------------------------
All systems nominal.
"""
        # 2. Buat file .txt untuk di-download
        buffer = io.StringIO(log_content)
        st.download_button(
            label="🛠️ Download Debug Log (.txt)",
            data=buffer.getvalue(),
            file_name="Ryro_Debug_Log.txt",
            mime="text/plain"
        )
        st.success("Diagnosa selesai. Klik tombol di atas untuk unduh log.")
        return True
    
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
                # Encode konten ke latin-1 untuk menghindari error karakter spesial
                pdf.multi_cell(0, 10, txt=f"{role}: {content}".encode('latin-1', 'replace').decode('latin-1'))
                pdf.ln(2)
            
            # AMBIL OUTPUT SEBAGAI BYTES
            pdf_bytes = pdf.output(dest='S')
            
            # Pastikan ini dalam format bytes
            if isinstance(pdf_bytes, bytearray):
                pdf_bytes = bytes(pdf_bytes)
            
            st.download_button(
                label="📄 Unduh Laporan PDF",
                data=pdf_bytes,
                file_name="Ryro_Report.pdf",
                mime="application/pdf"
            )
        return True

st.set_page_config(
    page_title="Ryro AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

set_ryro_theme()


# 1. INISIALISASI SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- PINDAHKAN SIDEBAR KE SINI (Di luar IF) ---
with st.sidebar:
    st.title("Ryro Terminal")
    st.markdown("---")
    st.info("Status: **Online**")
    st.write("Model: llama-3.3-70b-versatile")
    st.markdown("---")
    if st.button("Reset Session"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN UI ---
status_placeholder = st.empty()

def stream_response(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.05)

def update_status(mode="active"): # Kita set default ke "active"
    if mode == "thinking":
        status_placeholder.markdown('<div class="status-container"><div class="led led-orange led-pulse"></div>Ryro sedang berpikir...</div>', unsafe_allow_html=True)
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

brain_options = ["Brain V1 Claude Haiku", "Brain V2 Fast Model", "Brain V3 Ryro Ultimate", "Brain V4 (Gemini Veo)"]
selected_brain = st.selectbox("Pilih Otak:", brain_options, label_visibility="collapsed")

# Simpan pilihan ke session_state agar tidak lupa
st.session_state.current_brain = selected_brain

# PROSES INPUT
if prompt := st.chat_input("Perintah:", key="user_input"):
    if prompt.startswith("!"):
        if handle_commands(prompt.lower()):
            st.stop()
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    update_status(mode="thinking") # Ganti jadi oren saat proses
    response = get_ryro_response(prompt, st.session_state.messages[:-1], selected_brain)
    update_status(mode="active") # Balik ke biru setelah selesai
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write_stream(stream_response(response))