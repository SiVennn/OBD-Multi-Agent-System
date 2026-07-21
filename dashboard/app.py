import streamlit as st

st.set_page_config(
    page_title="Dashboard OBD-II MAS", 
    page_icon="🚗", 
    layout="wide"
)

# Menampilkan logo jika ada di folder assets
try:
    st.image("assets/logo.png", width=150)
except:
    pass

st.title("Dashboard Monitoring OBD-II Berbasis MAS")
st.subheader("Deteksi Anomali Kendaraan Modern Menggunakan Multi-Agentic System")

st.write("Selamat datang di aplikasi Dashboard Monitoring OBD-II. Proyek ini telah ditingkatkan menggunakan arsitektur **Multi-Agent System (MAS)**, di mana tugas-tugas cerdas didistribusikan ke tiga agen AI otonom (*Data Agent, AI Agent,* dan *Expert Agent*). Mereka berkolaborasi untuk memproses data, mendeteksi pola anomali, dan merumuskan diagnosis klinis kendaraan secara otomatis.")

st.write("---")
st.subheader("Alur Kerja Aplikasi (Lihat Sidebar):")
st.markdown("""
* **1. Dataset:** Eksplorasi data sensor kendaraan hasil prapemrosesan (*preprocessing*).
* **2. Visualisasi:** Analisis visual metrik tren sensor dan matriks korelasi.
* **3. Deteksi Anomali:** Pengujian data interaktif yang digerakkan oleh kolaborasi otonom 3 Agen AI secara *real-time*.
* **4. Evaluasi Model:** Meninjau performa dan hasil metrik dari algoritma dasar yang digunakan.
* **5. Tentang:** Informasi tambahan mengenai arsitektur sistem dan detail penelitian ini.
""")

st.success("👈 Silakan pilih menu pada sidebar di sebelah kiri untuk mulai menjelajah.")