# services/availability_service.py - This module contains business logic. In your case, it could contain a function that reads the data from settings.yaml and uses fetch_campground_data to check whether specific camp/site/date combinations are available.

import yaml
import utils.api_utils as api_utils
from datetime import datetime

def check_availability():
    with open('config/settings.yaml', 'r') as file:
        settings = yaml.safe_load(file)

    for campground in settings['campgrounds']:
        campground_id = campground['id']
        for date in campground['dates']:
            # Extract month and year from date
            date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000Z")
            month = date_obj.month
            year = date_obj.year

            # Fetch data
            results = api_utils.fetch_campground_data(campground_id, month, year)
            if results:
                for result in results:
                    if result['site'] in campground['sites']:
                        if result['quantities'].get(date) == 1:
                            print(f"Campsite {result['site']} is available on {date}")