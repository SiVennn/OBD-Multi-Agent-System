import streamlit as st
import pandas as pd
import joblib  
import os

st.title("🧠 Deteksi Anomali Real-Time")
st.write("Halaman ini menggunakan model *Isolation Forest* untuk mendeteksi indikasi anomali pada sensor kendaraan.")

# Mengamankan Path Berkas
current_dir = os.path.dirname(os.path.abspath(__file__))
path_model = os.path.join(current_dir, "../../model/isolationforest.pkl")
path_csv = os.path.join(current_dir, "../../Datasheet/OBD-Anomaly-Detection/dataset/preprocessing.csv")

# 1. Memuat Model menggunakan Joblib
@st.cache_resource
def load_ml_model():
    if os.path.exists(path_model):
        try:
            return joblib.load(path_model)
        except Exception as e:
            st.error(f"Gagal memuat file pkl lewat joblib: {e}")
    return None

# 2. Memuat Data Dasar untuk Sampel
@st.cache_data
def load_base_data():
    if os.path.exists(path_csv):
        return pd.read_csv(path_csv)
    return None

model = load_ml_model()
df_base = load_base_data()

if model is not None:
    st.sidebar.subheader("Pengaturan Data Uji")
    sumber_data = st.sidebar.radio("Pilih Sumber Data Pengujian:", ["Gunakan Sampel Data Riset", "Unggah Berkas Baru (.csv)"])
    
    df_test = None
    
    # Kondisi 1: Menggunakan data yang sudah ada
    if sumber_data == "Gunakan Sampel Data Riset":
        if df_base is not None:
            st.info("💡 Mengambil 20 baris acak dari data riset untuk simulasi deteksi.")
            df_test = df_base.sample(20, random_state=42).copy()
        else:
            st.error("Data dasar tidak ditemukan untuk simulasi.")
            
    # Kondisi 2: Pengguna mengunggah file baru
    else:
        uploaded_file = st.sidebar.file_uploader("Unggah berkas CSV sensor OBD-II baru:", type=["csv"])
        if uploaded_file is not None:
            df_test = pd.read_csv(uploaded_file)
            st.success("🎉 Berkas berhasil diunggah!")

    # 3. Proses Eksekusi Deteksi Anomali
    if df_test is not None:
        st.subheader("📋 Data yang Akan Diuji")
        st.dataframe(df_test, use_container_width=True)
        
        # Tombol Aksi
        if st.button("🚀 Jalankan Deteksi Anomali", type="primary"):
            try:
                X_test = df_test.copy()
                
                # 💡 TRIK 1: Buang kolom target jika ada
                if 'Anomaly' in X_test.columns:
                    X_test = X_test.drop(columns=['Anomaly'])
                
                # 💡 TRIK 2: FEATURE ALIGNMENT (Solusi Error Mismatch)
                # Mengecek apakah model menyimpan memori kolom saat masa training
                if hasattr(model, 'feature_names_in_'):
                    expected_features = model.feature_names_in_
                    
                    # Jika ada kolom yang ditagih model tapi tidak ada di X_test, buatkan kolomnya isi 0
                    for col in expected_features:
                        if col not in X_test.columns:
                            X_test[col] = 0
                            
                    # Susun ulang posisi kolom agar urutannya 100% sama dengan saat model dilatih
                    X_test = X_test[expected_features]

                # Masukkan data ke model
                prediksi = model.predict(X_test)
                
                # Buat salinan dataframe untuk menampilkan hasil ke user
                df_hasil = df_test.copy()
                df_hasil['Status_Deteksi'] = ["Normal" if p == 1 else "⚠️ ANOMALI" for p in prediksi]
                
                st.subheader("📊 Hasil Analisis Model")
                
                # Tampilkan Ringkasan Menggunakan Metrik
                total_data = len(df_hasil)
                total_anomali = (prediksi == -1).sum()
                total_normal = (prediksi == 1).sum()
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Data Diuji", total_data)
                col2.metric("Data Normal", total_normal)
                col3.metric("Data Terindikasi Anomali", total_anomali, delta=f"{total_anomali} terdeteksi", delta_color="inverse" if total_anomali > 0 else "normal")
                
                # Tampilkan tabel hasil akhir
                st.dataframe(df_hasil, use_container_width=True)
                
                # Berikan alert dinamis
                if total_anomali > 0:
                    st.error(f"🚨 Perhatian! Ditemukan {total_anomali} titik data sensor yang tidak wajar (Anomali). Segera cek kondisi kendaraan!")
                else:
                    st.success("✅ Luar biasa! Seluruh data sensor kendaraan terdeteksi berjalan dalam kondisi Normal.")
                    
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat melakukan prediksi: {e}")
else:
    st.error(f"❌ Gagal memuat model! File `isolationforest.pkl` tidak ditemukan di lokasi: {path_model}. Pastikan Anda sudah mengekspor model dari Notebook.")