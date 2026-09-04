import requests


def get_weather(latitude, longitude):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,rain,weather_code"
    )

    try:

        response = requests.get(
            url,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        return None

    except requests.RequestException:
        return None