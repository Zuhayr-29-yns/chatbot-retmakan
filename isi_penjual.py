
import sqlite3
from pathlib import Path

# Menggunakan database yang sama dengan proyek RetMakan
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "retmakan.db"

# Ganti koordinat None dengan koordinat Google Maps
# yang sudah kamu periksa untuk setiap tempat.
penjual = [
    {
        "name": "Gudeg dan Pecel Lumintu Jember",
        "address": "Jl. Kerta Negara No. 33, Jember Kidul, Kaliwates, Jember",
        "latitude": -8.179241792875262,
        "longitude":  113.68772969414309,
        "menu_keywords": "gudeg, pecel, ayam, masakan jawa",
    },
    {
        "name": "Depot Jawa Timur",
        "address": "Jl. Gatot Subroto No. 8, Kaliwates, Jember",
        "latitude": -8.172781441681916,
        "longitude": 113.70313171534269,
        "menu_keywords": "masakan jawa, masakan indonesia",
    },
    {
        "name": "Soto Ayam Dahlok",
        "address": "Kawasan Gang Dahlok, Kepatihan, Kaliwates, Jember",
        "latitude": -8.169867240673613,
        "longitude": 113.69949022883567,
        "menu_keywords": "soto ayam, soto",
    },
]

# Periksa kelengkapan koordinat sebelum menyimpan
for item in penjual:
    if item["latitude"] is None or item["longitude"] is None:
        raise ValueError(
            f"Koordinat Google Maps belum diisi: {item['name']}"
        )

    if not (-90 <= item["latitude"] <= 90):
        raise ValueError(f"Latitude tidak valid: {item['name']}")

    if not (-180 <= item["longitude"] <= 180):
        raise ValueError(f"Longitude tidak valid: {item['name']}")

with sqlite3.connect(DB_PATH) as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sellers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            menu_keywords TEXT
        )
    """)

    for item in penjual:
        # Hindari memasukkan nama dan alamat yang sama dua kali
        conn.execute("""
            INSERT INTO sellers
                (name, address, latitude, longitude, menu_keywords)
            SELECT ?, ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM sellers
                WHERE name = ? AND address = ?
            )
        """, (
            item["name"],
            item["address"],
            item["latitude"],
            item["longitude"],
            item["menu_keywords"],
            item["name"],
            item["address"],
        ))

print("Proses selesai. Periksa data melalui GET /sellers.")
