# services/availability_service.py - This module contains business logic. In your case, it could contain a function that reads the data from settings.yaml and uses fetch_campground_data to check whether specific camp/site/date combinations are available.

import yaml
import utils.api_utils as api_utils
import utils.get_dates as get_dates
from datetime import datetime
from collections import defaultdict
import calendar
from termcolor import colored



def check_availability(year):
    with open('src/config/settings.yaml', 'r') as file:
        settings = yaml.safe_load(file)

    # Get all Fridays and Saturdays of June and July
    all_dates = get_dates.get_fridays_and_saturdays(year)

    for campground in settings['campgrounds']:
        campground_id = campground['id']

        print(f"Checking data for {campground}")

        # Group dates by month
        dates_by_month = defaultdict(list)
        for date in all_dates:
            # Extract month and year from date
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            dates_by_month[date_obj.month].append(date)

        # Fetch data for each month
        for month, dates in dates_by_month.items():
            results = api_utils.fetch_campground_data(campground_id, month, year)
            if results:
                for result in results:
                    if result['site'] in campground['sites']:
                        for date in dates:
                            if result['quantities'].get(date + "T00:00:00Z") == 1:
                                print(f"Campsite {result['site']} is available on {date}")
                                available = True
                            else:
                                available = False
            if available == False:
                print(colored(f"No campsites found for {calendar.month_name[month]}", 'red'))

