import json
import logging

logger = logging.getLogger(__name__)

def parse_categorization(data):
    results = {'items': {}, 'totals': {}}
    if not data:
        logger.error("Empty data received for categorization")
        return results

    try:
        # Ensure we are decoding JSON only
        results = json.loads(data.strip())
        if 'items' not in results or 'totals' not in results:
            raise ValueError("Invalid JSON format: Missing keys 'items' or 'totals'")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in parsing categorization: {e}")
    return results