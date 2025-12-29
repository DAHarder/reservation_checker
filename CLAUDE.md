# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python tool that checks campsite availability on Recreation.gov for weekends (Fridays and Saturdays) during the camping season (May through September). The tool queries the Recreation.gov API for configured campgrounds and sites, displaying available dates with colored terminal output.

## Running the Application

```bash
# From the repository root
python src/main.py

# With custom config file
python src/main.py --config path/to/settings.yaml
```

## Setup and Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Create configuration
cp src/config/settings.yaml.template src/config/settings.yaml
# Edit settings.yaml with desired campground IDs and site numbers
```

## Configuration

Configuration is stored in `src/config/settings.yaml` (not version controlled). The template shows the expected format:

```yaml
campgrounds:
- id: 232868          # Recreation.gov campground ID
  sites:
  - '008'             # Site numbers as strings
  - '016'
  - '041'
```

## Architecture

The codebase follows a service-oriented structure:

- **main.py**: Entry point that handles CLI arguments and orchestrates the availability check
- **services/availability_service.py**: Core business logic that coordinates the checking process
  - Groups dates by month for efficient API usage
  - Iterates through configured campgrounds and sites
  - Displays results with colored terminal output (green=available, red=not found)
- **utils/api_utils.py**: Recreation.gov API wrapper
  - Fetches campground names (with caching to reduce API calls)
  - Fetches availability data by month
  - Handles all HTTP communication and error cases
- **utils/get_dates.py**: Date calculation utilities
  - Generates lists of Fridays/Saturdays in camping months (May-September)
  - Filters dates to only include today forward
  - Detects if camping season has passed
- **utils/config_validator.py**: Validates settings.yaml structure
- **utils/logger.py**: Logging setup (errors to console, all logs to daily file in `logs/`)

## Important Constants

- `CAMPING_MONTHS = [5, 6, 7, 8, 9]`: May through September
- `WEEKEND_DAYS = [4, 5]`: Friday and Saturday (Python weekday indices)
- API endpoint: `https://www.recreation.gov/api/camps`
- Logs are written to `logs/reservation_checker_YYYYMMDD.log`

## Key Behaviors

- The application always uses the current year automatically
- API responses include availability quantities as a dictionary keyed by ISO datetime strings (e.g., `"2025-05-16T00:00:00Z": 1`)
- Campground names are cached in-memory to reduce API calls
- If the current date is past September, the application exits with a message to run next year
- Results are displayed per-campground with Recreation.gov URLs for easy booking
