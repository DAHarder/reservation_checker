# main.py - This is the entry point of your application. It calls functions from other modules to execute the program.

import services.availability_service as availability_service
import utils.api_utils as api_utils

def main():
    # Call the check_availability function from availability_service
    # availability_service.check_availability()

    print(api_utils.fetch_campground_data("233870", 1, 2024))

if __name__ == "__main__":
    main()