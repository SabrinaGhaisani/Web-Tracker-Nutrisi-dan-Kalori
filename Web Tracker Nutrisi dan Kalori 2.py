import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Web Tracker Nutrisi dan Kalori", layout="centered")

st.title("🍽️ Tracker Nutrisi dan Kalori")
st.write("Web Tracker Kebutuhan Nutrisi dan Kalori Harianmu")

st.header("📝 Input Data Diri")

nama = st.text_input("Nama")
gender = st.radio("Gender", ["Perempuan", "Laki-laki"])
umur = st.number_input("Umur (tahun)", min_value=0)
tinggi = st.number_input("Tinggi Badan (cm)", min_value=0.0)
berat = st.number_input("Berat Badan (kg)", min_value=0.0)
aktivitas = st.selectbox("Aktivitas Harian", ["Ringan (kerja duduk)", "Sedang (jalan kaki, berdiri)", "Berat (fisik/olahraga)"])

if st.button("Lanjut ➡️"):
    st.success("Data berhasil disimpan!")

    st.header("📊 Kebutuhan Kalori & Nutrisi Harian")

    # Hitung BMR
    if gender == "Perempuan":
        bmr = 447.6 + (9.25 * berat) + (3.1 * tinggi) - (4.33 * umur)
    else:
        bmr = 88.36 + (13.4 * berat) + (4.8 * tinggi) - (5.7 * umur)

    # Tambah faktor aktivitas
    if aktivitas == "Ringan (kerja duduk)":
        kalori = bmr * 1.2
    elif aktivitas == "Sedang (jalan kaki, berdiri)":
        kalori = bmr * 1.55
    else:
        kalori = bmr * 1.9

    st.subheader(f"Total Kebutuhan Kalori Harian: **{kalori:.0f} kkal**")

    # HITUNG MAKRO NUTRISI
    karbo = kalori * 0.5 / 4
    lemak = kalori * 0.3 / 9
    protein = kalori * 0.2 / 4

    st.markdown("### 🍱 Rincian Makronutrisi:")
    st.write(f"🍚 Karbohidrat: **{karbo:.1f} g**")
    st.write(f"🥩 Protein: **{protein:.1f} g**")
    st.write(f"🧈 Lemak: **{lemak:.1f} g**")

    nutrisi_df = pd.DataFrame({
        'Nutrisi': ['Karbohidrat', 'Lemak', 'Protein'],
        'Gram': [karbo, lemak, protein]
    })

    fig, ax = plt.subplots()
    ax.pie(nutrisi_df['Gram'], labels=nutrisi_df['Nutrisi'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    st.info("📌 AKG Makro: 50% Karbo, 30% Lemak, 20% Protein dari total kalori harian.")

    # ------------------ FIBER, GULA, SODIUM ------------------

    st.markdown("### 🧂 Gula, Serat, dan Sodium")

    # Nilai umum AKG
    gula = 50   # gram
    serat = 30  # gram
    sodium = 2000  # mg

    st.write(f"🍬 Gula maksimum per hari: **{gula} g**")
    st.write(f"🌾 Serat yang disarankan: **{serat} g**")
    st.write(f"🧂 Sodium maksimum: **{sodium} mg**")

    mikro_df = pd.DataFrame({
        'Nutrisi': ['Gula', 'Serat', 'Sodium'],
        'Nilai': [gula, serat, sodium / 1000]  # Konversi sodium ke gram
    })

    fig2, ax2 = plt.subplots()
    ax2.pie(mikro_df['Nilai'], labels=mikro_df['Nutrisi'], autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)

    st.info("📌 Catatan: Gula & Sodium adalah batas maksimum. Serat adalah target minimal.")

    # ------------------ SARAN MAKANAN ------------------

    st.markdown("### 🥗 Saran Makanan")

    st.write("**Karbohidrat:** nasi merah, roti gandum, oat, ubi")
    st.write("**Protein:** dada ayam, tempe, tahu, telur, ikan")
    st.write("**Lemak Sehat:** alpukat, kacang-kacangan, minyak zaitun")
    st.write("**Serat:** sayur hijau, buah apel/pear, brokoli")
    st.write("**Hindari konsumsi gula dan sodium berlebih dari makanan instan dan minuman manis.**")

