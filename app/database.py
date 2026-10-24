
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "retmakan.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection



def init_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS foods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                taste TEXT NOT NULL,
                spicy_level INTEGER NOT NULL,
                meal_time TEXT NOT NULL,
                price INTEGER NOT NULL,
                cooking_method TEXT NOT NULL,
                calories REAL,
                protein REAL,
                description TEXT
            )
        """)

        total = conn.execute(
            "SELECT COUNT(*) FROM foods"
        ).fetchone()[0]

        if total == 0:
            foods = [
                (
                    "Nasi Ayam Geprek", "nasi", "gurih", 3,
                    "siang,malam", 15000, "digoreng",
                    None, None, "Nasi dengan ayam dan sambal."
                ),
                (
                    "Nasi Goreng", "nasi", "gurih", 2,
                    "malam", 15000, "ditumis",
                    None, None, "Nasi yang dimasak dengan bumbu."
                ),
                (
                    "Soto Ayam", "berkuah", "gurih", 1,
                    "pagi,siang,malam", 12000, "direbus",
                    None, None, "Sup ayam dengan kuah berbumbu."
                ),
                (
                    "Mie Ayam", "mie", "gurih", 1,
                    "siang,malam", 12000, "direbus",
                    None, None, "Mi dengan ayam berbumbu."
                ),
                (
                    "Gado-Gado", "sayuran", "gurih", 0,
                    "siang", 12000, "campuran",
                    None, None, "Sayuran dengan saus kacang."
                ),
                (
                    "Pecel Lele", "nasi", "gurih", 2,
                    "malam", 17000, "digoreng",
                    None, None, "Nasi dengan ikan lele dan sambal."
                ),
                (
                    "Bubur Ayam", "bubur", "gurih", 0,
                    "pagi", 10000, "direbus",
                    None, None, "Bubur dengan suwiran ayam."
                ),
                (
                    "Nasi Ayam Bakar", "nasi", "gurih", 1,
                    "siang,malam", 18000, "dibakar",
                    None, None, "Nasi dengan ayam berbumbu bakar."
                ),
            ]

            conn.executemany("""
                INSERT INTO foods (
                    name, category, taste, spicy_level,
                    meal_time, price, cooking_method,
                    calories, protein, description
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, foods)



def get_all_foods():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM foods ORDER BY name"
        ).fetchall()

    return [dict(row) for row in rows]


def get_food_by_id(food_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM foods WHERE id = ?",
            (food_id,)
        ).fetchone()

    return dict(row) if row else None  


def init_seller_table():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sellers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                menu_keywords TEXT NOT NULL DEFAULT ''
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS seller_menus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                seller_id INTEGER NOT NULL,
                menu_name TEXT NOT NULL,
                price INTEGER NOT NULL CHECK (price >= 0),
                is_available INTEGER NOT NULL DEFAULT 1
                    CHECK (is_available IN (0, 1)),
                FOREIGN KEY (seller_id)
                    REFERENCES sellers(id)
                    ON DELETE CASCADE
            )
        """)



def get_all_sellers():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT *
            FROM sellers
        """).fetchall()

    return [dict(row) for row in rows]


def get_seller_menus(seller_id=None):
    with get_connection() as conn:
        if seller_id is None:
            rows = conn.execute("""
                SELECT
                    sm.id,
                    sm.seller_id,
                    s.name AS seller_name,
                    sm.menu_name,
                    sm.price,
                    sm.is_available
                FROM seller_menus sm
                JOIN sellers s ON s.id = sm.seller_id
                ORDER BY s.name, sm.menu_name
            """).fetchall()
        else:
            rows = conn.execute("""
                SELECT
                    sm.id,
                    sm.seller_id,
                    s.name AS seller_name,
                    sm.menu_name,
                    sm.price,
                    sm.is_available
                FROM seller_menus sm
                JOIN sellers s ON s.id = sm.seller_id
                WHERE sm.seller_id = ?
                ORDER BY sm.menu_name
            """, (seller_id,)).fetchall()

    return [dict(row) for row in rows]

def tambah_menu_penjual(seller_id, menu_name, price, is_available=1):
    menu_name = menu_name.strip()

    if not menu_name:
        raise ValueError("Nama menu tidak boleh kosong.")

    if price < 0:
        raise ValueError("Harga menu tidak boleh negatif.")

    if is_available not in (0, 1):
        raise ValueError("Status ketersediaan harus 0 atau 1.")

    with get_connection() as conn:
        seller = conn.execute(
            "SELECT id FROM sellers WHERE id = ?",
            (seller_id,)
        ).fetchone()

        if seller is None:
            raise ValueError("Penjual tidak ditemukan.")

        conn.execute("""
            INSERT INTO seller_menus
                (seller_id, menu_name, price, is_available)
            VALUES (?, ?, ?, ?)
        """, (seller_id, menu_name, price, is_available))

def cari_menu_penjual(keyword=None, max_price=None):
    query = """
        SELECT
            sm.id,
            sm.seller_id,
            s.name AS seller_name,
            s.address,
            s.latitude,
            s.longitude,
            sm.menu_name,
            sm.price,
            sm.is_available
        FROM seller_menus sm
        JOIN sellers s ON s.id = sm.seller_id
        WHERE sm.is_available = 1
    """
    params = []

    if keyword and keyword.strip():
        query += " AND LOWER(sm.menu_name) LIKE LOWER(?)"
        params.append(f"%{keyword.strip()}%")

    if max_price is not None:
        query += " AND sm.price <= ?"
        params.append(max_price)

    query += " ORDER BY sm.price ASC, s.name ASC"

    with get_connection() as conn:
        rows = conn.execute(query, params).fetchall()

    return [dict(row) for row in rows]