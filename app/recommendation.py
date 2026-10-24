
from app.database import get_all_foods


def recommend_foods(
    category=None,
    taste=None,
    meal_time=None,
    max_price=None,
    max_spicy=None,
    cooking_method=None,
    limit=5,
):
    foods = get_all_foods()
    results = []

    for food in foods:
        score = 0

        # Filter kriteria yang wajib dipenuhi.
        if max_price is not None and food["price"] > max_price:
            continue

        if max_spicy is not None:
            if food["spicy_level"] > max_spicy:
                continue

        if category:
            if category.lower() not in food["category"].lower():
                continue
            score += 2

        if taste:
            if taste.lower() != food["taste"].lower():
                continue
            score += 2

        if meal_time:
            times = food["meal_time"].lower().split(",")
            if meal_time.lower() not in times:
                continue
            score += 1

        if cooking_method:
            if cooking_method.lower() != food["cooking_method"].lower():
                continue
            score += 1

        food["score"] = score
        results.append(food)

    results.sort(
        key=lambda item: (
            -item["score"],
            item["price"],
            item["name"],
        )
    )

    return results[:limit]
