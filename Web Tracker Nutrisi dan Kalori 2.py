import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# ========== SETUP ==========
st.set_page_config(page_title="Tracker Nutrisi", layout="wide")
st.image("logo_nutritrack.png", width=300)
st.title("🍽️ Tracker Nutrisi dan Kalori")

# ========== STATE ==========
if "sidebar_visible" not in st.session_state:
    st.session_state.sidebar_visible = True
if "menu" not in st.session_state:
    st.session_state.menu = "Input Data Diri"
if "show_nutrisi" not in st.session_state:
    st.session_state.show_nutrisi = False

# ========== DATABASE ==========
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

daftar_kandungan = {
    "Nasi Putih (100g)": [40, 3, 1],
    "Tempe Goreng": [10, 8, 6],
    "Telur Rebus": [1, 6, 5],
    "Ayam Panggang": [0, 30, 7],
    "Susu Full Cream (250ml)": [12, 8, 8],
    "Roti Tawar": [15, 3, 1],
    "Pisang": [22, 1, 0],
    "Sayur Bayam": [3, 2, 0],
    "Gorengan": [10, 2, 15],
    "Air Putih": [0, 0, 0],
}

# ========== TOGGLE SIDEBAR ==========
toggle = st.button("👈 Sembunyikan Menu" if st.session_state.sidebar_visible else "👉 Tampilkan Menu")
if toggle:
    st.session_state.sidebar_visible = not st.session_state.sidebar_visible

# ========== LAYOUT ==========
col1, col2 = st.columns([1, 5])

with col1:
    if st.session_state.sidebar_visible:
        st.markdown("## 📁 Menu")
        st.session_state.menu = st.radio("Navigasi", [
            "Input Data Diri",
            "Kalkulasi Kalori",
            "Input Konsumsi",
            "Riwayat",
            "Analisis Nutrisi"
        ])

with col2:
    menu = st.session_state.menu

    # ========== MENU 1: DATA DIRI ==========
    if menu == "Input Data Diri":
        st.header("📝 Input Data Diri")
        nama = st.text_input("Nama")
        gender = st.radio("Gender", ["Perempuan", "Laki-laki"])
        umur = st.number_input("Umur (tahun)", min_value=0)
        tinggi = st.number_input("Tinggi Badan (cm)", min_value=0.0)
        berat = st.number_input("Berat Badan (kg)", min_value=0.0)
        aktivitas = st.selectbox("Aktivitas Harian", [
            "Ringan (kerja duduk)", "Sedang (jalan kaki, berdiri)", "Berat (fisik/olahraga)"
        ])
        if st.button("Lanjut ➡️"):
            st.session_state.show_nutrisi = True
            st.session_state.menu = "Kalkulasi Kalori"

    # ========== MENU 2: KALKULASI KALORI ==========
    elif menu == "Kalkulasi Kalori" and st.session_state.show_nutrisi:
        st.header("📊 Kebutuhan Kalori & Nutrisi Harian")

        if gender == "Perempuan":
            bmr = 447.6 + (9.25 * berat) + (3.1 * tinggi) - (4.33 * umur)
        else:
            bmr = 88.36 + (13.4 * berat) + (4.8 * tinggi) - (5.7 * umur)

        kalori = bmr * {"Ringan (kerja duduk)": 1.2, "Sedang (jalan kaki, berdiri)": 1.55, "Berat (fisik/olahraga)": 1.9}[aktivitas]
        karbo = kalori * 0.5 / 4
        lemak = kalori * 0.3 / 9
        protein = kalori * 0.2 / 4

        st.subheader(f"Total Kalori Harian: **{kalori:.0f} kkal**")
        st.write(f"🍚 Karbohidrat: **{karbo:.1f} g**, 🥩 Protein: **{protein:.1f} g**, 🧈 Lemak: **{lemak:.1f} g**")

        df_makro = pd.DataFrame({
            "Nutrisi": ["Karbohidrat", "Protein", "Lemak"],
            "Jumlah (g)": [karbo, protein, lemak]
        })
        fig, ax = plt.subplots()
        ax.pie(df_makro["Jumlah (g)"], labels=df_makro["Nutrisi"], autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)

        # Gula, serat, sodium
        st.markdown("### 🧂 Gula, Serat, dan Sodium")
        st.write(f"🍬 Gula maksimum: **50 g**")
        st.write(f"🌾 Serat disarankan: **30 g**")
        st.write(f"🧂 Sodium maksimum: **2000 mg**")

    # ========== MENU 3: INPUT KONSUMSI ==========
    elif menu == "Input Konsumsi":
        st.header("🧾 Input Konsumsi Harian")
        tanggal = st.date_input("Tanggal", value=datetime.date.today())
        sarapan = st.multiselect("🍳 Sarapan", list(daftar_makanan.keys()), key="sarapan")
        siang = st.multiselect("🍛 Makan Siang", list(daftar_makanan.keys()), key="siang")
        malam = st.multiselect("🍲 Makan Malam", list(daftar_makanan.keys()), key="malam")
        snack = st.multiselect("🍩 Snack", list(daftar_makanan.keys()), key="snack")

        def hitung_kal(pil): return sum(daftar_makanan[m] for m in pil)

        kal_sarapan = hitung_kal(sarapan)
        kal_siang = hitung_kal(siang)
        kal_malam = hitung_kal(malam)
        kal_snack = hitung_kal(snack)
        total_kalori = kal_sarapan + kal_siang + kal_malam + kal_snack

        st.subheader("🔥 Total Kalori Hari Ini")
        st.write(f"🍳 Sarapan: {kal_sarapan} kkal")
        st.write(f"🍛 Siang: {kal_siang} kkal")
        st.write(f"🍲 Malam: {kal_malam} kkal")
        st.write(f"🍩 Snack: {kal_snack} kkal")
        st.success(f"**Total: {total_kalori} kkal**")

        if st.button("💾 Simpan Data"):
            df = pd.DataFrame({
                "tanggal": [tanggal],
                "sarapan": [", ".join(sarapan)],
                "siang": [", ".join(siang)],
                "malam": [", ".join(malam)],
                "snack": [", ".join(snack)],
                "total_kalori": [total_kalori]
            })

            try:
                df_lama = pd.read_csv("kalori_tracker.csv")
                df_baru = pd.concat([df_lama, df], ignore_index=True)
            except FileNotFoundError:
                df_baru = df

            df_baru.to_csv("kalori_tracker.csv", index=False)
            st.success("✅ Data disimpan ke `kalori_tracker.csv`")

    # ========== MENU 4: RIWAYAT ==========
    elif menu == "Riwayat":
        st.header("📈 Riwayat Kalori Harian")
        if st.checkbox("👀 Tampilkan Riwayat"):
            try:
                df_riwayat = pd.read_csv("kalori_tracker.csv")
                df_riwayat['tanggal'] = pd.to_datetime(df_riwayat['tanggal'])
                st.dataframe(df_riwayat)

                st.subheader("📊 Grafik Kalori Harian (7
