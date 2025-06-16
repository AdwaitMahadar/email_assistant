import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def geocode_location(location_name: str) -> tuple:
    """
    Convert a location name to (latitude, longitude) using the Geocoding API.
    """
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location_name,
        "key": GOOGLE_MAPS_API_KEY
    }
    resp = requests.get(endpoint, params=params).json()

    if resp["status"] == "OK" and resp["results"]:
        loc = resp["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    else:
        raise ValueError(f"Could not geocode location: {location_name}")

def find_nearby_places_v1(query: str, location_name: str, limit: int = 3) -> list:
    """
    Use Google Places API v1 (Nearby Search - New) to find top places near a location.
    """
    lat, lng = geocode_location(location_name)

    endpoint = "https://places.googleapis.com/v1/places:searchNearby"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating"
    }

    payload = {
        "includedPrimaryTypes": [query],  # e.g., 'restaurant', 'cafe'
        "maxResultCount": limit,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lng
                },
                "radius": 1500.0
            }
        }
    }

    resp = requests.post(endpoint, headers=headers, json=payload).json()

    places = []
    for place in resp.get("places", []):
        name = place.get("displayName", {}).get("text", "Unnamed")
        address = place.get("formattedAddress", "Unknown address")
        rating = place.get("rating", "N/A")
        places.append({
            "name": name,
            "address": address,
            "rating": rating
        })

    return places

if __name__ == "__main__":
    try:
        test_places = find_nearby_places_v1("restaurant", "Palo Alto")
        for i, p in enumerate(test_places, start=1):
            print(f"{i}. {p['name']} — {p['address']} (Rating: {p['rating']})")
    except Exception as e:
        print(f"Error: {e}")
