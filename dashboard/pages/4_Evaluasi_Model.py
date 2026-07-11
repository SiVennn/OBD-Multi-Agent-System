import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📋 Evaluasi & Performa Algoritma")
st.write("Halaman ini menyajikan analisis hasil pengujian serta komparasi performa antara algoritma Isolation Forest dan Random Forest.")

# Mengamankan Path Berkas Hasil Pengujian
current_dir = os.path.dirname(os.path.abspath(__file__))
path_iso_result = os.path.join(current_dir, "../../Datasheet/OBD-Anomaly-Detection/dataset/isolation_result.csv")
path_rf_result = os.path.join(current_dir, "../../Datasheet/OBD-Anomaly-Detection/dataset/randomforest_result.csv")

@st.cache_data
def load_result(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None

df_iso_res = load_result(path_iso_result)
df_rf_res = load_result(path_rf_result)

# ==========================================
# 📊 TAB PERBANDINGAN
# ==========================================
tab1, tab2 = st.tabs(["📈 Log Hasil Pengujian", "⚔️ Analisis Komparasi Model"])

with tab1:
    st.subheader("Log Hasil Prediksi Model")
    st.write("Menampilkan cuplikan data hasil prediksi yang telah diekspor oleh masing-masing algoritma.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌲 Isolation Forest Result")
        if df_iso_res is not None:
            st.dataframe(df_iso_res.head(50), use_container_width=True)
            st.caption(f"Total baris hasil pengujian Isolation Forest: {len(df_iso_res):,}")
        else:
            st.info("ℹ️ File `isolation_result.csv` tidak ditemukan. Pastikan Notebook 03 telah dijalankan.")
            
    with col2:
        st.markdown("### 🌿 Random Forest Result")
        if df_rf_res is not None:
            st.dataframe(df_rf_res.head(50), use_container_width=True)
            st.caption(f"Total baris hasil pengujian Random Forest: {len(df_rf_res):,}")
        else:
            st.info("ℹ️ File `randomforest_result.csv` tidak ditemukan. Pastikan Notebook 04 telah dijalankan.")

with tab2:
    st.subheader("Perbandingan Karakteristik Model")
    
    # Membuat tabel komparasi teoretis & praktis untuk kebutuhan sidang
    komparasi_data = {
        "Karakteristik": [
            "Tipe Pembelajaran", 
            "Kebutuhan Label Data", 
            "Fokus Deteksi utama", 
            "Kelebihan Utama"
        ],
        "Isolation Forest": [
            "Unsupervised Learning", 
            "Tidak Butuh Label (X)", 
            "Mencari data pencilan / anomali baru", 
            "Sangat cepat mendeteksi anomali yang belum pernah terjadi sebelumnya"
        ],
        "Random Forest": [
            "Supervised Learning", 
            "Butuh Label Kelas (Y)", 
            "Mengklasifikasikan tipe anomali terstruktur", 
            "Tingkat akurasi klasifikasi sangat tinggi pada pola anomali yang sudah dikenali"
        ]
    }
    df_komparasi = pd.DataFrame(komparasi_data)
    st.table(df_komparasi.set_index("Karakteristik"))
    
    # Bagian Metrik Ringkasan Performa (Bisa Anda sesuaikan dengan angka akurasi/f1-score asli riset Anda)
    st.markdown("### 📌 Kesimpulan Rekomendasi Penelitian")
    
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Rekomendasi Utama", value="Hybrid System")
    m2.metric(label="Waktu Eksekusi", value="< 0.1 Detik")
    m3.metric(label="Efisiensi Sensor", value="Optimal")
    
    st.info("""
    💡 **Saran Integrasi Sistem:**
    Untuk memonitor kendaraan secara berkala, **Isolation Forest** ideal digunakan di garda depan guna menyaring data-data anomali baru yang tidak terduga dari sensor OBD-II. Di sisi lain, **Random Forest** bertindak sebagai mesin klasifikasi tingkat lanjut untuk mendiagnosis jenis kerusakan spesifik berdasarkan pola anomali historis yang sudah dipelajari sebelumnya.
    """)