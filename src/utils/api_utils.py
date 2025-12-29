"""API utilities for interacting with recreation.gov."""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlencode

import requests

# Constants
RECREATION_GOV_API_BASE = "https://www.recreation.gov/api/camps"
API_TIMEOUT = 30
USER_AGENT = "Mozilla/5.0"

# Cache for campground names to avoid repeated API calls
_campground_name_cache: Dict[str, str] = {}

logger = logging.getLogger("reservation_checker")

def fetch_campground_name(campground_id: str) -> str:
    """Fetch the campground name from recreation.gov API with caching.
    
    Args:
        campground_id: The campground ID to fetch the name for
        
    Returns:
        The campground name or a fallback string if not found
    """
    # Check cache first
    if campground_id in _campground_name_cache:
        logger.debug(f"Using cached name for campground {campground_id}")
        return _campground_name_cache[campground_id]
    
    api_url = f"{RECREATION_GOV_API_BASE}/campgrounds/{campground_id}"
    headers = {"User-Agent": USER_AGENT}

    try:
        response = requests.get(api_url, headers=headers, timeout=API_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            name = data["campground"]["facility_name"]
            # Cache the result
            _campground_name_cache[campground_id] = name
            logger.debug(f"Fetched name for campground {campground_id}: {name}")
            return name
        elif response.status_code == 404:
            name = f"Campground {campground_id} (name not found)"
            logger.warning(f"Campground {campground_id} not found (404)")
            _campground_name_cache[campground_id] = name
            return name
        else:
            name = f"Campground {campground_id} (error fetching name)"
            logger.error(f"Error fetching name for {campground_id}: status {response.status_code}")
            _campground_name_cache[campground_id] = name
            return name
            
    except requests.exceptions.RequestException as e:
        name = f"Campground {campground_id} (network error)"
        logger.error(f"Network error fetching name for {campground_id}: {e}")
        _campground_name_cache[campground_id] = name
        return name
    except Exception as e:
        name = f"Campground {campground_id} (unexpected error)"
        logger.error(f"Unexpected error fetching name for {campground_id}: {e}")
        _campground_name_cache[campground_id] = name
        return name

def fetch_campground_data(campground_id: str, month: int, year: int) -> Optional[List[Dict]]:
    """Fetch availability data for a campground for a specific month.
    
    Args:
        campground_id: The campground ID
        month: Month number (1-12)
        year: Year (e.g., 2025)
        
    Returns:
        List of availability data dictionaries, or None if request fails
    """
    # Format the date to the first day of the month
    date = datetime(year, month, 1).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    params = {"start_date": date}

    api_url = f"{RECREATION_GOV_API_BASE}/availability/campground/{campground_id}/month?{urlencode(params)}"
    headers = {"User-Agent": USER_AGENT}

    logger.debug(f"Fetching data for campground {campground_id}, month {month}/{year}")
    
    try:
        response = requests.get(api_url, headers=headers, timeout=API_TIMEOUT)
        
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
            
            logger.debug(f"Successfully fetched {len(results)} campsites for {campground_id}")
            return results
        elif response.status_code == 400:
            error_msg = f"Invalid request for campground {campground_id} (month {month}/{year}). Check if campground ID is valid."
            logger.error(error_msg)
            print(error_msg)
            return None
        elif response.status_code == 404:
            error_msg = f"Campground {campground_id} not found."
            logger.error(error_msg)
            print(error_msg)
            return None
        else:
            error_msg = f"Failed to get data for campground {campground_id}. Status code: {response.status_code}"
            logger.error(error_msg)
            print(error_msg)
            return None
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error fetching data for campground {campground_id}: {e}"
        logger.error(error_msg)
        print(error_msg)
        return None
    except Exception as e:
        error_msg = f"Unexpected error fetching data for campground {campground_id}: {e}"
        logger.error(error_msg, exc_info=True)
        print(error_msg)
        return None