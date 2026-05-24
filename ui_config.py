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

        /* 3. LOGO RYRO TETAP AMAN DI KANAN ATAS */
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
                
        /* Styling tombol download */
        .stDownloadButton button {
            background: rgba(0, 123, 255, 0.2) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(0, 123, 255, 0.4) !important;
            color: white !important;
        }
                
        /* Styling tambahan untuk konten Debug di sidebar */
        [data-testid="stSidebar"] code {
            background: rgba(0, 0, 0, 0.3) !important;
            color: #00ff00 !important; 
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
                
                /* 1. Gaya Cyberpunk: Sudut terpotong (Chamfered Edges) */
        div[data-testid="stExpander"] details summary, div[data-testid="stPopover"] button {
            background: linear-gradient(90deg, #151522 0%, #1e1e30 100%) !important;
            border: none !important;
            /* Teknik memotong bentuk kotak menjadi poligon kustom */
            clip-path: polygon(15% 0, 100% 0, 100% 75%, 85% 100%, 0 100%, 0 25%) !important;
            padding: 12px 20px !important;
            border-left: 4px solid #00a8ff !important; /* Aksen neon di kiri */
            color: #00a8ff !important;
            font-weight: bold !important;
            letter-spacing: 1px !important;
            transition: all 0.3s ease-in-out !important;
        }

        /* Efek hover Cyberpunk */
        div[data-testid="stExpander"] details summary:hover, div[data-testid="stPopover"] button:hover {
            background: #00a8ff !important;
            color: #151522 !important;
            border-left: 4px solid #ffffff !important;
            transform: scale(1.02) !important;
        }
                
                /* --- AREA DALAM UPLOADER (PILIH GAMBAR) --- */

        /* 1. Modifikasi area kotak utama (Dropzone) */
        div[data-testid="stFileUploader"] section {
            background-color: #12121c !important; /* Background super gelap */
            border: 1px solid #2a2a3d !important;
            border-left: 4px solid #00a8ff !important; /* Aksen garis neon biru di kiri nyamain tombol luar */
            border-radius: 4px !important; /* Sudut lebih tajam, nggak membulat pasaran */
            padding: 20px !important;
            box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.5) !important; /* Efek kedalaman (masuk ke dalam) */
            transition: all 0.3s ease !important;
        }

        /* Efek nyala pas kursor masuk atau lagi drag file ke area dropzone */
        div[data-testid="stFileUploader"] section:hover {
            border-color: #00a8ff !important;
            background-color: #171724 !important;
            box-shadow: inset 0 0 10px rgba(0, 168, 255, 0.1) !important;
        }

        /* 2. Modifikasi tombol "Upload" (Browse files) di bagian dalam */
        div[data-testid="stFileUploader"] button {
            background: transparent !important;
            border: 1px solid #00a8ff !important;
            color: #00a8ff !important;
            border-radius: 0px !important; /* Kotak kaku ala interface Sci-Fi */
            padding: 5px 20px !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            letter-spacing: 1.5px !important;
            transition: all 0.2s ease !important;
        }

        /* Efek nyala pas tombol Upload internal disorot */
        div[data-testid="stFileUploader"] button:hover {
            background: #00a8ff !important;
            color: #000000 !important;
            box-shadow: 0 0 12px rgba(0, 168, 255, 0.6) !important;
        }

        /* 3. Modifikasi teks limit (200MB per file...) biar kayak teks terminal */
        div[data-testid="stFileUploader"] small {
            color: #5c637a !important;
            font-family: 'Courier New', Courier, monospace !important;
            font-size: 0.8rem !important;
            letter-spacing: 0.5px !important;
            margin-top: 10px !important;
        }

        /* 4. Ubah warna icon awan bawaan Streamlit (opsional biar senada) */
        div[data-testid="stFileUploader"] svg {
            color: #00a8ff !important;
        }
                
                /* Bikin posisi Popover melayang (Fixed) di pojok kanan bawah */
        div[data-testid="stPopover"] {
            position: fixed !important;
            bottom: 30px !important;
            right: 30px !important;
            z-index: 1000 !important;
        }

        /* Kustomisasi bentuk tombolnya biar bulat, minimalis, & nyatu sama tema gelap Ryro */
        div[data-testid="stPopover"] button {
            border-radius: 50% !important;
            width: 55px !important;
            height: 55px !important;
            padding: 0 !important;
            background-color: #1E1E1E !important; /* Warna dasar gelap */
            border: 2px solid #00a8ff !important; /* Garis biru khas Ryro AI lu */
            color: white !important;
            font-size: 24px !important; /* Ukuran icon gear */
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5) !important;
            transition: all 0.3s ease-in-out !important;
        }

        /* Efek pas disorot mouse (Hover) */
        div[data-testid="stPopover"] button:hover {
            background-color: #00a8ff !important;
            box-shadow: 0 0 15px rgba(0, 168, 255, 0.7) !important;
            transform: scale(1.1) !important;
        }
        </style>
        
        <div class="ryro-logo">Ryro AI</div>
    """, unsafe_allow_html=True)
