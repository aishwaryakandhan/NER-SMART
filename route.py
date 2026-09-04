import requests


def get_routes(start_lat, start_lon, end_lat, end_lon):

    url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{start_lon},{start_lat};{end_lon},{end_lat}"
    )

    params = {
        "alternatives": "true",
        "steps": "false",
        "overview": "full",
        "geometries": "geojson"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        if response.status_code != 200:
            return []

        data = response.json()

        if data.get("code") != "Ok":
            return []

        routes = []

        for route in data.get("routes", []):

            routes.append({
                "distance": route["distance"] / 1000,
                "duration": route["duration"] / 3600,
                "geometry": route["geometry"]["coordinates"]
            })

        return routes

    except requests.RequestException:
        return []