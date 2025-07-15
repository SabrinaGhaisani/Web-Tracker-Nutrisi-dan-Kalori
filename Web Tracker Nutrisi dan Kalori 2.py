import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Input Kalori Harian", layout="centered")

st.title("📆 Input Kalori Harian")
st.write("Isi data makanan yang kamu konsumsi hari ini")

# ---------- PILIH TANGGAL ----------
tanggal = st.date_input("Tanggal", value=datetime.date.today())

# ---------- DATABASE MAKANAN ----------
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

# ---------- FORM INPUT MAKANAN ----------
st.markdown("### 🍳 Sarapan")
sarapan = st.multiselect("Pilih makanan saat sarapan:", list(daftar_makanan.keys()), key="sarapan")

st.markdown("### 🍛 Makan Siang")
siang = st.multiselect("Pilih makanan saat makan siang:", list(daftar_makanan.keys()), key="siang")

st.markdown("### 🍲 Makan Malam")
malam = st.multiselect("Pilih makanan saat makan malam:", list(daftar_makanan.keys()), key="malam")

st.markdown("### 🍩 Snack / Cemilan")
snack = st.multiselect("Pilih makanan saat snack:", list(daftar_makanan.keys()), key="snack")

# ---------- HITUNG TOTAL KALORI ----------
def hitung_kalori(pilihan):
    return sum(daftar_makanan[m] for m in pilihan)

kal_sarapan = hitung_kalori(sarapan)
kal_siang = hitung_kalori(siang)
kal_malam = hitung_kalori(malam)
kal_snack = hitung_kalori(snack)

total_kalori = kal_sarapan + kal_siang + kal_malam + kal_snack

# ---------- TAMPILKAN HASIL ----------
st.markdown("## 🔥 Total Kalori Hari Ini:")
st.write(f"🍳 Sarapan: {kal_sarapan} kkal")
st.write(f"🍛 Makan Siang: {kal_siang} kkal")
st.write(f"🍲 Makan Malam: {kal_malam} kkal")
st.write(f"🍩 Snack: {kal_snack} kkal")
st.success(f"Total: **{total_kalori} kkal**")

# ---------- SIMPAN KE CSV ----------
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

