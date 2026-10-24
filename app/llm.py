
import json
from urllib.request import Request, urlopen


OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"


def extract_preferences(message: str) -> dict:
    prompt = f"""
Kamu bertugas mengekstrak preferensi makanan dari pesan pengguna.

Kembalikan hanya JSON valid dengan field:
category, taste, meal_time, max_price, max_spicy, cooking_method.

Aturan:
- category: nasi, mie, berkuah, sayuran, bubur, atau null.
- taste: gurih, manis, pedas, asam, atau null.
- meal_time: pagi, siang, malam, atau null.
- max_price: bilangan rupiah atau null.
- max_spicy: bilangan 0 sampai 3 atau null.
- cooking_method: digoreng, ditumis, direbus, dibakar,
  atau null.
- Jangan menebak preferensi yang tidak disebutkan.
- "agak pedas" dapat diartikan sebagai max_spicy 2.
- "tidak terlalu pedas" dapat diartikan sebagai max_spicy 1.

Pesan pengguna:
{message}
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0,
            "num_predict": 150,
        },
    }

    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))

    content = result["message"]["content"]
    preferences = json.loads(content)

    if not isinstance(preferences, dict):
        raise ValueError("Format preferensi dari model tidak valid.")

    return preferences
