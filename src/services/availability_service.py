# services/availability_service.py - This module contains business logic. In your case, it could contain a function that reads the data from settings.yaml and uses fetch_campground_data to check whether specific camp/site/date combinations are available.

import yaml
import utils.api_utils as api_utils
import utils.get_dates as get_dates
import utils.config_validator as config_validator
from datetime import datetime
from collections import defaultdict
import calendar
from termcolor import colored



def check_availability(year, config_path='src/config/settings.yaml'):
    try:
        with open(config_path, 'r') as file:
            settings = yaml.safe_load(file)
        
        # Validate configuration
        config_validator.validate_settings(settings)
        
    except FileNotFoundError:
        print(colored("Error: settings.yaml file not found. Please copy settings.yaml.template to settings.yaml and configure it.", 'red'))
        return
    except yaml.YAMLError as e:
        print(colored(f"Error reading settings.yaml: {e}", 'red'))
        return
    except ValueError as e:
        print(colored(f"Configuration error: {e}", 'red'))
        return

    # Get all Fridays and Saturdays from today through end of September
    all_dates = get_dates.get_future_fridays_and_saturdays(year)
    
    # Check if we're past the camping season (past September)
    if all_dates is None:
        print(colored(f"Error: It's past September in {year}. The camping season (May-September) has ended. Run this next year.", 'red'))
        return

    for campground in settings['campgrounds']:
        campground_id = campground['id']

        # Get campground name from ID using the API
        campground_name = api_utils.fetch_campground_name(campground_id)

        print(f"Checking data for {campground_name} (ID: {campground_id})")
        print(colored(f"https://www.recreation.gov/camping/campgrounds/{campground_id}", 'yellow'))

        # Group dates by month
        dates_by_month = defaultdict(list)
        for date in all_dates:
            # Extract month and year from date
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            dates_by_month[date_obj.month].append(date)

        # Fetch data for each month
        for month, dates in dates_by_month.items():
            month_has_availability = False
            results = api_utils.fetch_campground_data(campground_id, month, year)
            if results:
                for result in results:
                    if result['site'] in campground['sites']:
                        for date in dates:
                            if result['quantities'].get(date + "T00:00:00Z") == 1:
                                print(colored(f"✓ Campsite {result['site']} is available on {date}", 'green'))
                                month_has_availability = True
            
            if not month_has_availability:
                print(colored(f"✗ No campsites found for {calendar.month_name[month]}", 'red'))

