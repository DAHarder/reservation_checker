import calendar
from datetime import datetime, timedelta

def get_fridays_and_saturdays(year, from_date=None):
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
        return None
    
    months = [5, 6, 7, 8, 9]  # May, June, July, August, and September
    days = []

    for month in months:
        # Skip months that are in the past
        if from_date.year == year and month < from_date.month:
            continue
            
        # Find out the number of days in the month
        _, num_days = calendar.monthrange(year, month)

        for day in range(1, num_days + 1):
            date = datetime(year, month, day)
            # Check if the day is Friday or Saturday (weekday() function returns 4 for Friday and 5 for Saturday)
            if date.weekday() in [4, 5]:
                # Only include dates that are today or in the future
                if date.date() >= from_date:
                    days.append(date.strftime("%Y-%m-%d"))

    return days

def get_future_fridays_and_saturdays(year):
    """
    Get Fridays and Saturdays from today through the end of September for the given year.
    
    Args:
        year (int): The year to check
    
    Returns:
        list: List of date strings in YYYY-MM-DD format
        None: If it's past September in the selected year
    """
    return get_fridays_and_saturdays(year)