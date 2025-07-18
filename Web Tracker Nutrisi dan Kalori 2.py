import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# ====== Konfigurasi Layout & Logo ======
st.set_page_config(
    page_title="NutriTrack - Web Tracker Nutrisi & Kalori",
    layout="wide",
)

# Inisialisasi Session State
if "show_nutrisi" not in st.session_state:
    st.session_state.show_nutrisi = False
if "show_konsumsi" not in st.session_state:
    st.session_state.show_konsumsi = False
if "show_riwayat" not in st.session_state:
    st.session_state.show_riwayat = False

    
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

# ========== SIDEBAR ==========
st.sidebar.title("Navigasi")
halaman = st.sidebar.radio(
    "Pilih Halaman",
    ("Beranda", "Pendahuluan Nutrisi", "Kalkulator Nutrisi", "Konsumsi Harian", "Analisis & Riwayat")
)

if halaman == "Beranda":
    st.image("logo_nutritrack.png", width=180)  # atau langsung pake link
    st.title("NutriTrack")
    st.subheader("Aplikasi Tracker Nutrisi dan Kalori Harian")

    st.write("""
    NutriTrack adalah aplikasi web berbasis Streamlit untuk membantu kamu memantau kebutuhan kalori dan zat gizi harian.
    Dengan tampilan simpel dan fitur interaktif, aplikasi ini cocok untuk semua kalangan—baik pelajar, mahasiswa, maupun masyarakat umum.
    """)
    st.success("Yuk mulai hidup sehat dari sekarang! Gunakan menu di sidebar untuk mulai.")

elif halaman == "Kalkulator Nutrisi":
   # ========== INPUT DATA DIRI ==========
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
        st.session_state.show_nutrisi = True

    # ========== KALKULASI KEBUTUHAN ==========
    if st.session_state.show_nutrisi:
        st.header("📊 Kebutuhan Kalori & Nutrisi Harian")

    if gender == "Perempuan":
        bmr = 447.6 + (9.25 * berat) + (3.1 * tinggi) - (4.33 * umur)
    else:
        bmr = 88.36 + (13.4 * berat) + (4.8 * tinggi) - (5.7 * umur)

    if aktivitas == "Ringan (kerja duduk)":
        kalori = bmr * 1.2
    elif aktivitas == "Sedang (jalan kaki, berdiri)":
        kalori = bmr * 1.55
    else:
        kalori = bmr * 1.9

    st.subheader(f"Total Kebutuhan Kalori Harian: **{kalori:.0f} kkal**")

    karbo = kalori * 0.5 / 4
    lemak = kalori * 0.3 / 9
    protein = kalori * 0.2 / 4

    st.markdown("### 🍱 Rincian Makronutrisi:")
    st.write(f"🍚 Karbohidrat: **{karbo:.1f} g**")
    st.write(f"🥩 Protein: **{protein:.1f} g**")
    st.write(f"🧈 Lemak: **{lemak:.1f} g**")

    df_makro = pd.DataFrame({
        "Nutrisi": ["Karbohidrat", "Protein", "Lemak"],
        "Jumlah (g)": [karbo, protein, lemak]
    })

    fig, ax = plt.subplots()
    ax.pie(df_makro["Jumlah (g)"], labels=df_makro["Nutrisi"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    # ========== GULA SERAT SODIUM ==========
    st.markdown("### 🧂 Gula, Serat, dan Sodium")
    gula, serat, sodium = 50, 30, 2000

    st.write(f"🍬 Gula maksimum per hari: **{gula} g**")
    st.write(f"🌾 Serat yang disarankan: **{serat} g**")
    st.write(f"🧂 Sodium maksimum: **{sodium} mg**")

    df_mikro = pd.DataFrame({
        "Nutrisi": ["Gula", "Serat", "Sodium"],
        "Jumlah": [gula, serat, sodium/1000]
    })

    fig2, ax2 = plt.subplots()
    ax2.pie(df_mikro["Jumlah"], labels=df_mikro["Nutrisi"], autopct="%1.1f%%", startangle=90)
    ax2.axis("equal")
    st.pyplot(fig2)

    # ========== SARAN ==========
    st.markdown("### 🥗 Saran Makanan")
    st.write("**Karbohidrat:** nasi merah, oat, roti gandum")
    st.write("**Protein:** tempe, dada ayam, telur, tahu")
    st.write("**Lemak Sehat:** alpukat, minyak zaitun, kacang")
    st.write("**Serat:** sayuran, buah tinggi serat")
    st.warning("Hindari makanan tinggi gula & sodium ➡️ mi instan, snack kemasan")

elif halaman == "Konsumsi Harian":
    st.markdown("## 🧾 Input Konsumsi Harian")
    tanggal = st.date_input("Tanggal", value=datetime.date.today())

    st.markdown("### 🍳 Sarapan")
    sarapan = st.multiselect("Pilih:", list(daftar_makanan.keys()), key="sarapan")
    st.markdown("### 🍛 Makan Siang")
    siang = st.multiselect("Pilih:", list(daftar_makanan.keys()), key="siang")
    st.markdown("### 🍲 Makan Malam")
    malam = st.multiselect("Pilih:", list(daftar_makanan.keys()), key="malam")
    st.markdown("### 🍩 Snack")
    snack = st.multiselect("Pilih:", list(daftar_makanan.keys()), key="snack")

    # Hitung total kalori
    def hitung_kal(pil):
        return sum(daftar_makanan[m] for m in pil)

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

elif halaman == "Analisis & Riwayat":
    st.markdown("---")
    st.header("📈 Riwayat Kalori Harian")

    if st.checkbox("👀 Tampilkan Riwayat"):
        try:
            df_riwayat = pd.read_csv("kalori_tracker.csv")
            df_riwayat['tanggal'] = pd.to_datetime(df_riwayat['tanggal'], format="%Y-%m-%d")
            st.dataframe(df_riwayat)

            st.subheader("📊 Grafik Kalori Harian (7 hari terakhir)")
            df_filtered = df_riwayat.sort_values('tanggal', ascending=False).head(7).sort_values('tanggal')

            fig3, ax3 = plt.subplots()
            ax3.plot(df_filtered['tanggal'], df_filtered['total_kalori'], marker='o', color='darkorange')
            ax3.set_xlabel("Tanggal")
            ax3.set_ylabel("Total Kalori")
            ax3.set_title("Kalori Harian")
            plt.xticks(rotation=45)
            st.pyplot(fig3)

            rata2 = df_filtered['total_kalori'].mean()
            st.success(f"📌 Rata-rata kalori 7 hari: **{rata2:.2f} kkal**")
        except:
            st.warning("Belum ada data disimpan.")

    # ========== ANALISIS KONSUMSI ==========
    st.markdown("## 📋 Analisis Konsumsi Harian")

    if kalori > 0:
        if total_kalori > kalori + 200:
            st.error("⚠️ Kalori terlalu tinggi. Hati-hati kelebihan energi.")
        elif total_kalori < kalori - 200:
            st.warning("🔻 Kalori terlalu rendah. Bisa membuat lemas.")
        else:
            st.success("✅ Kalori seimbang dengan kebutuhan tubuh.")

    # Top 3
    makanan_semua = sarapan + siang + malam + snack
    kalori_makanan = {}
    for m in makanan_semua:
        kalori_makanan[m] = kalori_makanan.get(m, 0) + daftar_makanan[m]
    top3 = sorted(kalori_makanan.items(), key=lambda x: x[1], reverse=True)[:3]

    st.markdown("### 🍟 Top 3 Penyumbang Kalori")
    for i, (m, k) in enumerate(top3, 1):
        st.write(f"{i}. {m} - **{k} kkal**")

    # ===== ANALISIS NUTRISI =====
    st.markdown("---")
    st.header("🔬 Analisis Makronutrien vs Kebutuhan Harian")

    karbo_aktual = sum([daftar_kandungan[m][0] for m in makanan_semua])
    protein_aktual = sum([daftar_kandungan[m][1] for m in makanan_semua])
    lemak_aktual = sum([daftar_kandungan[m][2] for m in makanan_semua])

    st.subheader("📌 Target vs Terkonsumsi (gram)")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"- Karbohidrat: {karbo:.1f}")
        st.write(f"- Protein: {protein:.1f}")
        st.write(f"- Lemak: {lemak:.1f}")
    with col2:
        st.write(f"- Karbohidrat: {karbo_aktual:.1f}")
        st.write(f"- Protein: {protein_aktual:.1f}")
        st.write(f"- Lemak: {lemak_aktual:.1f}")

    df_nut = pd.DataFrame({
        "Jenis": ["Karbohidrat", "Protein", "Lemak"],
        "Target": [karbo, protein, lemak],
        "Aktual": [karbo_aktual, protein_aktual, lemak_aktual]
    })

    fig4, ax4 = plt.subplots()
    x = range(len(df_nut))
    width = 0.35
    ax4.bar(x, df_nut["Target"], width=width, label="Target", color="skyblue")
    ax4.bar([p + width for p in x], df_nut["Aktual"], width=width, label="Terkonsumsi", color="salmon")
    ax4.set_xticks([p + width/2 for p in x])
    ax4.set_xticklabels(df_nut["Jenis"])
    ax4.set_ylabel("Jumlah (g)")
    ax4.set_title("Perbandingan Nutrisi")
    ax4.legend()
    st.pyplot(fig4)

    # SARAN
    if karbo_aktual > karbo + 10:
        st.warning("🍚 Karbohidrat tinggi. Kurangi nasi, mie, atau gula.")
    elif karbo_aktual < karbo - 10:
        st.info("🍚 Tambahkan karbo dari oat, ubi, roti gandum.")

    if protein_aktual < protein - 5:
        st.info("🥩 Tambahkan protein: tempe, tahu, ayam, telur.")
    elif protein_aktual > protein + 10:
        st.warning("🥩 Protein terlalu tinggi. Hati-hati beban ginjal.")

    if lemak_aktual > lemak + 5:
        st.warning("🧈 Lemak tinggi. Kurangi gorengan & makanan berminyak.")
    elif lemak_aktual < lemak - 5:
        st.info("🧈 Lemak sehat dibutuhkan. Tambahkan alpukat, zaitun.")
        
elif halaman == "Pendahuluan Nutrisi":
    st.header("🧬 Pendahuluan Nutrisi dan Kalori")

    st.write("""
    Kalori adalah satuan energi yang didapat tubuh dari makanan. Dalam konteks kimia organik, kalori berkaitan erat dengan proses metabolisme senyawa karbon seperti karbohidrat, protein, dan lemak.

    Setiap makronutrien memiliki peran berbeda:
    - **Karbohidrat**: sumber energi utama
    - **Protein**: penyusun sel dan jaringan
    - **Lemak**: cadangan energi dan pelarut vitamin

    Melalui pemantauan nutrisi, kamu bisa menyeimbangkan asupan dengan kebutuhan tubuh agar tetap sehat dan optimal.
    """)
