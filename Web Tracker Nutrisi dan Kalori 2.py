import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# ========== KONFIGURASI AWAL ==========
st.set_page_config(page_title="Web Tracker Nutrisi dan Kalori", layout="centered")

# ✅ TAMBAHIN CSS DI SINI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #f7fff8;
        color: #2e2e2e;
    }

    .stButton>button {
        background-color: #a8e6cf;
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.4em 1em;
    }

    .stButton>button:hover {
        background-color: #81c784;
        color: white;
    }

    .stSidebar {
        background-color: #e5fce7;
    }
    </style>
""", unsafe_allow_html=True)

    page_title="NutriTrack - Web Tracker Nutrisi & Kalori",
    layout="wide",
)

# ====== Logo & Warna (custom style sederhana) ======
st.markdown("""
    <style>
        body {
            background-color: #f5fff5;
        }
        .sidebar .sidebar-content {
            background-color: #e0f7e9;
        }
        h1, h2, h3, h4 {
            color: #317256;
        }
    </style>
""", unsafe_allow_html=True)

# ====== Sidebar Navigasi ======
menu = st.sidebar.radio(
    "Navigasi",
    ("🏠 Beranda", "📚 Pendahuluan Nutrisi", "📝 Kalkulator Nutrisi", "🍽️ Konsumsi Harian", "📊 Analisis & Riwayat")
)

# ====== Beranda ======
if menu == "🏠 Beranda":
    st.image("logo_nutracker.png", width=150)  # pastikan file ini ada di repo!
    st.title("NutriTrack")
    st.markdown("### Aplikasi Tracker Nutrisi dan Kalori Harian")
    st.write(
        """
        NutriTrack adalah aplikasi web berbasis Streamlit untuk membantu kamu memantau kebutuhan kalori dan zat gizi harian.
        Dengan tampilan simpel dan fitur interaktif, aplikasi ini cocok untuk semua kalangan—baik pelajar, mahasiswa, maupun masyarakat umum.
        """
    )
    st.success("Yuk mulai hidup sehat dari sekarang! Gunakan menu di sidebar untuk mulai.")
