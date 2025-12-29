"""Utilities for getting camping dates."""

import calendar
import logging
from datetime import datetime, timedelta
from typing import List, Optional

# Constants
CAMPING_MONTHS = [5, 6, 7, 8, 9]  # May through September
WEEKEND_DAYS = [4, 5]  # Friday (4) and Saturday (5)

logger = logging.getLogger("reservation_checker")


def get_fridays_and_saturdays(year: int, from_date: Optional[datetime] = None) -> Optional[List[str]]:
    """
    Get all Fridays and Saturdays in May, June, July, August, and September for the given year.
    
    Args:
        year (int): The year to check
        from_date (datetime, optional): Only return dates on or after this date. 
                                      If None, uses today's date.
    
    Returns:
        list: List of date strings in YYYY-MM-DD format
        None: If it's past September in the selected year
    """
    if from_date is None:
        from_date = datetime.now().date()
    else:
        from_date = from_date.date() if isinstance(from_date, datetime) else from_date
    
    # Check if we're past September in the selected year
    if from_date.year == year and from_date.month > 9:
        logger.warning(f"Past camping season for year {year}")
        return None
    
    days = []

    for month in CAMPING_MONTHS:
        # Skip months that are in the past
        if from_date.year == year and month < from_date.month:
            continue
            
        # Find out the number of days in the month
        _, num_days = calendar.monthrange(year, month)

        for day in range(1, num_days + 1):
            date = datetime(year, month, day)
            # Check if the day is Friday or Saturday
            if date.weekday() in WEEKEND_DAYS:
                # Only include dates that are today or in the future
                if date.date() >= from_date:
                    days.append(date.strftime("%Y-%m-%d"))

    return days

def get_future_fridays_and_saturdays(year: int) -> Optional[List[str]]:
    """Get Fridays and Saturdays from today through the end of September.
    
    Args:
        year: The year to check
    
    Returns:
        List of date strings in YYYY-MM-DD format, or None if past season
    """
    dates = get_fridays_and_saturdays(year)
    if dates:
        logger.info(f"Found {len(dates)} weekend dates for year {year}")
    return dates