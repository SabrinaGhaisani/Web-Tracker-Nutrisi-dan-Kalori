import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# ====== Konfigurasi Layout & Logo ======
st.set_page_config(
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
