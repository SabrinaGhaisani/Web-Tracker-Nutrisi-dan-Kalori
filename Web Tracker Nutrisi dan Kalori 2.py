import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="🍽️ Tracker Nutrisi & Kalori", layout="centered")

# ========== STYLING UMUM ==========
st.markdown("""
    <style>
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #ff914d;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
    }
    .card {
        background-color: #fef6e4;
        padding: 30px;
        border-radius: 18px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }
    .section-title {
        font-size: 22px;
        font-weight: bold;
        color: #6a4c93;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)
# ========== TITLE ==========
st.markdown('<div class="title">🍽️ Web Tracker Nutrisi & Kalori</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Cek kebutuhan gizi & track asupan harianmu!</div>', unsafe_allow_html=True)

# ========== FORM ==========
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📝 Data Diri</div>', unsafe_allow_html=True)

nama = st.text_input("👤 Nama")
gender = st.radio("🚻 Gender", ["Perempuan", "Laki-laki"])
umur = st.number_input("🎂 Umur (tahun)", min_value=0)
tinggi = st.number_input("📏 Tinggi Badan (cm)", min_value=0.0)
berat = st.number_input("⚖️ Berat Badan (kg)", min_value=0.0)
aktivitas = st.selectbox("🏃 Aktivitas Harian", [
    "Ringan (kerja duduk)",
    "Sedang (jalan kaki, berdiri)",
    "Berat (fisik/olahraga)"
])
submit = st.button("➡️ Hitung Kebutuhan")

st.markdown('</div>', unsafe_allow_html=True)

# ========== PERHITUNGAN ==========
if submit:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Hasil Perhitungan</div>', unsafe_allow_html=True)

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

    st.subheader(f"🔥 Total Kebutuhan Kalori: **{kalori:.0f} kkal**")

    # Makro Nutrisi
    karbo = kalori * 0.5 / 4
    lemak = kalori * 0.3 / 9
    protein = kalori * 0.2 / 4

    st.markdown("### 🍱 Rincian Makronutrisi")
    st.write(f"🍚 Karbohidrat: **{karbo:.1f} g**")
    st.write(f"🥩 Protein: **{protein:.1f} g**")
    st.write(f"🧈 Lemak: **{lemak:.1f} g**")

    # Pie Chart
    df_makro = pd.DataFrame({
        'Makro': ['Karbohidrat', 'Lemak', 'Protein'],
        'Gram': [karbo, lemak, protein]
    })

    fig, ax = plt.subplots()
    colors = ['#f4a261', '#e76f51', '#2a9d8f']
    ax.pie(df_makro['Gram'], labels=df_makro['Makro'], autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    st.info("📌 AKG: 50% Karbo, 30% Lemak, 20% Protein")

    # Mikro Nutrisi
    st.markdown("### 🧂 Gula, Serat, Sodium")
    gula = 50
    serat = 30
    sodium = 2000

    st.write(f"🍬 Gula Maks: **{gula} g**")
    st.write(f"🌾 Serat: **{serat} g**")
    st.write(f"🧂 Sodium Maks: **{sodium/1000:.1f} g**")

    df_mikro = pd.DataFrame({
        'Mikro': ['Gula', 'Serat', 'Sodium'],
        'Jumlah': [gula, serat, sodium/1000]
    })

    fig2, ax2 = plt.subplots()
    colors2 = ['#ffcad4', '#d0f4de', '#cdb4db']
    ax2.pie(df_mikro['Jumlah'], labels=df_mikro['Mikro'], autopct='%1.1f%%', colors=colors2, startangle=90)
    ax2.axis('equal')
    st.pyplot(fig2)

    st.markdown('</div>', unsafe_allow_html=True)
    st.info("📌 Catatan: Gula & Sodium = batas maksimum. Serat = target minimal.")

    # ------------------ SARAN MAKANAN ------------------
    st.markdown("### 🥗 Saran Makanan")
    st.write("**Karbohidrat:** nasi merah, roti gandum, oat, ubi")
    st.write("**Protein:** dada ayam, tempe, tahu, telur, ikan")
    st.write("**Lemak Sehat:** alpukat, kacang-kacangan, minyak zaitun")
    st.write("**Serat:** sayur hijau, buah apel/pear, brokoli")
    st.write("⚠️ Hindari konsumsi gula dan sodium berlebih dari makanan instan dan minuman manis.")
  
    # ========== FORM INPUT KONSUMSI ==========
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🧾 Input Konsumsi Harian</div>', unsafe_allow_html=True)

tanggal = st.date_input("📅 Tanggal", value=datetime.date.today())

# DATABASE MAKANAN (dengan nilai kalorinya)
daftar_makanan = {
    "Nasi Putih (100g)": {"kalori": 175, "karbo": 40, "protein": 3, "lemak": 0.3},
    "Tempe Goreng": {"kalori": 120, "karbo": 8, "protein": 8, "lemak": 6},
    "Telur Rebus": {"kalori": 70, "karbo": 1, "protein": 6, "lemak": 5},
    "Ayam Panggang": {"kalori": 200, "karbo": 0, "protein": 30, "lemak": 8},
    "Susu Full Cream (250ml)": {"kalori": 150, "karbo": 12, "protein": 8, "lemak": 8},
    "Roti Tawar": {"kalori": 80, "karbo": 15, "protein": 2, "lemak": 1},
    "Pisang": {"kalori": 90, "karbo": 23, "protein": 1, "lemak": 0.3},
    "Sayur Bayam": {"kalori": 30, "karbo": 4, "protein": 3, "lemak": 0.2},
    "Gorengan": {"kalori": 180, "karbo": 20, "protein": 3, "lemak": 10},
    "Air Putih": {"kalori": 0, "karbo": 0, "protein": 0, "lemak": 0},
}

st.markdown("### 🍳 Sarapan")
sarapan = st.multiselect("Pilih makanan:", list(daftar_makanan.keys()), key="sarapan")

st.markdown("### 🍛 Makan Siang")
siang = st.multiselect("Pilih makanan:", list(daftar_makanan.keys()), key="siang")

st.markdown("### 🍲 Makan Malam")
malam = st.multiselect("Pilih makanan:", list(daftar_makanan.keys()), key="malam")

st.markdown("### 🍩 Snack")
snack = st.multiselect("Pilih makanan:", list(daftar_makanan.keys()), key="snack")

# ========== FUNGSI HITUNG ==========
def hitung_total(pilihan):
    total = {"kalori": 0, "karbo": 0, "protein": 0, "lemak": 0}
    for mkn in pilihan:
        data = daftar_makanan[mkn]
        total["kalori"] += data["kalori"]
        total["karbo"] += data["karbo"]
        total["protein"] += data["protein"]
        total["lemak"] += data["lemak"]
    return total

total_sarapan = hitung_total(sarapan)
total_siang = hitung_total(siang)
total_malam = hitung_total(malam)
total_snack = hitung_total(snack)

# TOTAL KESELURUHAN
total_kal = {
    "kalori": total_sarapan["kalori"] + total_siang["kalori"] + total_malam["kalori"] + total_snack["kalori"],
    "karbo": total_sarapan["karbo"] + total_siang["karbo"] + total_malam["karbo"] + total_snack["karbo"],
    "protein": total_sarapan["protein"] + total_siang["protein"] + total_malam["protein"] + total_snack["protein"],
    "lemak": total_sarapan["lemak"] + total_siang["lemak"] + total_malam["lemak"] + total_snack["lemak"],
}

st.markdown('</div>', unsafe_allow_html=True)

# ========== TAMPILKAN HASIL ==========
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Rangkuman Konsumsi Hari Ini</div>', unsafe_allow_html=True)

st.write(f"🔥 **Total Kalori:** {total_kal['kalori']} kkal")
st.write(f"🍚 Karbohidrat: {total_kal['karbo']} g")
st.write(f"🥩 Protein: {total_kal['protein']} g")
st.write(f"🧈 Lemak: {total_kal['lemak']} g")

# Pie chart makronutrisi konsumsi
df_konsumsi = pd.DataFrame({
    "Makro": ["Karbohidrat", "Protein", "Lemak"],
    "Gram": [total_kal['karbo'], total_kal['protein'], total_kal['lemak']]
})
fig3, ax3 = plt.subplots()
colors3 = ['#e9c46a', '#2a9d8f', '#f4a261']
ax3.pie(df_konsumsi["Gram"], labels=df_konsumsi["Makro"], autopct="%1.1f%%", colors=colors3, startangle=90)
ax3.axis("equal")
st.pyplot(fig3)

st.markdown('</div>', unsafe_allow_html=True)

# ========== SIMPAN DATA ==========
if st.button("💾 Simpan Konsumsi Hari Ini"):
    data = {
        "tanggal": [tanggal],
        "sarapan": [", ".join(sarapan)],
        "siang": [", ".join(siang)],
        "malam": [", ".join(malam)],
        "snack": [", ".join(snack)],
        "kalori": [total_kal["kalori"]],
        "karbo": [total_kal["karbo"]],
        "protein": [total_kal["protein"]],
        "lemak": [total_kal["lemak"]],
    }

    df_hari = pd.DataFrame(data)

    try:
        df_lama = pd.read_csv("kalori_tracker.csv")
        df_baru = pd.concat([df_lama, df_hari], ignore_index=True)
    except FileNotFoundError:
        df_baru = df_hari

    df_baru.to_csv("kalori_tracker.csv", index=False)
    st.success("✅ Data berhasil disimpan ke `kalori_tracker.csv`")

    # ========== RIWAYAT KALORI ==========

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📈 Riwayat Konsumsi Harian</div>', unsafe_allow_html=True)

lihat_riwayat = st.checkbox("👀 Tampilkan Riwayat Harian")

if lihat_riwayat:
    try:
        df_riwayat = pd.read_csv("kalori_tracker.csv")
        df_riwayat['tanggal'] = pd.to_datetime(df_riwayat['tanggal'], format='%Y-%m-%d')
        df_riwayat['tanggal_str'] = df_riwayat['tanggal'].dt.strftime("%d-%m-%Y")

        # Tampilkan tabel dengan format tanggal yang rapi
        df_display = df_riwayat.copy()
        df_display = df_display.drop(columns=["tanggal"])
        df_display = df_display.rename(columns={"tanggal_str": "Tanggal"})

        st.dataframe(df_display)

        # Ambil 7 hari terakhir
        df_filtered = df_riwayat.sort_values('tanggal', ascending=False).head(7).sort_values('tanggal')

        st.subheader("📊 Grafik Kalori 7 Hari Terakhir")

        fig, ax = plt.subplots()
        ax.plot(df_filtered['tanggal'], df_filtered['kalori'], marker='o', linestyle='-', color='#e76f51')
        ax.set_xlabel("Tanggal")
        ax.set_ylabel("Kalori (kkal)")
        ax.set_title("Perbandingan Kalori Harian")
        ax.set_xticks(df_filtered['tanggal'])
        ax.set_xticklabels(df_filtered['tanggal'].dt.strftime("%d-%m"), rotation=45)

        st.pyplot(fig)

        rata2 = df_filtered['kalori'].mean()
        st.success(f"🔍 Rata-rata kalori kamu dalam 7 hari terakhir: **{rata2:.1f} kkal**")

    except FileNotFoundError:
        st.warning("🚫 Belum ada data konsumsi yang disimpan.")
