import calendar
from datetime import datetime, timedelta

def get_fridays_and_saturdays(year):
    months = [6, 7]  # June and July
    days = []

    for month in months:
        # Find out the number of days in the month
        _, num_days = calendar.monthrange(year, month)

        for day in range(1, num_days + 1):
            date = datetime(year, month, day)
            # Check if the day is Friday or Saturday (weekday() function returns 4 for Friday and 5 for Saturday)
            if date.weekday() in [4, 5]:
                days.append(date.strftime("%Y-%m-%d"))

    return days