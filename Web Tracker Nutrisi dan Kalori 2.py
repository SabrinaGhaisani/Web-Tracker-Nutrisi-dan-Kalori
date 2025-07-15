import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# CUMA DIPANGGIL SEKALI
st.set_page_config(page_title="Web Tracker Nutrisi dan Kalori", layout="centered")

# INISIALISASI STATE
if "show_nutrisi" not in st.session_state:
    st.session_state.show_nutrisi = False

st.title("Tracker Nutrisi dan Kalori")
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

    # -------------------- PIE CHART LUCU MAKRO --------------------
    labels = ['🍚 Karbohidrat', '🥩 Protein', '🧈 Lemak']
    sizes = [karbo, protein, lemak]
    colors = ['#FFDDC1', '#FFABAB', '#FFC3A0']
    explode = (0.05, 0.05, 0.05)

    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        explode=explode,
        autopct='%1.1f%%',
        startangle=90,
        wedgeprops=dict(width=0.5)
    )

    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_fontsize(9)

    ax.axis('equal')
    plt.title("🍱 Komposisi Makronutrisi Harian", fontsize=14)
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
        'Nutrisi': ['🍬 Gula', '🌾 Serat', '🧂 Sodium'],
        'Nilai': [gula, serat, sodium / 1000]
    })

    fig2, ax2 = plt.subplots()
    ax2.pie(mikro_df['Nilai'], labels=mikro_df['Nutrisi'], colors=['#D5AAFF','#A0E7E5','#FFDAC1'],
            autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.5))
    ax2.axis('equal')
    plt.title("🍬 Gula, Serat, Sodium", fontsize=14)
    st.pyplot(fig2)

    st.info("📌 Catatan: Gula & Sodium = batas maksimum. Serat = target minimal.")

    # ------------------ SARAN MAKANAN ------------------
    st.markdown("### 🥗 Saran Makanan")
    st.write("**Karbohidrat:** nasi merah, roti gandum, oat, ubi")
    st.write("**Protein:** dada ayam, tempe, tahu, telur, ikan")
    st.write("**Lemak Sehat:** alpukat, kacang-kacangan, minyak zaitun")
    st.write("**Serat:** sayur hijau, buah apel/pear, brokoli")
    st.write("⚠️ Hindari konsumsi gula dan sodium berlebih dari makanan instan dan minuman manis.")
    # ------------------ INPUT KONSUMSI HARIAN ------------------
    st.markdown("## 🧾 Input Konsumsi Harian")

    tanggal = st.date_input("Tanggal", value=datetime.date.today())

    # DATABASE MAKANAN DENGAN KANDUNGAN GIZI
    daftar_makanan = {
        "Nasi Putih (100g)": {"kal": 175, "karbo": 40, "protein": 3, "lemak": 0.5},
        "Tempe Goreng": {"kal": 120, "karbo": 8, "protein": 6, "lemak": 8},
        "Telur Rebus": {"kal": 70, "karbo": 1, "protein": 6, "lemak": 5},
        "Ayam Panggang": {"kal": 200, "karbo": 0, "protein": 25, "lemak": 10},
        "Susu Full Cream (250ml)": {"kal": 150, "karbo": 12, "protein": 8, "lemak": 8},
        "Roti Tawar": {"kal": 80, "karbo": 15, "protein": 3, "lemak": 1},
        "Pisang": {"kal": 90, "karbo": 23, "protein": 1, "lemak": 0.3},
        "Sayur Bayam": {"kal": 30, "karbo": 5, "protein": 2, "lemak": 0.2},
        "Gorengan": {"kal": 180, "karbo": 15, "protein": 2, "lemak": 12},
        "Air Putih": {"kal": 0, "karbo": 0, "protein": 0, "lemak": 0},
    }

    def hitung_total(makanan_list, tipe):
        return sum(daftar_makanan[m][tipe] for m in makanan_list)

    st.markdown("### 🍳 Sarapan")
    sarapan = st.multiselect("Pilih makanan:", list(daftar_makanan.keys()), key="sarapan")
    st.markdown("### 🍛 Makan Siang")
    siang = st.multiselect("Pilih makanan:", list(daftar_makanan.keys()), key="siang")
    st.markdown("### 🍲 Makan Malam")
    malam = st.multiselect("Pilih makanan:", list(daftar_makanan.keys()), key="malam")
    st.markdown("### 🍩 Snack")
    snack = st.multiselect("Pilih makanan:", list(daftar_makanan.keys()), key="snack")

    semua_makanan = sarapan + siang + malam + snack

    total_kal = hitung_total(semua_makanan, "kal")
    total_karbo = hitung_total(semua_makanan, "karbo")
    total_protein = hitung_total(semua_makanan, "protein")
    total_lemak = hitung_total(semua_makanan, "lemak")

    st.markdown("### 🔥 Total Konsumsi Hari Ini")
    st.write(f"🍚 Karbohidrat: **{total_karbo} g**")
    st.write(f"🥩 Protein: **{total_protein} g**")
    st.write(f"🧈 Lemak: **{total_lemak} g**")
    st.success(f"Total Kalori: **{total_kal} kkal**")

    # PIE CHART KONSUMSI HARI INI
    konsumsi_df = pd.DataFrame({
        "Makronutrien": ["🍚 Karbo", "🥩 Protein", "🧈 Lemak"],
        "Gram": [total_karbo, total_protein, total_lemak]
    })

    fig3, ax3 = plt.subplots()
    ax3.pie(konsumsi_df['Gram'], labels=konsumsi_df['Makronutrien'],
            autopct='%1.1f%%', startangle=90, colors=['#FFF5BA','#B5EAD7','#FFB7B2'],
            wedgeprops=dict(width=0.5))
    ax3.axis('equal')
    plt.title("🍽️ Komposisi Makronutrien Konsumsi Hari Ini")
    st.pyplot(fig3)

    # SIMPAN DATA
    if st.button("💾 Simpan Data"):
        data = {
            "tanggal": [tanggal],
            "sarapan": [", ".join(sarapan)],
            "siang": [", ".join(siang)],
            "malam": [", ".join(malam)],
            "snack": [", ".join(snack)],
            "total_kalori": [total_kal],
            "karbo": [total_karbo],
            "protein": [total_protein],
            "lemak": [total_lemak]
        }

        df = pd.DataFrame(data)

        try:
            df_lama = pd.read_csv("kalori_tracker.csv")
            df_baru = pd.concat([df_lama, df], ignore_index=True)
        except FileNotFoundError:
            df_baru = df

        df_baru.to_csv("kalori_tracker.csv", index=False)
        st.success("✅ Data berhasil disimpan!")

    # ===================== RINGKASAN RIWAYAT =====================
    st.markdown("---")
    st.header("📈 Riwayat Kalori Harian")
    lihat_riwayat = st.checkbox("👀 Lihat Riwayat 7 Hari Terakhir")

    if lihat_riwayat:
        try:
            df_riwayat = pd.read_csv("kalori_tracker.csv")
            df_riwayat['tanggal'] = pd.to_datetime(df_riwayat['tanggal'])

            df_7hari = df_riwayat.sort_values('tanggal', ascending=False).head(7).sort_values('tanggal')

            st.dataframe(df_7hari)

            fig4, ax4 = plt.subplots()
            ax4.plot(df_7hari['tanggal'], df_7hari['total_kalori'], marker='o', color='coral')
            ax4.set_xlabel("Tanggal")
            ax4.set_ylabel("Kalori (kkal)")
            ax4.set_title("Grafik Kalori 7 Hari Terakhir")
            plt.xticks(rotation=45)
            st.pyplot(fig4)

            rata2 = df_7hari['total_kalori'].mean()
            st.info(f"📊 Rata-rata konsumsi kalori: **{rata2:.1f} kkal**")

        except FileNotFoundError:
            st.warning("❌ Belum ada data disimpan sebelumnya.")
