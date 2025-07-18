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
