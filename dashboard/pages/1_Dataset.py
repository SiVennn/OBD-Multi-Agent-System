import streamlit as st
import pandas as pd
import os

st.title("📂 Dataset Overview")

# 1. Trik Pintar Path: Membuat path otomatis presisi di mana pun terminal dijalankan
current_dir = os.path.dirname(os.path.abspath(__file__))
# Naik 2 tingkat dari 'dashboard/pages' ke 'Penelitian', lalu masuk ke 'Datasheet'
path_csv = os.path.join(current_dir, "../../Datasheet/OBD-Anomaly-Detection/dataset/preprocessing.csv")

# 2. Fitur Cache: Agar dataset tidak di-load ulang setiap kali kamu klik menu
@st.cache_data
def load_data():
    return pd.read_csv(path_csv)

# Memuat data dengan penanganan error jika file belum ada
try:
    df = load_data()

    st.subheader("Preview Dataset")
    # use_container_width=True membuat tabel melebar penuh mengikuti layar
    st.dataframe(df.head(100), use_container_width=True) 

    st.subheader("Informasi Dataset")
    col1, col2, col3 = st.columns(3)

    # Format {len(df):,} memberikan tanda koma separator ribuan (misal: 10,000)
    col1.metric("Jumlah Data (Baris)", f"{len(df):,}")
    col2.metric("Jumlah Kolom (Sensor)", len(df.columns))
    col3.metric("Jumlah Missing Value", df.isnull().sum().sum())

    st.subheader("Tipe Data Sensor")
    # Mengubah tampilan tipe data agar berbentuk tabel dua kolom yang rapi
    df_types = pd.DataFrame(df.dtypes.astype(str), columns=["Tipe Data"])
    df_types.index.name = "Nama Sensor"
    st.dataframe(df_types, use_container_width=True)

except FileNotFoundError:
    st.error(f"❌ Gagal memuat file! Berkas `preprocessing.csv` tidak ditemukan di lokasi: {path_csv}")