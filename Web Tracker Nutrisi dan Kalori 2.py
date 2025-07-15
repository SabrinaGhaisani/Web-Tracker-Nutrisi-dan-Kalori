import streamlit as st

# Header halaman
st.set_page_config(page_title="Tracker Nutrisi", layout="centered")
st.title("🍽️ Tracker Nutrisi dan Kalori")
st.write("Web Tracker Kebutuhan Nutrisi dan Kalori Harianmu")

st.markdown("---")

# Form input data diri
st.header("📝 Input Data Diri")
nama = st.text_input("Nama")
gender = st.radio("Gender", ["Perempuan", "Laki-laki"])
umur = st.number_input("Umur (tahun)", min_value=0)
tinggi = st.number_input("Tinggi Badan (cm)", min_value=0)
berat = st.number_input("Berat Badan (kg)", min_value=0)
aktivitas = st.selectbox("Aktivitas Harian", ["Sedentari", "Ringan", "Sedang", "Berat", "Sangat Berat"])
