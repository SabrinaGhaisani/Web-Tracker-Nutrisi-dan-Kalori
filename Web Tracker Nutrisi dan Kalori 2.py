import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Web Tracker Nutrisi dan Kalori", layout="centered")

# ===================== STATE =====================
if "show_nutrisi" not in st.session_state:
    st.session_state.show_nutrisi = False
if "data_konsumsi" not in st.session_state:
    st.session_state.data_konsumsi = pd.DataFrame(columns=["Tanggal", "Makanan", "Kalori", "Protein", "Lemak", "Karbohidrat"])
if "hasil_perhitungan" not in st.session_state:
    st.session_state.hasil_perhitungan = {}

# ===================== SIDEBAR MENU =====================
st.sidebar.title("🧭 Navigasi")
menu = st.sidebar.radio("Pilih Halaman", [
    "📝 Input Data Diri",
    "📊 Kebutuhan Kalori & Nutrisi Harian",
    "🧾 Input Konsumsi Harian",
    "📈 Riwayat Kalori Harian & 📋 Analisis Konsumsi Harian",
    "🔬 Analisis Makronutrien vs Kebutuhan Harian"
])

# ===================== INPUT DATA DIRI =====================
if menu == "📝 Input Data Diri":
    st.header("📝 Input Data Diri")

    nama = st.text_input("Nama")
    gender = st.radio("Gender", ["Perempuan", "Laki-laki"])
    umur = st.number_input("Umur (tahun)", min_value=0)
    tinggi = st.number_input("Tinggi Badan (cm)", min_value=0.0)
    berat = st.number_input("Berat Badan (kg)", min_value=0.0)
    aktivitas = st.selectbox("Aktivitas Harian", ["Ringan (kerja duduk)", "Sedang (jalan kaki, berdiri)", "Berat (fisik/olahraga)"])

    if st.button("Lanjut ➡️"):
        st.session_state.show_nutrisi = True
        st.success("Data berhasil disimpan. Silakan buka halaman 📊 Kebutuhan Kalori & Nutrisi Harian.")

# ===================== HITUNG KEBUTUHAN NUTRISI =====================
elif menu == "📊 Kebutuhan Kalori & Nutrisi Harian":
    st.header("📊 Kebutuhan Kalori & Nutrisi Harian")

    if not st.session_state.show_nutrisi:
        st.warning("Silakan isi data diri terlebih dahulu di halaman 📝 Input Data Diri.")
    else:
        aktivitas_faktor = {"Ringan (kerja duduk)": 1.2, "Sedang (jalan kaki, berdiri)": 1.55, "Berat (fisik/olahraga)": 1.9}
        bmr = 10 * berat + 6.25 * tinggi - 5 * umur + (5 if gender == "Laki-laki" else -161)
        tdee = bmr * aktivitas_faktor[aktivitas]
        kebutuhan_protein = berat * 1.2
        kebutuhan_lemak = (0.25 * tdee) / 9
        kebutuhan_karbo = (tdee - (kebutuhan_protein * 4 + kebutuhan_lemak * 9)) / 4

        st.session_state.hasil_perhitungan = {
            "TDEE": tdee,
            "Protein": kebutuhan_protein,
            "Lemak": kebutuhan_lemak,
            "Karbohidrat": kebutuhan_karbo
        }

        st.write(f"**Total Kalori Harian (TDEE):** {tdee:.2f} kkal")
        st.write(f"**Protein:** {kebutuhan_protein:.2f} gram")
        st.write(f"**Lemak:** {kebutuhan_lemak:.2f} gram")
        st.write(f"**Karbohidrat:** {kebutuhan_karbo:.2f} gram")

# ===================== INPUT KONSUMSI =====================
elif menu == "🧾 Input Konsumsi Harian":
    st.header("🧾 Input Konsumsi Harian")

    tanggal = st.date_input("Tanggal", value=datetime.date.today())
    makanan = st.text_input("Nama Makanan")
    kalori = st.number_input("Kalori (kkal)", min_value=0.0)
    protein = st.number_input("Protein (g)", min_value=0.0)
    lemak = st.number_input("Lemak (g)", min_value=0.0)
    karbohidrat = st.number_input("Karbohidrat (g)", min_value=0.0)

    if st.button("Tambah Konsumsi"):
        st.session_state.data_konsumsi = pd.concat([
            st.session_state.data_konsumsi,
            pd.DataFrame([{
                "Tanggal": tanggal,
                "Makanan": makanan,
                "Kalori": kalori,
                "Protein": protein,
                "Lemak": lemak,
                "Karbohidrat": karbohidrat
            }])
        ], ignore_index=True)
        st.success("Data konsumsi berhasil ditambahkan.")

# ===================== RIWAYAT KALORI & ANALISIS =====================
elif menu == "📈 Riwayat Kalori Harian & 📋 Analisis Konsumsi Harian":
    st.header("📈 Riwayat Kalori Harian & 📋 Analisis Konsumsi Harian")

    if st.session_state.data_konsumsi.empty:
        st.info("Belum ada data konsumsi.")
    else:
        st.dataframe(st.session_state.data_konsumsi)

        kalori_harian = st.session_state.data_konsumsi.groupby("Tanggal")["Kalori"].sum()
        st.line_chart(kalori_harian)

        if st.session_state.hasil_perhitungan:
            total_kalori = st.session_state.data_konsumsi["Kalori"].sum()
            sisa_kalori = st.session_state.hasil_perhitungan["TDEE"] - total_kalori

            st.write(f"**Total Kalori yang Dikonsumsi:** {total_kalori:.2f} kkal")
            st.write(f"**Sisa Kalori dari Kebutuhan Harian:** {sisa_kalori:.2f} kkal")

# ===================== ANALISIS MAKRO =====================
elif menu == "🔬 Analisis Makronutrien vs Kebutuhan Harian":
    st.header("🔬 Analisis Makronutrien vs Kebutuhan Harian")

    if st.session_state.data_konsumsi.empty or not st.session_state.hasil_perhitungan:
        st.info("Belum ada data konsumsi atau hasil perhitungan nutrisi.")
    else:
        total_protein = st.session_state.data_konsumsi["Protein"].sum()
        total_lemak = st.session_state.data_konsumsi["Lemak"].sum()
        total_karbo = st.session_state.data_konsumsi["Karbohidrat"].sum()

        kebutuhan = st.session_state.hasil_perhitungan
        data_perbandingan = pd.DataFrame({
            "Dikonsumsi": [total_protein, total_lemak, total_karbo],
            "Dibutuhkan": [kebutuhan["Protein"], kebutuhan["Lemak"], kebutuhan["Karbohidrat"]]
        }, index=["Protein", "Lemak", "Karbohidrat"])

        st.bar_chart(data_perbandingan)
        st.dataframe(data_perbandingan)
