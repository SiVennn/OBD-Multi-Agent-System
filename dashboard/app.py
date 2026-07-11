import streamlit as st

st.set_page_config(
    page_title="Dashboard Monitoring OBD-II",
    page_icon="🚗",
    layout="wide"
)

# Menampilkan logo jika ada di folder assets
try:
    st.image("assets/logo.png", width=150)
except:
    pass

st.title("🚗 Dashboard Monitoring OBD-II")

st.markdown("""
### Deteksi Anomali Kendaraan Modern Menggunakan Machine Learning

Selamat datang di aplikasi Dashboard Monitoring OBD-II. Proyek ini berfokus pada deteksi dini anomali pada sensor kendaraan menggunakan pendekatan Machine Learning.

### 📊 Alur Kerja Aplikasi (Lihat Sidebar):
- **1. Dataset**: Eksplorasi data hasil prapemrosesan (*preprocessing*).
- **2. Visualisasi**: Analisis grafik tren sensor dan matriks korelasi.
- **3. Deteksi Anomali**: Pengujian data secara langsung dengan model *Isolation Forest*.
- **4. Evaluasi Model**: Meninjau performa dan hasil dari algoritma yang digunakan.
- **5. Tentang**: Informasi tambahan mengenai penelitian ini.
""")

st.success("👈 Silakan pilih menu pada sidebar di sebelah kiri untuk mulai menjelajah.")