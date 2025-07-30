# utils/api_utils.py - This module contains functions related to the API.
#API info: 'https://www.recreation.gov/api/camps/availability/campground/233870/month?start_date=2024-01-01T00%3A00%3A00.000Z'

import requests
from datetime import datetime
from urllib.parse import urlencode

# Cache for campground names to avoid repeated API calls
_campground_name_cache = {}

def fetch_campground_name(campground_id: str):
    """Fetch the campground name from recreation.gov API with caching"""
    # Check cache first
    if campground_id in _campground_name_cache:
        return _campground_name_cache[campground_id]
    
    API_URL = f"https://www.recreation.gov/api/camps/campgrounds/{campground_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(API_URL, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            name = data["campground"]["facility_name"]
            # Cache the result
            _campground_name_cache[campground_id] = name
            return name
        elif response.status_code == 404:
            name = f"Campground {campground_id} (name not found)"
            _campground_name_cache[campground_id] = name
            return name
        else:
            name = f"Campground {campground_id} (error fetching name)"
            _campground_name_cache[campground_id] = name
            return name
            
    except requests.exceptions.RequestException as e:
        name = f"Campground {campground_id} (network error)"
        _campground_name_cache[campground_id] = name
        return name
    except Exception as e:
        name = f"Campground {campground_id} (unexpected error)"
        _campground_name_cache[campground_id] = name
        return name

def fetch_campground_data(campground_id: str, month: int, year: int):
    # Format the date to the first day of the month
    date = datetime(year, month, 1).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    params = {
        "start_date": date
    }

    API_URL = f"https://www.recreation.gov/api/camps/availability/campground/{campground_id}/month?{urlencode(params)}"

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(API_URL, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results = []
            
            # Iterate over each campsite
            for campsite in data["campsites"].values():
                # Extract the required fields
                campsite_id = campsite["campsite_id"]
                site = campsite["site"]
                quantities = campsite["quantities"]
                result = {
                    "campsite_id": campsite_id,
                    "site": site,
                    "quantities": quantities
                }
                results.append(result)
            
            return results
        elif response.status_code == 400:
            print(f"Invalid request for campground {campground_id} (month {month}/{year}). Check if campground ID is valid.")
            return None
        elif response.status_code == 404:
            print(f"Campground {campground_id} not found.")
            return None
        else:
            print(f"Failed to get data for campground {campground_id}. Status code: {response.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching data for campground {campground_id}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching data for campground {campground_id}: {e}")
        return None