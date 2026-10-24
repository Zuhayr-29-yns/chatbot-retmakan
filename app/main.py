
import logging

from fastapi import HTTPException, Query
from pydantic import BaseModel, Field

from app.llm import extract_preferences

from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field

from fastapi.responses import HTMLResponse
from pathlib import Path

from app.database import init_database, get_all_foods, get_food_by_id
from app.recommendation import recommend_foods

from app.database import init_seller_table, get_all_sellers, get_seller_menus, tambah_menu_penjual, cari_menu_penjual
from app.location import find_nearest_sellers


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    init_seller_table()
    yield

app = FastAPI(
    title="Chatbot RetMakan",
    description="API rekomendasi makanan",
    version="0.2.0",
    lifespan=lifespan,
)


class FoodPreference(BaseModel):
    category: str | None = None
    taste: str | None = None
    meal_time: str | None = None
    max_price: int | None = Field(default=None, ge=0)
    max_spicy: int | None = Field(default=None, ge=0, le=3)
    cooking_method: str | None = None


@app.get("/")
def home():
    return {
        "app": "Chatbot RetMakan",
        "status": "berjalan",
    }


@app.get("/foods")
def list_foods():
    return {
        "total": len(get_all_foods()),
        "foods": get_all_foods(),
    }

@app.post("/recommend")
def get_recommendations(preference: FoodPreference):
    results = recommend_foods(
        category=preference.category,
        taste=preference.taste,
        meal_time=preference.meal_time,
        max_price=preference.max_price,
        max_spicy=preference.max_spicy,
        cooking_method=preference.cooking_method,
    )

    return {
        "total": len(results),
        "recommendations": results,
        "message": (
            "Berikut rekomendasi makanan yang cocok."
            if results
            else "Belum ditemukan makanan yang sesuai."
        ),
    }

@app.get("/app", response_class=HTMLResponse)
def chatbot_page():
    html_path = (
        Path(__file__).parent / "templates" / "index.html"
    )
    return html_path.read_text(encoding="utf-8")



logger = logging.getLogger(__name__)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(
            status_code=422,
            detail="Pesan tidak boleh kosong.",
        )

    try:
        raw = extract_preferences(message)

        allowed_categories = {
            "nasi", "mie", "berkuah", "sayuran", "bubur"
        }
        allowed_tastes = {
            "gurih", "manis", "pedas", "asam"
        }
        allowed_times = {"pagi", "siang", "malam"}
        allowed_methods = {
            "digoreng", "ditumis", "direbus", "dibakar"
        }

        category = raw.get("category")
        taste = raw.get("taste")
        meal_time = raw.get("meal_time")
        cooking_method = raw.get("cooking_method")
        max_price = raw.get("max_price")
        max_spicy = raw.get("max_spicy")

        # Validasi hasil ekstraksi sebelum digunakan.
        if category not in allowed_categories:
            category = None

        if taste not in allowed_tastes:
            taste = None

        if meal_time not in allowed_times:
            meal_time = None

        if cooking_method not in allowed_methods:
            cooking_method = None

        if (
            isinstance(max_price, bool)
            or not isinstance(max_price, (int, float))
            or max_price < 0
        ):
            max_price = None
        else:
            max_price = int(max_price)

        if (
            isinstance(max_spicy, bool)
            or not isinstance(max_spicy, int)
            or not 0 <= max_spicy <= 3
        ):
            max_spicy = None

        recommendations = recommend_foods(
            category=category,
            taste=taste,
            meal_time=meal_time,
            max_price=max_price,
            max_spicy=max_spicy,
            cooking_method=cooking_method,
        )

        if recommendations:
            names = ", ".join(
                food["name"] for food in recommendations
            )
            reply = (
                f"Berdasarkan keinginanmu, kamu bisa "
                f"mempertimbangkan: {names}. "
                "Pilihan ini berasal dari database RetMakan."
            )
        else:
            reply = (
                "Belum ditemukan makanan yang cocok "
                "dengan kriteria tersebut. Coba longgarkan "
                "beberapa preferensi."
            )

        return {
            "message": reply,
            "preferences": {
                "category": category,
                "taste": taste,
                "meal_time": meal_time,
                "max_price": max_price,
                "max_spicy": max_spicy,
                "cooking_method": cooking_method,
            },
            "recommendations": recommendations,
        }

    except Exception as exc:
        logger.exception("Pemrosesan chatbot gagal")
        raise HTTPException(
            status_code=502,
            detail=(
                "Chatbot gagal memproses permintaan. "
                "Pastikan Ollama berjalan dan model tersedia."
            ),
        ) from exc

class SellerMenuRequest(BaseModel):
    seller_id: int = Field(gt=0)
    menu_name: str = Field(min_length=1, max_length=100)
    price: int = Field(ge=0)
    is_available: bool = True
    
class LocationRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    max_distance_km: float | None = Field(
        default=5, gt=0, le=100
    )


@app.post("/nearby-sellers")
def nearby_sellers(request: LocationRequest):
    sellers = get_all_sellers()

    if not sellers:
        return {
            "total": 0,
            "sellers": [],
            "message": (
                "Belum ada data penjual. "
                "Tambahkan data penjual terlebih dahulu."
            ),
        }

    results = find_nearest_sellers(
        request.latitude,
        request.longitude,
        sellers,
        max_distance_km=request.max_distance_km,
    )

    for seller in results:
        seller["map_url"] = (
            "https://www.google.com/maps/dir/?api=1"
            f"&destination={seller['latitude']},"
            f"{seller['longitude']}"
        )

    return {
        "total": len(results),
        "sellers": results,
        "message": (
            "Penjual terdekat berhasil ditemukan."
            if results
            else "Tidak ditemukan penjual dalam radius tersebut."
        ),
    }


@app.get("/sellers")
def list_sellers():
    sellers = get_all_sellers()

    return {
        "total": len(sellers),
        "sellers": sellers,
    }

@app.get("/seller-menus")
def list_seller_menus():
    menus = get_seller_menus()

    return {
        "total": len(menus),
        "menus": menus,
    }


@app.get("/seller-menus/{seller_id}")
def list_menus_by_seller(seller_id: int):
    sellers = get_all_sellers()
    seller_exists = any(
        seller["id"] == seller_id for seller in sellers
    )

    if not seller_exists:
        raise HTTPException(
            status_code=404,
            detail="Penjual tidak ditemukan.",
        )

    menus = get_seller_menus(seller_id)

    return {
        "seller_id": seller_id,
        "total": len(menus),
        "menus": menus,
    }


@app.post("/seller-menus")
def create_seller_menu(request: SellerMenuRequest):
    try:
        tambah_menu_penjual(
            seller_id=request.seller_id,
            menu_name=request.menu_name,
            price=request.price,
            is_available=int(request.is_available),
        )

        return {
            "message": "Menu penjual berhasil ditambahkan.",
            "menu": {
                "seller_id": request.seller_id,
                "menu_name": request.menu_name.strip(),
                "price": request.price,
                "is_available": request.is_available,
            },
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
        
@app.get("/search-seller-menus")
def search_seller_menus(
    keyword: str | None = None,
    max_price: int | None = Query(default=None, ge=0),
):
    menus = cari_menu_penjual(
        keyword=keyword,
        max_price=max_price,
    )

    return {
        "total": len(menus),
        "menus": menus,
        "message": (
            "Menu yang sesuai berhasil ditemukan."
            if menus
            else "Menu yang sesuai belum ditemukan."
        ),
    }