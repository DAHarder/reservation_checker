# Campground Availability Checker (WIP)

This project is a Python application that checks the availability of specific campsites on certain dates using data from the Recreation.gov API.

## Project Structure

The project is divided into several modules:

- `main.py`: The entry point of the application.
- `utils/api_utils.py`: Contains the `fetch_campground_data` function, which fetches data from the API.
- `services/availability_service.py`: Contains the `check_availability` function, which reads the settings from a YAML file and checks the availability of the specified campsites.

## How to Run the Application

1. Install the required Python packages:

    ```bash
    pip install requests.txt
    ```

2. Run the main script:

    ```bash
    python main.py
    ```

## Configuration

The application's settings are defined in the `config/settings.yaml` file. 

This file should contain a list of campgrounds, each with an id, a list of site numbers, and a list of dates. The application will check the availability of each site on each date.

Here's an example of what the settings file might look like:

```yaml
campgrounds:
- id: 233870
  sites: 
  - "002"
  - "004"
  dates: 
  - "2024-01-01T00:00:00Z"
  - "2024-01-02T00:00:00Z"
