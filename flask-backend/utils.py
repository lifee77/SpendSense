def parse_categorization(api_response):
    lines = api_response.splitlines()
    items = {}
    totals = {}

    current_category = None
    for line in lines:
        if ':' in line and not line.strip().startswith('-'):
            current_category = line.split(':')[0].strip()
            items[current_category] = []
            continue

        if current_category and '*' in line:
            parts = line.split('=')
            description = parts[0].strip()
            amount = float(parts[1].strip())
            items[current_category].append({'description': description, 'amount': amount})
            totals[current_category] = totals.get(current_category, 0) + amount

    return {'items': items, 'totals': totals}
