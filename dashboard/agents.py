import pandas as pd
import joblib

# ====================================================
# 1. AGEN DATA
# ====================================================
class DataAgent:
    def __init__(self):
        self.name = "Data Collector Agent"

    def process_data(self, uploaded_file):
        """Membaca file CSV yang diunggah pengguna dengan deteksi otomatis pemisah"""
        try:
            df = pd.read_csv(uploaded_file, sep=None, engine='python')
            return df
        except Exception as e:
            return None
        
# ====================================================
# 2. AGEN AI / DETEKSI (VERSI UPGRADE)
# ====================================================
class AnomalyDetectionAgent:
    def __init__(self, model_path):
        self.name = "AI Detection Agent"
        self.model = joblib.load(model_path)
        
        # Mengecek "ingatan" model: kolom apa saja yang dia butuhkan?
        if hasattr(self.model, 'feature_names_in_'):
            self.expected_features = list(self.model.feature_names_in_)
        else:
            self.expected_features = None

    def analyze(self, data):
        """Melakukan prediksi anomali dengan adaptasi kolom otomatis"""
        
        # Jika model mengingat kolom spesifik, agen akan menyesuaikan data secara paksa
        if self.expected_features is not None:
            # 1. Jika ada kolom yang kurang, agen akan membuatnya dan mengisinya dengan angka 0
            for col in self.expected_features:
                if col not in data.columns:
                    data[col] = 0
                    
            # 2. Agen akan membuang kolom yang tidak dikenali model dan mengurutkannya
            data_ready = data[self.expected_features]
        else:
            data_ready = data
            
        # 3. Lakukan prediksi pada data yang sudah dirapikan
        predictions = self.model.predict(data_ready)
        return predictions

# ====================================================
# 3. AGEN PAKAR
# ====================================================
class DiagnosticAgent:
    def __init__(self):
        self.name = "Expert Diagnostic Agent"

    def conclude(self, predictions):
        """Menganalisis hasil prediksi dan memberikan laporan"""
        total_data = len(predictions)
        anomalies = list(predictions).count(-1)
        
        if anomalies > 0:
            status = "BAHAYA"
            pesan = f"Mendeteksi {anomalies} titik anomali dari {total_data} data sensor. Diperlukan pengecekan mesin segera!"
        else:
            status = "AMAN"
            pesan = f"Semua {total_data} data sensor normal. Kondisi kendaraan prima."
            
        return status, pesan