# api calls, pagination

import requests
import time

BASE_URL = "https://www.dnd5eapi.co/api"

def fetch_endpoint(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, headers={'Accept': 'application/json'})
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None
    
def get_spells():
    list_data = fetch_endpoint("spells")
    if not list_data or "results" not in list_data:
        print("No spells data found.")
        return []

    spell_summaries = list_data["results"]
    full_spell_data = []

    for spell in spell_summaries:
        index = spell["index"]
        detail = fetch_endpoint(f"spells/{index}")
        if detail:
            full_spell_data.append(detail)

        time.sleep(0.1)
    
    return full_spell_data