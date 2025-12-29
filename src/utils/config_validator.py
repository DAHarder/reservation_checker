"""Configuration validation utilities."""

import logging
from typing import Any, Dict

logger = logging.getLogger("reservation_checker")


def validate_settings(settings: Dict[str, Any]) -> bool:
    """Validate the settings configuration.
    
    Args:
        settings: The settings dictionary to validate
        
    Returns:
        True if validation passes
        
    Raises:
        ValueError: If validation fails
    """
    if not settings:
        raise ValueError("Settings cannot be empty")
    
    if 'campgrounds' not in settings:
        raise ValueError("Settings must contain 'campgrounds' key")
    
    if not isinstance(settings['campgrounds'], list):
        raise ValueError("'campgrounds' must be a list")
    
    for i, campground in enumerate(settings['campgrounds']):
        if not isinstance(campground, dict):
            raise ValueError(f"Campground {i} must be a dictionary")
        
        if 'id' not in campground:
            raise ValueError(f"Campground {i} must have an 'id' field")
        
        if 'sites' not in campground:
            raise ValueError(f"Campground {i} must have a 'sites' field")
        
        if not isinstance(campground['sites'], list):
            raise ValueError(f"Campground {i} 'sites' must be a list")
        
        if not campground['sites']:
            raise ValueError(f"Campground {i} must have at least one site")
    
    logger.info(f"Configuration validation passed: {len(settings['campgrounds'])} campground(s)")
    return True
