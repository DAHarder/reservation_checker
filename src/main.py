# main.py - This is the entry point of your application. It calls functions from other modules to execute the program.

import argparse
import services.availability_service as availability_service
import utils.api_utils as api_utils
import utils.get_dates as get_dates
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Check campground availability for weekends')
    parser.add_argument('--year', type=int, default=datetime.now().year,
                       help='Year to check availability for (default: current year)')
    parser.add_argument('--config', type=str, default='src/config/settings.yaml',
                       help='Path to configuration file (default: src/config/settings.yaml)')
    
    args = parser.parse_args()
    
    # Call the check_availability function from availability_service
    availability_service.check_availability(args.year, args.config)

if __name__ == "__main__":
    main()