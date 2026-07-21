import streamlit as st

st.set_page_config(page_title="Tentang - MAS", page_icon="ℹ️", layout="wide")

st.title("ℹ️ Tentang Penelitian")
st.write("---")

st.subheader("Judul Penelitian")
st.write("**Implementasi Multi-Agentic System (MAS) untuk Deteksi Anomali Kendaraan Modern Berbasis Data OBD-II.**")
st.write("---")

st.subheader("Arsitektur Sistem & Algoritma Utama")
st.markdown("""
**Sistem Multi-Agen (*Centralized Sequential Architecture*):**
* **Data Collector Agent:** Agen otonom yang bertugas merekayasa data mentah dan membongkar format kompleks (JSON/String) menjadi struktur terstandarisasi.
* **AI Detection Agent:** Agen kecerdasan buatan (*Isolation Forest* & *Random Forest*) yang dilengkapi sistem toleransi kesalahan (*Fault Tolerance*) untuk mendeteksi anomali pada fitur sensor.
* **Expert Diagnostic Agent:** Agen pakar yang bertugas menganalisis komputasi model menjadi bahasa keputusan status mesin.
""")
st.write("---")

st.subheader("Dataset")
st.write("Driving Dataset OBD-II CAN Bus")
st.write("---")

st.subheader("Bahasa Pemrograman & Library")
st.markdown("""
* **Bahasa:** Python
* **Library Utama:** Pandas, Scikit-learn, Streamlit, Matplotlib, Seaborn, Joblib, JSON, Regex (`re`)
""")
st.write("---")

st.subheader("Tujuan")
st.write("Membangun sistem cerdas yang mampu mendeteksi kondisi kendaraan secara otomatis dan terdistribusi. Melalui kolaborasi antar-agen AI, sistem dapat melakukan penyelesaian masalah secara paralel, mentolerir kesalahan format data input, serta memberikan diagnosis dini terkait potensi gangguan pada kendaraan dengan sangat efisien.")