"""Business logic for checking campground availability."""

import calendar
import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional

import yaml
from termcolor import colored

import utils.api_utils as api_utils
import utils.config_validator as config_validator
import utils.get_dates as get_dates

# Constants
CAMPING_MONTHS = [5, 6, 7, 8, 9]  # May through September
WEEKEND_DAYS = [4, 5]  # Friday and Saturday

logger = logging.getLogger("reservation_checker")



def check_availability(year: int, config_path: str = 'config/settings.yaml') -> None:
    """Check campground availability for the specified year.
    
    Args:
        year: The year to check availability for
        config_path: Path to the settings YAML file
    """
    try:
        with open(config_path, 'r') as file:
            settings = yaml.safe_load(file)
        
        # Validate configuration
        config_validator.validate_settings(settings)
        logger.info(f"Configuration loaded from {config_path}")
        
    except FileNotFoundError:
        error_msg = "Error: settings.yaml file not found. Please copy settings.yaml.template to settings.yaml and configure it."
        logger.error(error_msg)
        print(colored(error_msg, 'red'))
        return
    except yaml.YAMLError as e:
        error_msg = f"Error reading settings.yaml: {e}"
        logger.error(error_msg)
        print(colored(error_msg, 'red'))
        return
    except ValueError as e:
        error_msg = f"Configuration error: {e}"
        logger.error(error_msg)
        print(colored(error_msg, 'red'))
        return

    # Get all Fridays and Saturdays from today through end of September
    all_dates = get_dates.get_future_fridays_and_saturdays(year)
    
    # Check if we're past the camping season (past September)
    if all_dates is None:
        error_msg = f"Error: It's past September in {year}. The camping season (May-September) has ended. Run this next year."
        logger.warning(error_msg)
        print(colored(error_msg, 'red'))
        return
    
    logger.info(f"Found {len(all_dates)} weekend dates to check")
    print("")
    for campground in settings['campgrounds']:
        campground_id = campground['id']
        logger.info(f"Checking campground ID: {campground_id}")

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
            month_has_nyr = False
            month_header_printed = False
            results = api_utils.fetch_campground_data(campground_id, month, year)
            if results:
                for result in results:
                    # Normalize site numbers for comparison (remove leading zeros)
                    result_site_normalized = result['site'].lstrip('0') or '0'
                    configured_sites_normalized = [site.lstrip('0') or '0' for site in campground['sites']]

                    if result_site_normalized in configured_sites_normalized:
                        for date in dates:
                            date_key = date + "T00:00:00Z"
                            availability_status = result['availabilities'].get(date_key)

                            # Only show as available if status is "Available"
                            # This filters out "NYR" (Not Yet Released), "Reserved", etc.
                            if availability_status == "Available":
                                # Print month header before first available site
                                if not month_header_printed:
                                    print(f"\n{calendar.month_name[month]}:")
                                    month_header_printed = True
                                msg = f"✓ Campsite {result['site']} is available on {date}"
                                logger.info(f"Available: {campground_id} - {result['site']} - {date}")
                                print(colored(msg, 'green'))
                                month_has_availability = True
                            elif availability_status == "NYR":
                                month_has_nyr = True

            if not month_has_availability:
                if month_has_nyr:
                    print(colored(f"✗ No campsites available for {calendar.month_name[month]} (some dates not yet released)", 'red'))
                else:
                    print(colored(f"✗ No campsites found for {calendar.month_name[month]}", 'red'))
        print("-" * 50)  # Separator for each campground
    
    logger.info("Availability check completed")
    print(colored("Availability check completed.", 'blue'))
    print("")