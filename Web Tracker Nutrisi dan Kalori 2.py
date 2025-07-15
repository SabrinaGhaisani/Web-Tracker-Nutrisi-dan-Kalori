import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------ HALAMAN 1 ------------------------
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

# Tombol submit
if st.button("Lanjut ➡️"):
    st.success("Data berhasil disimpan!")

    # ------------------------ HALAMAN 2 ------------------------
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

    # Hitung kebutuhan nutrisi (standar umum)
    karbo = kalori * 0.5 / 4     # 1 gram karbo = 4 kkal
    lemak = kalori * 0.3 / 9     # 1 gram lemak = 9 kkal
    protein = kalori * 0.2 / 4   # 1 gram protein = 4 kkal

    st.markdown("### Rincian Kebutuhan Nutrisi Harian:")
    st.write(f"🍚 Karbohidrat: **{karbo:.1f} g**")
    st.write(f"🥩 Protein: **{protein:.1f} g**")
    st.write(f"🧈 Lemak: **{lemak:.1f} g**")

    # Pie Chart visualisasi
nutrisi_df = pd.DataFrame({
    'Nutrisi': ['Karbohidrat', 'Lemak', 'Protein'],
    'Gram': [karbo, lemak, protein]
})

fig, ax = plt.subplots()
ax.pie(nutrisi_df['Gram'], labels=nutrisi_df['Nutrisi'], autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)
