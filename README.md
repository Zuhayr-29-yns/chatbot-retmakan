# 🍽️ Chatbot RetMakan

Chatbot RetMakan adalah aplikasi rekomendasi makanan berbasis AI yang membantu pengguna menemukan pilihan makanan sesuai preferensi dan anggaran, serta mencari penjual makanan terdekat berdasarkan lokasi GPS.

## ✨ Fitur Utama

- Chatbot AI yang memproses pesan pengguna dalam bahasa alami.
- Rekomendasi makanan berdasarkan jenis, rasa, waktu makan, anggaran, tingkat kepedasan, dan metode memasak.
- Pencarian penjual makanan berdasarkan lokasi GPS.
- Filter jarak pencarian 5 km, 10 km, 25 km, dan 50 km.
- Pencarian menu berdasarkan nama makanan dan anggaran.
- Informasi penjual, alamat, harga menu, jarak, dan tautan rute Google Maps.

## 🛠️ Teknologi

- Python
- FastAPI
- Ollama dengan model `qwen2.5:3b`
- SQLite
- HTML, CSS, dan JavaScript
- Browser Geolocation API
- Google Maps Directions URL

## 📋 Persyaratan

- Python yang kompatibel dengan dependensi proyek.
- Ollama terpasang di komputer.
- Model `qwen2.5:3b` tersedia di Ollama.
- Browser modern untuk mengakses antarmuka dan fitur GPS.

## 🚀 Instalasi dan Menjalankan Aplikasi

### 1. Clone repositori

```bash
git clone https://github.com/USERNAME/chatbot-retmakan.git
cd chatbot-retmakan
```

Ganti `USERNAME` dengan nama pengguna GitHub pemilik repositori.

### 2. Buat virtual environment

Windows:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instal dependensi

```cmd
python -m pip install -r requirements.txt
```

### 4. Siapkan Ollama

Pastikan Ollama sudah terpasang dan model tersedia:

```cmd
ollama pull qwen2.5:3b
```

Pastikan layanan Ollama berjalan sebelum menggunakan fitur chatbot.

### 5. Jalankan aplikasi

```cmd
uvicorn app.main:app --reload
```

### 6. Buka aplikasi

- Antarmuka RetMakan: http://127.0.0.1:8000/app
- Dokumentasi API: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## 📍 Penggunaan GPS

Izinkan akses lokasi melalui browser untuk mencari penjual di sekitar pengguna. Hasil pencarian bergantung pada data penjual, koordinat, menu, dan harga yang tersedia di database.

## 📂 Struktur Proyek

```text
FoodMateAI/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── location.py
│   ├── recommendation.py
│   ├── llm.py
│   └── templates/
│       └── index.html
├── data/
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚠️ Catatan

- Database lokal tidak disertakan dalam repositori. Siapkan atau inisialisasi database sesuai implementasi aplikasi sebelum menggunakan fitur penjual.
- Data penjual dan harga perlu diisi dengan data yang benar.
- Akses GPS memerlukan izin pengguna dan konteks browser yang mendukung Geolocation API.
- Model AI dijalankan secara lokal melalui Ollama.

## 🎓 Tujuan Proyek

Proyek ini dibuat sebagai implementasi chatbot berbasis AI untuk pelatihan, dengan use case rekomendasi makanan dan integrasi pencarian penjual berdasarkan lokasi.
