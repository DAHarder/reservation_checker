# utils/api_utils.py - This module contains functions related to the API.
#API info: 'https://www.recreation.gov/api/camps/availability/campground/233870/month?start_date=2024-01-01T00%3A00%3A00.000Z'

import requests
from datetime import datetime
from urllib.parse import urlencode

def fetch_campground_data(campground_id:str, month:int, year:int):
    # Format the date to the first day of the month
    date = datetime(year, month, 1).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    params = {
        "start_date": date
    }

    API_URL = f"https://www.recreation.gov/api/camps/availability/campground/{campground_id}/month?{urlencode(params)}"

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(API_URL, headers=headers)

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

    else:
        print(f"Failed to get data. Status code: {response.status_code}")
        return None