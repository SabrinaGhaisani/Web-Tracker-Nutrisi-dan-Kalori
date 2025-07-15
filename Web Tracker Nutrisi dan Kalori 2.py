import streamlit as st

# --- Halaman 1: Input Data Diri ---
st.title("📝 Input Data Diri")

nama = st.text_input("Nama")
gender = st.radio("Gender", ["Perempuan", "Laki-laki"])
umur = st.number_input("Umur (tahun)", min_value=0, max_value=120)
tinggi = st.number_input("Tinggi Badan (cm)", min_value=0)
berat = st.number_input("Berat Badan (kg)", min_value=0)

aktivitas = st.selectbox("Aktivitas Harian", [
    "Tidak aktif (tidur rebahan saja)",
    "Ringan (kerja duduk, sedikit jalan)",
    "Sedang (kerja ringan + olahraga ringan)",
    "Berat (kerja fisik berat/olahraga intens)"
])

# Tombol untuk melanjutkan
if st.button("Lanjutkan"):
    st.session_state.nama = nama
    st.session_state.gender = gender
    st.session_state.umur = umur
    st.session_state.tinggi = tinggi
    st.session_state.berat = berat
    st.session_state.aktivitas = aktivitas
    st.switch_page("halaman2.py")  # nanti kita buat file ini
