# main.py - This is the entry point of your application. It calls functions from other modules to execute the program.

import services.availability_service as availability_service
import utils.api_utils as api_utils
import utils.get_dates as get_dates

def main():
    # Call the check_availability function from availability_service
    # availability_service.check_availability()

    # print(api_utils.fetch_campground_data("233870", 1, 2024))
    # print(get_dates.get_fridays_and_saturdays(2024))
    availability_service.check_availability(2024)

if __name__ == "__main__":
    main()