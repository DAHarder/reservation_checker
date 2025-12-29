"""Main entry point for the reservation checker application."""

import argparse
import logging
from datetime import datetime

import services.availability_service as availability_service
import utils.logger as logger_utils


def main() -> None:
    """Parse arguments and check campground availability."""
    # Setup logging
    logger = logger_utils.setup_logger()
    
    parser = argparse.ArgumentParser(description='Check campground availability for weekends')
    parser.add_argument('--config', type=str, default='config/settings.yaml',
                       help='Path to configuration file (default: config/settings.yaml)')
    
    args = parser.parse_args()
    
    # Use current year automatically
    current_year = datetime.now().year
    logger.info(f"Starting availability check for year {current_year}")
    
    # Call the check_availability function from availability_service
    availability_service.check_availability(current_year, args.config)

if __name__ == "__main__":
    main()