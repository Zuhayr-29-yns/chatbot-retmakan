
from math import radians, sin, cos, asin, sqrt


def haversine_distance(lat1, lon1, lat2, lon2):
    """Menghitung jarak garis lurus dalam kilometer."""
    earth_radius_km = 6371.0

    lat1, lon1, lat2, lon2 = map(
        radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    a = min(1.0, max(0.0, a))

    return 2 * earth_radius_km * asin(sqrt(a))


def find_nearest_sellers(
    user_lat,
    user_lon,
    sellers,
    limit=5,
    max_distance_km=None,
):
    results = []

    for seller in sellers:
        distance = haversine_distance(
            user_lat,
            user_lon,
            seller["latitude"],
            seller["longitude"],
        )

        if (
            max_distance_km is not None
            and distance > max_distance_km
        ):
            continue

        result = dict(seller)
        result["distance_km"] = round(distance, 2)
        results.append(result)

    results.sort(key=lambda item: item["distance_km"])

    return results[:limit]
