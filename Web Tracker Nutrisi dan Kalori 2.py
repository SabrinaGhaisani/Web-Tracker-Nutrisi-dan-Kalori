import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# CUMA DIPANGGIL SEKALI
st.set_page_config(page_title="Web Tracker Nutrisi dan Kalori", layout="centered")

# INISIALISASI STATE
if "show_nutrisi" not in st.session_state:
    st.session_state.show_nutrisi = False

st.title("🍽️ Tracker Nutrisi dan Kalori")
st.write("Web Tracker Kebutuhan Nutrisi dan Kalori Harianmu")

# ------------------------ INPUT DATA DIRI ------------------------
st.header("📝 Input Data Diri")

nama = st.text_input("Nama")
gender = st.radio("Gender", ["Perempuan", "Laki-laki"])
umur = st.number_input("Umur (tahun)", min_value=0)
tinggi = st.number_input("Tinggi Badan (cm)", min_value=0.0)
berat = st.number_input("Berat Badan (kg)", min_value=0.0)
aktivitas = st.selectbox("Aktivitas Harian", ["Ringan (kerja duduk)", "Sedang (jalan kaki, berdiri)", "Berat (fisik/olahraga)"])

if st.button("Lanjut ➡️"):
    st.session_state.show_nutrisi = True

# ------------------------ TAMPILKAN HASIL ------------------------
if st.session_state.show_nutrisi:
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

    # ------------------ GULA, SERAT, SODIUM ------------------
    st.markdown("### 🧂 Gula, Serat, dan Sodium")

    gula = 50
    serat = 30
    sodium = 2000

    st.write(f"🍬 Gula maksimum per hari: **{gula} g**")
    st.write(f"🌾 Serat yang disarankan: **{serat} g**")
    st.write(f"🧂 Sodium maksimum: **{sodium} mg**")

    mikro_df = pd.DataFrame({
        'Nutrisi': ['Gula', 'Serat', 'Sodium'],
        'Nilai': [gula, serat, sodium / 1000]
    })

    fig2, ax2 = plt.subplots()
    ax2.pie(mikro_df['Nilai'], labels=mikro_df['Nutrisi'], autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)

    st.info("📌 Catatan: Gula & Sodium = batas maksimum. Serat = target minimal.")

    # ------------------ SARAN MAKANAN ------------------
    st.markdown("### 🥗 Saran Makanan")
    st.write("**Karbohidrat:** nasi merah, roti gandum, oat, ubi")
    st.write("**Protein:** dada ayam, tempe, tahu, telur, ikan")
    st.write("**Lemak Sehat:** alpukat, kacang-kacangan, minyak zaitun")
    st.write("**Serat:** sayur hijau, buah apel/pear, brokoli")
    st.write("⚠️ Hindari konsumsi gula dan sodium berlebih dari makanan instan dan minuman manis.")

    # ------------------ INPUT KONSUMSI HARI INI ------------------
    st.markdown("## 🧾 Input Konsumsi Harian")

    tanggal = st.date_input("Tanggal", value=datetime.date.today())

    daftar_makanan = {
        "Nasi Putih (100g)": 175,
        "Tempe Goreng": 120,
        "Telur Rebus": 70,
        "Ayam Panggang": 200,
        "Susu Full Cream (250ml)": 150,
        "Roti Tawar": 80,
        "Pisang": 90,
        "Sayur Bayam": 30,
        "Gorengan": 180,
        "Air Putih": 0,
    }

    st.markdown("### 🍳 Sarapan")
    sarapan = st.multiselect("Pilih makanan:", list(daftar_makanan.keys()), key="sarapan")
    st.markdown("### 🍛 Makan Siang")
    siang = st.multiselect("Pilih makanan:", list(daftar_makanan.keys()), key="siang")
    st.markdown("### 🍲 Makan Malam")
    malam = st.multiselect("Pilih makanan:", list(daftar_makanan.keys()), key="malam")
    st.markdown("### 🍩 Snack")
    snack = st.multiselect("Pilih makanan:", list(daftar_makanan.keys()), key="snack")

    def hitung_kalori(pilihan):
        return sum(daftar_makanan[m] for m in pilihan)

    kal_sarapan = hitung_kalori(sarapan)
    kal_siang = hitung_kalori(siang)
    kal_malam = hitung_kalori(malam)
    kal_snack = hitung_kalori(snack)

    total_kalori = kal_sarapan + kal_siang + kal_malam + kal_snack

    st.markdown("### 🔥 Total Kalori Hari Ini:")
    st.write(f"🍳 Sarapan: {kal_sarapan} kkal")
    st.write(f"🍛 Makan Siang: {kal_siang} kkal")
    st.write(f"🍲 Makan Malam: {kal_malam} kkal")
    st.write(f"🍩 Snack: {kal_snack} kkal")
    st.success(f"**Total: {total_kalori} kkal**")

    if st.button("💾 Simpan Data"):
        data = {
            "tanggal": [tanggal],
            "sarapan": [", ".join(sarapan)],
            "siang": [", ".join(siang)],
            "malam": [", ".join(malam)],
            "snack": [", ".join(snack)],
            "total_kalori": [total_kalori]
        }

        df = pd.DataFrame(data)

        try:
            df_lama = pd.read_csv("kalori_tracker.csv")
            df_baru = pd.concat([df_lama, df], ignore_index=True)
        except FileNotFoundError:
            df_baru = df

        df_baru.to_csv("kalori_tracker.csv", index=False)
        st.success("✅ Data berhasil disimpan ke `kalori_tracker.csv`")
