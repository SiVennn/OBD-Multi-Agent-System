import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📈 Visualisasi Sensor OBD-II")
st.write("Halaman ini digunakan untuk menganalisis hubungan antar-sensor dan tren data kendaraan.")

# Trik amankan Path berkas
current_dir = os.path.dirname(os.path.abspath(__file__))
path_csv = os.path.join(current_dir, "../../Datasheet/OBD-Anomaly-Detection/dataset/preprocessing.csv")
path_heatmap = os.path.join(current_dir, "../../gambar/heatmap.png")

@st.cache_data
def load_data():
    if os.path.exists(path_csv):
        return pd.read_csv(path_csv)
    return None

df = load_data()

if df is not None:
    # Membuat dua Tab agar tampilan rapi dan tidak memanjang ke bawah
    tab1, tab2 = st.tabs(["📊 Korelasi Antar Sensor", "📉 Tren Nilai Sensor"])
    
# ---------------------------------------------------------
    # TAB 1: HEATMAP KORELASI (Dinamis & Anti-Blank)
    # ---------------------------------------------------------
    with tab1:
        st.subheader("Matriks Korelasi (Heatmap) Dinamis")
        st.write("Membantu melihat sensor mana saja yang saling memengaruhi satu sama lain secara real-time.")
        
        # Memastikan hanya kolom berisi angka (numerik) yang dihitung korelasinya
        # Ini mencegah error jika dataset kamu memiliki kolom teks/waktu
        df_numerik = df.select_dtypes(include=['int64', 'float64'])
        
        if not df_numerik.empty:
            # 1. Membuat objek grafik matplotlib
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # 2. Menggambar heatmap dengan seaborn
            sns.heatmap(
                df_numerik.corr(), 
                annot=True, 
                cmap="coolwarm", 
                fmt=".2f", 
                ax=ax, 
                cbar=True,
                linewidths=0.5
            )
            
            # 3. Mengatur layout agar teks tidak terpotong
            plt.tight_layout()
            
            # 4. Tampilkan grafik langsung ke layar Streamlit
            st.pyplot(fig)
        else:
            st.warning("⚠️ Tidak ditemukan kolom numerik di dataset untuk membuat heatmap.")
    # ---------------------------------------------------------
    # TAB 2: TREN SENSOR (LINE CHART)
    # ---------------------------------------------------------
    with tab2:
        st.subheader("Analisis Pergerakan Sensor")
        st.write("Pilih salah satu fitur sensor untuk melihat grafik tren nilainya sepanjang waktu.")
        
        # Dropdown interaktif untuk memilih kolom sensor
        sensor_terpilih = st.selectbox("Pilih Sensor/Fitur OBD-II:", df.columns)
        
        # Batasi 1000 data pertama agar browser tidak berat/lag saat rendering grafik
        st.write(f"Grafik Tren untuk **{sensor_terpilih}** (1000 sampel pertama):")
        st.line_chart(df[sensor_terpilih].head(1000))
        
else:
    st.error(f"❌ Gagal memuat data! Berkas `preprocessing.csv` tidak ditemukan di lokasi: {path_csv}")