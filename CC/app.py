import os
import numpy as np
from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import requests
from io import BytesIO
from google.cloud import firestore

# Menetapkan path ke file kredensial Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./apk-scan-buah-9013695ecf45.json"

app = Flask(__name__)

# Inisialisasi klien Firestore
db = firestore.Client()

def download_model_from_url(url):
    """
    Mengunduh model dari URL dan memuatnya dalam memori.
    """
    print(f"Downloading model from {url}...")
    response = requests.get(url)
    print(f"HTTP status code: {response.status_code}")  # Menambahkan logging status kode
    
    if response.status_code == 200:
        # Memuat model jika statusnya 200 (OK)
        model_file = BytesIO(response.content)
        return load_model(model_file)
    else:
        raise Exception(f"Failed to download model from {url}, status code: {response.status_code}")

# URL tempat model Anda disimpan
model_url = 'https://storage.googleapis.com/apkbuah/model_fruit.h5'

# Coba memuat model dari URL
try:
    model = download_model_from_url(model_url)
    if model is None:
        raise Exception("Model is None")
    print("Model loaded successfully from URL.")
except Exception as e:
    print(f"Error loading model from URL: {str(e)}")
    print("Falling back to loading model from local file.")
    try:
        # Jika unduhan gagal, coba memuat model dari file lokal
        model = load_model('model_fruit.h5')  # Pastikan file model tersedia di folder proyek Anda
        print("Model loaded successfully from local file.")
    except Exception as e:
        print(f"Error loading model from local file: {str(e)}")
        model = None

def process_image(image):
    """
    Mengolah gambar yang diterima untuk diprediksi oleh model.
    """
    image = image.convert('RGB')
    image = image.resize((224, 224))  # Ukuran input model, misalnya 224x224
    image_array = np.array(image) / 255.0  # Normalisasi
    image_array = np.expand_dims(image_array, axis=0)  # Menambah dimensi untuk batch
    return image_array

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint untuk menerima gambar dan mengembalikan prediksi dari model.
    """
    if model is None:
        return jsonify({'error': 'Model not loaded properly, please check your model URL or file.'}), 500
    
    try:
        # Mengambil file gambar dari permintaan
        file = request.files['input']
        filename = file.filename  # Mendapatkan nama file gambar
        image = Image.open(file.stream)  # Memuat gambar dari stream file
        input_data = process_image(image)  # Mengolah gambar agar sesuai dengan input model

        # Melakukan prediksi dengan model
        prediction = model.predict(input_data)
        prediction_value = prediction.tolist()[0][0]  # Mendapatkan nilai prediksi sebagai angka

        # Mengonversi prediksi ke label
        deskripsi = {
            0: "Segar",
            1: "Busuk",
        }

        prediction_label = deskripsi[round(prediction_value)]  # Pembulatan untuk mendapatkan label

        # Menyimpan prediksi ke Firestore dengan document ID sesuai nama file
        save_prediction_to_firestore(filename, prediction_value, prediction_label)

        # Mengembalikan angka prediksi dan label deskripsi
        return jsonify({
            'hasil': prediction_label,
            'akurasi busuk': prediction_value,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

def save_prediction_to_firestore(filename, prediction_value, prediction_label):
    """
    Fungsi untuk menyimpan hasil prediksi ke Firestore dengan nama file sebagai document ID.
    """
    db = firestore.Client()  # Pastikan Anda sudah mengkonfigurasi Firestore client sebelumnya
    doc_ref = db.collection('predictions').document(filename)  # Menggunakan nama file sebagai ID dokumen
    doc_ref.set({
        'prediction_value': prediction_value,
        'prediction_label': prediction_label,
        'timestamp': firestore.SERVER_TIMESTAMP  # Menambahkan timestamp untuk referensi
    })


@app.route('/')
@app.route('/index')
def index():
    """
    Endpoint untuk memeriksa status aplikasi.
    """
    return jsonify({'message': 'running..'})

if __name__ == '__main__':
    # Jalankan aplikasi Flask
    app.run(debug=False, host='0.0.0.0', port=8080)
