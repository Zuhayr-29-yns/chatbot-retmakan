
# Chatbot RetMakan

Chatbot RetMakan adalah aplikasi rekomendasi makanan berbasis AI yang membantu pengguna mencari rekomendasi makanan dan penjual berdasarkan kebutuhan pengguna. Aplikasi ini menggunakan model bahasa lokal melalui Ollama, database SQLite, serta fitur pencarian penjual berdasarkan lokasi pengguna.

## ✨ Fitur Utama

- Chatbot AI untuk membantu pengguna memperoleh rekomendasi makanan.
- Rekomendasi makanan berdasarkan kebutuhan pengguna.
- Pencarian menu makanan yang tersedia pada database.
- Pencarian penjual makanan berdasarkan lokasi pengguna.
- Pencarian penjual terdekat berdasarkan radius jarak.
- Filter menu berdasarkan harga maksimum.
- Pemanfaatan GPS melalui Browser Geolocation API.
- Integrasi Google Maps Directions URL untuk membantu navigasi menuju penjual.
- Database SQLite untuk menyimpan data makanan, penjual, dan menu.
- Model AI lokal menggunakan Ollama dengan model `qwen2.5:3b`.

## 🛠️ Teknologi yang Digunakan

- **Bahasa pemrograman:** Python
- **Framework backend:** FastAPI
- **Database:** SQLite
- **Model AI:** Ollama `qwen2.5:3b`
- **Antarmuka:** HTML
- **Lokasi pengguna:** Browser Geolocation API
- **Navigasi:** Google Maps Directions URL
- **Server aplikasi:** Uvicorn

## 📋 Persyaratan

Sebelum menjalankan aplikasi, pastikan perangkat sudah memiliki:

- Python yang kompatibel dengan dependensi pada `requirements.txt`.
- Git untuk mengunduh repositori.
- Ollama yang sudah terinstal dan dapat dijalankan.
- Model AI `qwen2.5:3b`.
- Browser modern yang mendukung JavaScript dan Geolocation API.

## 🚀 Instalasi dan Menjalankan Aplikasi

### 1. Clone Repository

Buka CMD atau terminal, lalu jalankan:

```bash
git clone https://github.com/Zuhayr-29-yns/chatbot-retmakan.git
cd chatbot-retmakan
```

### 2. Buat Virtual Environment

Jalankan perintah berikut untuk membuat lingkungan Python terpisah:

```bash
py -m venv .venv
```

### 3. Instal Dependensi

Instal seluruh pustaka yang dibutuhkan oleh aplikasi:

```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Siapkan Model AI

Pastikan Ollama sudah terinstal dan berjalan. Kemudian, unduh model AI yang digunakan aplikasi:

```bash
ollama pull qwen2.5:3b
```

Model tersebut dijalankan secara lokal melalui Ollama.

### 5. Siapkan Database dan Data Demo

Jalankan skrip inisialisasi database dan data demo:

```bash
.venv\Scripts\python.exe isi_data_demo.py
```

Skrip ini menyiapkan tabel database serta data demo penjual dan menu untuk kebutuhan pengujian. Data yang sudah ada tidak sengaja dihapus oleh skrip tersebut.

**Catatan:** Data penjual, lokasi, menu, dan harga demo digunakan untuk pengujian. Verifikasi terlebih dahulu sebelum menggunakannya sebagai data aktual.

### 6. Jalankan Aplikasi

Jalankan server FastAPI menggunakan Uvicorn:

```bash
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Setelah server berjalan, biarkan terminal tetap terbuka selama aplikasi digunakan.

### 7. Buka Aplikasi

Akses alamat berikut melalui browser:

- **Antarmuka aplikasi:** http://127.0.0.1:8000/app
- **Dokumentasi API:** http://127.0.0.1:8000/docs

## 📍 Penggunaan GPS

Untuk menggunakan fitur pencarian penjual terdekat:

1. Buka aplikasi melalui browser.
2. Aktifkan fitur pencarian berdasarkan lokasi jika tersedia.
3. Izinkan browser mengakses lokasi perangkat.
4. Gunakan fitur pencarian penjual terdekat sesuai kebutuhan.
5. Atur radius pencarian apabila fitur tersebut tersedia.
6. Gunakan tautan navigasi untuk membuka petunjuk arah menuju penjual.

Hasil pencarian bergantung pada ketersediaan data penjual, koordinat lokasi, menu, harga, serta izin akses lokasi dari browser.

## 🗄️ Database

Chatbot RetMakan menggunakan SQLite sebagai penyimpanan data lokal.

Database digunakan untuk menyimpan data yang diperlukan oleh aplikasi, termasuk:

- Data makanan.
- Data penjual.
- Data menu penjual.

File database lokal tidak disertakan dalam repository. Jalankan skrip `isi_data_demo.py` untuk menyiapkan database dan data demo sebelum mencoba fitur pencarian penjual dan menu.

## 📂 Struktur Proyek

```text
Chatbot RetMakan/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── location.py
│   ├── recommendation.py
│   ├── llm.py
│   └── templates/
│       └── index.html
├── data/
├── isi_penjual.py
├── isi_data_demo.py
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚠️ Catatan

- Pastikan dependensi sudah terinstal sebelum menjalankan aplikasi.
- Pastikan layanan Ollama berjalan ketika fitur chatbot AI digunakan.
- Database SQLite lokal tidak disertakan dalam repository.
- Data demo penjual, koordinat, menu, dan harga perlu diverifikasi sebelum dianggap sebagai data aktual.
- Fitur GPS memerlukan izin pengguna dan dukungan Geolocation API pada browser.
- Hasil pencarian penjual terdekat bergantung pada data lokasi yang tersedia.
- Google Maps digunakan melalui tautan navigasi; konfigurasi tambahan mungkin diperlukan jika implementasi aplikasi berubah.

## 👨‍💻 Pengembang

**Zuhayr-29-yns**

Repository GitHub: https://github.com/Zuhayr-29-yns/chatbot-retmakan
