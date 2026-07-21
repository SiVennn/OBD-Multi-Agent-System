import streamlit as st
import pandas as pd
import os
import time

# Memanggil Agen yang sudah kita buat di file agents.py
from agents import DataAgent, AnomalyDetectionAgent, DiagnosticAgent

st.set_page_config(page_title="Deteksi Anomali - MAS", page_icon="🤖", layout="wide")

st.title("Sistem Deteksi Anomali Berbasis Multi-Agent")
st.write("Halaman ini digerakkan oleh kolaborasi 3 Agen AI yang saling berbagi tugas secara otonom.")
st.write("---")

# Mengatur path model secara aman agar tidak error di server lokal maupun cloud
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.abspath(os.path.join(BASE_DIR, "../../model/isolationforest.pkl"))

# 1. Inisialisasi Agen (Menghidupkan Para Agen)
data_agent = DataAgent()
ai_agent = AnomalyDetectionAgent(MODEL_PATH)
expert_agent = DiagnosticAgent()

# Tambahan input untuk pengguna
st.subheader("📁 Masukkan Data Sensor OBD-II")
uploaded_file = st.file_uploader("Unggah file CSV data sensor kendaraan kamu", type=["csv"])

if uploaded_file is not None:
    st.success("File berhasil diunggah! Para agen siap bekerja.")
    
    # Tombol untuk memicu pergerakan agen
    if st.button("🚀 Jalankan Kolaborasi Multi-Agen", type="primary"):
        
        st.subheader("🔄 Log Komunikasi & Aktivitas Agen (MAS):")
        
        # --- PROSES AGEN 1 ---
        log_container = st.container(border=True)
        with log_container:
            with st.spinner(f"⏳ {data_agent.name} sedang bekerja..."):
                time.sleep(1.5) # Efek jeda simulasi berpikir/bekerja
                df_clean = data_agent.process_data(uploaded_file)
                
            if df_clean is not None:
                st.write(f"🟢 **[{data_agent.name}]:** 'Saya telah berhasil membaca data mentah sebanyak {len(df_clean)} baris. Sekarang saya kirim data ini ke {ai_agent.name}.'")
                
                # --- PROSES AGEN 2 ---
                with st.spinner(f"⏳ {ai_agent.name} sedang bekerja..."):
                    time.sleep(2) # Efek jeda simulasi memproses ML
                    
                    # Mengambil kolom numerik
                    fitur = df_clean.select_dtypes(include=['float64', 'int64'])
                    
                    # Jika ada kolom target/label bawaan skripsi lama, drop dulu
                    if 'Anomaly' in fitur.columns:
                        fitur = fitur.drop(columns=['Anomaly'])
                    if 'label' in fitur.columns:
                        fitur = fitur.drop(columns=['label'])
                    
                    # 🚨 REM DARURAT: Cek apakah data fitur kosong sebelum dimasukkan ke model
                    if fitur.empty or list(fitur.columns) == []:
                        st.error(f"🚨 **[{ai_agent.name}]:** 'Proses dihentikan! Saya tidak menemukan kolom angka (numerik) yang cocok untuk dimasukkan ke dalam model Isolation Forest.'")
                        st.warning("📊 **Analisis Masalah:** Tipe data kolom kamu saat ini terbaca sebagai teks (object). Silakan cek struktur file Anda di bawah ini:")
                        st.write(df_clean.dtypes.to_frame(name='Tipe Data Terdeteksi'))
                        st.stop() # Menghentikan streamlit agar tidak memicu error crash Python
                        
                    prediksi = ai_agent.analyze(fitur)
                
                # --- PROSES AGEN 3 ---
                with st.spinner(f"⏳ {expert_agent.name} sedang bekerja..."):
                    time.sleep(1.5)
                    status, pesan = expert_agent.conclude(prediksi)
                
                st.write(f"🟣 **[{expert_agent.name}]:** 'Hasil komputasi selesai dianalisis. Saya merumuskan laporan akhir untuk Dashboard.'")
                
                # --- HASIL AKHIR ---
                st.write("---")
                st.subheader("📊 Laporan Diagnosis Akhir Sistem")
                
                # Tampilkan hasil berdasarkan status dari Agen Pakar
                if status == "BAHAYA":
                    st.error(f"🚨 STATUS: {status}\n\n{pesan}")
                else:
                    st.success(f"✅ STATUS: {status}\n\n{pesan}")
                    
                # Menambahkan kolom prediksi ke dataframe untuk ditampilkan ke pengguna
                df_clean['Status_Agen_AI'] = ['Anomali' if p == -1 else 'Normal' for p in prediksi]
                
                st.write("### Data Hasil Analisis Agen:")
                st.dataframe(df_clean, use_container_width=True)
                
            else:
                st.error(f"🔴 **[{data_agent.name}]:** 'Format file CSV tidak valid. Proses dihentikan!'")
else:
    st.info("💡 Silakan unggah file CSV sensor terlebih dahulu untuk melihat para agen beraksi.")