import requests


NER_STATES = [
    "Assam",
    "Arunachal Pradesh",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Tripura",
    "Sikkim"
]


def search_location(place):

    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": place,
        "format": "jsonv2",
        "limit": 10,
        "countrycodes": "in",
        "viewbox": "88.0,29.5,97.5,21.5",
        "bounded": 1,
        "addressdetails": 1
    }

    headers = {
        "User-Agent": "NER-SMART-SIH-Prototype/1.0"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return []

        results = response.json()

        ner_results = []

        for result in results:

            address = result.get("address", {})

            state = address.get("state", "")

            if state in NER_STATES:
                ner_results.append(result)

        return ner_results

    except requests.RequestException:
        return []