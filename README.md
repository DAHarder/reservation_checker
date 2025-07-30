# Campground Availability Checker

A Python tool that checks campsite availability on weekends (Fridays and Saturdays) for all months until end of September using the Recreation.gov API.

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create your configuration:
   ```bash
   cp src/config/settings.yaml.template src/config/settings.yaml
   ```

3. Edit `src/config/settings.yaml` with your desired campgrounds and sites

4. Run the checker:
   ```bash
   python src/main.py
   ```

## Configuration

Create `src/config/settings.yaml` with your campground details:

```yaml
campgrounds:
- id: 232868
  sites: 
  - '008'
  - '016'
  - '041'
```

## Flag Options

- `--config PATH` - Use a different config file
