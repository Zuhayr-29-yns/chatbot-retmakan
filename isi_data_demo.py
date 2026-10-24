
import sqlite3

from app.database import DB_PATH, init_database, init_seller_table


# DATA DEMO UNTUK PENGUJIAN CHATBOT RETMAKAN
# Nama, alamat, koordinat, menu, dan harga perlu diverifikasi
# sebelum digunakan sebagai data aktual.

PENJUAL_DEMO = [
    {
        "name": "Gudeg dan Pecel Lumintu Jember",
        "address": "Jl. Kerta Negara No. 33, Jember Kidul, Kaliwates, Jember",
        "latitude": -8.179241792875262,
        "longitude": 113.68772969414309,
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

MENU_DEMO = [
    ("Gudeg dan Pecel Lumintu Jember", "Nasi Ayam Geprek", 15000),
    ("Gudeg dan Pecel Lumintu Jember", "Nasi Pecel", 12000),
    ("Gudeg dan Pecel Lumintu Jember", "Soto Ayam", 15000),
    ("Depot Jawa Timur", "Nasi Goreng", 15000),
    ("Soto Ayam Dahlok", "Soto Ayam", 15000),
]


def main():
    # Membuat database dan tabel jika belum tersedia.
    init_database()
    init_seller_table()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")

        # Memasukkan penjual tanpa menduplikasi nama dan alamat.
        for item in PENJUAL_DEMO:
            conn.execute(
                """
                INSERT INTO sellers (
                    name, address, latitude, longitude, menu_keywords
                )
                SELECT ?, ?, ?, ?, ?
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM sellers
                    WHERE name = ? AND address = ?
                )
                """,
                (
                    item["name"],
                    item["address"],
                    item["latitude"],
                    item["longitude"],
                    item["menu_keywords"],
                    item["name"],
                    item["address"],
                ),
            )

        # Memasukkan menu untuk penjual yang sesuai.
        for seller_name, menu_name, price in MENU_DEMO:
            seller = conn.execute(
                """
                SELECT id
                FROM sellers
                WHERE name = ?
                ORDER BY id
                LIMIT 1
                """,
                (seller_name,),
            ).fetchone()

            if seller is None:
                raise RuntimeError(
                    f"Penjual tidak ditemukan: {seller_name}"
                )

            conn.execute(
                """
                INSERT INTO seller_menus (
                    seller_id, menu_name, price, is_available
                )
                SELECT ?, ?, ?, 1
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM seller_menus
                    WHERE seller_id = ? AND menu_name = ?
                )
                """,
                (
                    seller[0],
                    menu_name,
                    price,
                    seller[0],
                    menu_name,
                ),
            )

        total_penjual = conn.execute(
            "SELECT COUNT(*) FROM sellers"
        ).fetchone()[0]

        total_menu = conn.execute(
            "SELECT COUNT(*) FROM seller_menus"
        ).fetchone()[0]

    print("Inisialisasi data demo selesai.")
    print(f"Jumlah seluruh penjual: {total_penjual}")
    print(f"Jumlah seluruh menu: {total_menu}")
    print("Data yang sudah ada tidak dihapus.")


if __name__ == "__main__":
    main()
