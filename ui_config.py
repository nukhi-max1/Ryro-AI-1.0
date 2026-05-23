import streamlit as st

def set_ryro_theme():
    st.markdown("""
        <style>
        /* 1. Sembunyikan HANYA tombol Deploy & Menu (Titik Tiga) */
        [data-testid="stToolbar"] {
            display: none !important;
        }
                
        /* Membuat background selectbox transparan/gelap */
        [data-testid="stSelectbox"] > div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        }
        
        /* Sembunyikan dekorasi pelangi */
        [data-testid="stDecoration"] {
            display: none !important;
        }

        /* 2. Biarkan header hidup tapi transparan */
        header {
            background: transparent !important;
        }

        /* 3. BAJAK TOMBOL SIDEBAR ASLI & PINDAHKAN KE BAWAH! */
        /* Kita menggunakan tombol bawaan Streamlit, cuma pindah tempat */
        [data-testid="collapsedControl"] {
            position: fixed !important;
            top: auto !important;          /* Matikan posisi atas */
            left: auto !important;         /* Matikan posisi kiri */
            bottom: 33px !important;       /* Sejajar dengan input chat */
            right: 65px !important;        /* Di sebelah tombol panah kirim */
            z-index: 999999 !important;
            background-color: #161b22 !important;
            border: 1px solid #30363d !important;
            border-radius: 8px !important;
            display: flex !important;      /* Pastikan tombol terlihat */
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.3s ease;
        }

        /* Efek Hover untuk tombol yang dibajak */
        [data-testid="collapsedControl"]:hover {
            background-color: #30363d !important;
            border-color: #007bff !important;
        }

        /* 4. LOGO RYRO TETAP AMAN DI KANAN ATAS */
        .ryro-logo {
            position: fixed;
            top: 15px;
            right: 20px;
            font-size: 20px;
            font-weight: bold;
            color: #007bff;
            z-index: 99999;
            pointer-events: none;
        }

        /* --- TEMA UTAMA --- */
        @keyframes fadeInPulse {
            0% { background-color: #0d1117; }
            50% { background-color: #121820; }
            100% { background-color: #0d1117; }
        }

        .stApp { 
            animation: fadeInPulse 4s ease-out forwards;
            animation-iteration-count: 1;
            background-color: #0d1117; 
            color: #c9d1d9; 
        }

        /* Chat bubble */
        [data-testid="stChatMessage"] { 
            background-color: #161b22; 
            border-left: 3px solid #007bff; 
        }

        /* Input Styling */
        .stChatInput {
            border: 1px solid #30363d !important;
            border-radius: 8px;
            box-shadow: none !important;
        }
        .stChatInput:focus-within {
            border: 1px solid #007bff !important;
        }
        .stChatInput textarea {
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            padding-right: 120px !important; /* Ruang biar teks ga nabrak tombol */
        }
        .stChatInput > div {
            border-color: #30363d !important;
        }

        /* Sembunyikan Avatar */
        [data-testid="stChatMessageAvatarUser"],
        [data-testid="stChatMessageAvatarAssistant"] {
            display: none !important;
        }
        [data-testid="stChatMessageContent"] {
            margin-left: 0 !important;
        }

        /* Tombol Kirim */
        div[data-testid="stChatInput"] button {
            background-color: #007bff !important;
            z-index: 999999 !important;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0d1117 !important;
            border-right: 1px solid #30363d;
        }
        [data-testid="stSidebarContent"] {
            padding: 20px;
        }
                
        /* 1. Efek Glassmorphism untuk Input Bar */
        .stChatInput {
            background: rgba(22, 27, 34, 0.4) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
        }

        /* 2. Efek Glassmorphism untuk Sidebar */
        [data-testid="stSidebar"] {
            background: rgba(13, 17, 23, 0.6) !important;
            backdrop-filter: blur(20px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }

        /* 3. Efek Hover/Klik yang elegan */
        .stChatInput:focus-within {
            background: rgba(22, 27, 34, 0.6) !important;
            border: 1px solid rgba(0, 123, 255, 0.4) !important;
            box-shadow: 0 0 20px rgba(0, 123, 255, 0.1) !important;
        }
                
        /* 1. Efek Glassmorphism untuk Tombol Pengiriman */
        div[data-testid="stChatInput"] button {
            background: rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(5px) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }

        /* 2. Efek Hover/Klik yang lebih cantik */
        div[data-testid="stChatInput"] button:hover {
            background: rgba(0, 123, 255, 0.3) !important;
            border: 1px solid rgba(0, 123, 255, 0.5) !important;
        }
                
        /* Tambahkan di st.markdown css lo */
        .stDownloadButton button {
            background: rgba(0, 123, 255, 0.2) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(0, 123, 255, 0.4) !important;
            color: white !important;
        }
                
        /* Styling tambahan untuk konten Debug di sidebar */
        [data-testid="stSidebar"] code {
            background: rgba(0, 0, 0, 0.3) !important;
            color: #00ff00 !important; /* Warna terminal hijau klasik */
            border-radius: 5px;
            padding: 10px;
        }
        [data-testid="stSidebar"] h3 {
            color: #007bff !important;
            font-family: monospace;
        }
                
        .led {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        }
        .led-blue { background-color: #007bff; box-shadow: 0 0 8px #007bff; }
        .led-orange { background-color: #fd7e14; box-shadow: 0 0 8px #fd7e14; }
        .led-gray { background-color: #6c757d; }
        
        .led-pulse {
            animation: pulse-animation 1.5s infinite;
        }
        
        @keyframes pulse-animation {
            0% { opacity: 1; }
            50% { opacity: 0.3; }
            100% { opacity: 1; }
        }
        
        .status-container {
            display: flex;
            align-items: center;
            font-family: sans-serif;
            font-size: 14px;
        }
                
        /* Mengubah warna border saat selectbox diklik/aktif */
        [data-testid="stSelectbox"] > div[data-baseweb="select"] > div {
            border-color: #007bff !important; 
        }
        
        /* Mengubah warna fokus agar tidak merah */
        div[data-baseweb="select"] > div:focus-within {
            border-color: #007bff !important;
            box-shadow: 0 0 0 1px #007bff !important;
        }
        </style>
        
        <div class="ryro-logo">Ryro AI</div>
    """, unsafe_allow_html=True)