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
elif selected_main == "📊 Kebutuhan Kalori & Nutrisi Harian":
    st.title("📊 Kebutuhan Kalori & Nutrisi Harian")
    with st.sidebar:
        st.header("📊 Menu Kalori & Nutrisi")
        st.write("Berisi info kebutuhan kalori harian berdasarkan data diri.")
        if st.button("Kembali ke Input Data Diri"):
            st.session_state.main_page = "👤 Input Data Diri"

    # Get previously inputted data from session state (set in Input Data Diri)
    if all(k in st.session_state for k in ["berat", "tinggi", "umur", "gender", "aktivitas"]):
        berat = st.session_state.berat
        tinggi = st.session_state.tinggi
        umur = st.session_state.umur
        gender = st.session_state.gender
        aktivitas = st.session_state.aktivitas

        bmr = 10 * berat + 6.25 * tinggi - 5 * umur + (5 if gender == "Laki-laki" else -161)

        faktor_aktivitas = {
            "Tidak aktif": 1.2,
            "Sedikit aktif": 1.375,
            "Cukup aktif": 1.55,
            "Aktif": 1.725,
            "Sangat aktif": 1.9
        }
        tdee = bmr * faktor_aktivitas[aktivitas]

        st.subheader("🔹 Ringkasan")
        st.write(f"**BMR (Basal Metabolic Rate)**: {bmr:.2f} kalori/hari")
        st.write(f"**TDEE (Total Daily Energy Expenditure)**: {tdee:.2f} kalori/hari")

    else:
        st.warning("Silakan isi data diri terlebih dahulu di halaman '👤 Input Data Diri'.")

# ===================== INPUT KONSUMSI =====================
elif selected_main == "🍽️ Input Konsumsi Harian":
    st.title("🍽️ Input Konsumsi Harian")
    with st.sidebar:
        st.header("🍽️ Menu Konsumsi")
        st.write("Input makanan dari daftar dan beratnya.")
        if st.button("Lihat Riwayat & Analisis"):
            st.session_state.main_page = "📈 Riwayat & Analisis Harian"

    # Daftar makanan (bisa diganti dengan load dari file CSV kalau mau)
    makanan_dict = {
        "Nasi Putih": 175,
        "Ayam Goreng": 260,
        "Tempe Goreng": 193,
        "Tahu Goreng": 121,
        "Telur Rebus": 155,
        "Sayur Bayam": 36,
        "Ikan Goreng": 200,
        "Kentang Goreng": 312
    }

    makanan = st.selectbox("Pilih Makanan", list(makanan_dict.keys()))
    berat = st.number_input("Masukkan berat (gram)", min_value=0, step=10)

    if st.button("Tambah ke Konsumsi Hari Ini"):
        kalori_per_100g = makanan_dict[makanan]
        total_kalori = (kalori_per_100g / 100) * berat

        # Simpan data ke session_state
        if "konsumsi_harian" not in st.session_state:
            st.session_state.konsumsi_harian = []

        st.session_state.konsumsi_harian.append({
            "makanan": makanan,
            "berat": berat,
            "kalori": total_kalori
        })
        st.success(f"{makanan} ({berat}g) ditambahkan! Kalori: {total_kalori:.2f}")

    # Tampilkan konsumsi hari ini
    if "konsumsi_harian" in st.session_state and st.session_state.konsumsi_harian:
        st.subheader("🍱 Konsumsi Hari Ini")
        df = pd.DataFrame(st.session_state.konsumsi_harian)
        df.index += 1
        st.table(df)
    else:
        st.info("Belum ada konsumsi yang ditambahkan hari ini.")

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
