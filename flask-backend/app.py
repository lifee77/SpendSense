from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from models import db, Expense
from utils import parse_categorization
import requests
import base64
import logging
import certifi
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
from datetime import datetime, timedelta
import json

# Set up SSL certificates
os.environ['SSL_CERT_FILE'] = certifi.where()

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)
app.config['DEBUG'] = True

# Initialize database tables
with app.app_context():
    db.create_all()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Helper function for a session with retries
def create_requests_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=5,  # Total retries
        backoff_factor=1,  # Exponential backoff (1s, 2s, 4s, etc.)
        status_forcelist=[429, 500, 502, 503, 504],  # Retry on these HTTP codes
        allowed_methods=["POST"]  # Retry only on POST requests
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.verify = certifi.where()  # Use certifi for SSL
    return session

@app.route('/')
def welcome():
    return 'Welcome to the SpendSense Flask application! Visit /classify to classify a receipt or /dashboard to view the dashboard in the frontend.'

@app.route('/classify', methods=['POST'])
def classify_receipt():
    try:
        # Validate receipt_image in the request
        receipt_image = request.files.get('receipt_image')
        if not receipt_image:
            logger.error("No receipt image uploaded")
            return jsonify({'error': 'No receipt image uploaded'}), 400

        # Encode image to Base64
        image_b64 = base64.b64encode(receipt_image.read()).decode()


        # Prepare NVIDIA API payload
        payload = {
            "model": 'meta/llama-3.2-11b-vision-instruct',
            "messages": [
                {
                    "role": "user",
                    "content": f"""
Classify all items in this receipt into strictly these categories:
- Produce: Fruits, vegetables, fresh herbs.
- Dairy: Milk, cheese, yogurt, butter.
- Meat & Seafood: Chicken, beef, fish, shrimp.
- Pantry Staples: Rice, pasta, flour, sugar, spices.
- Snacks: Chips, nuts, chocolates.
- Beverages: Coffee, tea, juices, soft drinks.
- Frozen Items: Ice cream, frozen meals, frozen vegetables.
- Bakery: Bread, rolls, pastries.
- Household Supplies: Cleaning products, paper towels, detergents.
- Personal Care: Shampoo, soap, toothpaste.
- Electronics & Appliances: Phones, chargers, small appliances, batteries.
- Clothing & Accessories: Shirts, shoes, belts, hats.
- Furniture & Home Decor: Chairs, tables, lamps, curtains.
- Toys & Games: Children's toys, board games, video games.
- Books & Stationery: Books, notebooks, pens, markers.
- Pet Supplies: Pet food, toys, grooming products.
- Pharmacy & Health: Medicines, vitamins, first-aid items.
- Automotive: Car maintenance supplies, oil, wipers.
- Garden & Outdoor: Plants, seeds, garden tools.
- Sporting Goods: Sports equipment, workout gear, bikes.
- Entertainment: DVDs, music, streaming gift cards.
- Office Supplies: Printers, paper, office chairs.
- Gifts & Party Supplies: Wrapping paper, greeting cards, balloons.
- Luxury Items: Jewelry, watches, designer products.
- Transportation: Bus/train passes, parking fees, tolls.
- Other: Miscellaneous items not listed above.

Return the output **strictly as a JSON object** in this format:

{{
  "items": {{
    "Produce": [
      {{"description": "Banana", "amount": 1.50}},
      {{"description": "Apples", "amount": 2.00}}
    ],
    "Dairy": [
      {{"description": "Milk", "amount": 3.50}}
    ]
  }},
  "totals": {{
    "Produce": 3.50,
    "Dairy": 3.50
  }},
  "date": "YYYY-MM-DD"
}}

Do not include any additional text or explanations either at the beginning or at the end. Only return the JSON object. <img src=\"data:image/png;base64,{image_b64}\" />
"""
                }
            ],
            "max_tokens": 512,
            "temperature": 1.00,
            "top_p": 1.00
        }

        # Send request to NVIDIA API
        headers = {
            "Authorization": f"Bearer {Config.NVIDIA_API_KEY}",
            "Accept": "application/json"
        }
        session = create_requests_session()
        response = session.post(Config.NVIDIA_API_URL, headers=headers, json=payload, timeout=120)

        if response.status_code != 200:
            logger.error(f"Failed to classify receipt: {response.status_code}, {response.text}")
            return jsonify({'error': 'Failed to classify receipt', 'details': response.text}), response.status_code

        # Parse API response
        api_result = response.json()
        categorized_expenses_raw = api_result.get('choices', [{}])[0].get('message', {}).get('content', '')

        if not categorized_expenses_raw:
            logger.error("Received empty response from NVIDIA API")
            return jsonify({'error': 'Received empty response from NVIDIA API'}), 500

        # Debug raw data
        logger.info(f"Categorized Expenses Raw Data: {categorized_expenses_raw}")

        # Extract JSON part from the response
        try:
            json_start = categorized_expenses_raw.index("{")
            json_end = categorized_expenses_raw.rindex("}") + 1
            categorized_expenses = categorized_expenses_raw[json_start:json_end]
            results = json.loads(categorized_expenses)
        except (ValueError, json.JSONDecodeError) as e:
            logger.error(f"Failed to extract or decode JSON: {e}")
            return jsonify({'error': 'Failed to process the NVIDIA API response'}), 500

        # Store results in the database
        today = datetime.utcnow()
        for category, items in results['items'].items():
            for item in items:
                db.session.add(
                    Expense(
                        description=item.get('description', 'Unknown item'),
                        category=category,
                        amount=item.get('amount', 0.0),
                        date=today
                    )
                )
        db.session.commit()

        return jsonify({'message': 'Receipt classified and stored successfully', 'summary': results['totals']})

    except requests.exceptions.SSLError as e:
        logger.error(f"SSL Error: {e}")
        return jsonify({'error': 'SSL error occurred'}), 500
    except requests.exceptions.RequestException as e:
        logger.error(f"Request Error: {e}")
        return jsonify({'error': 'Request failed'}), 500
    except Exception as e:
        logger.exception("An error occurred while processing the receipt")
        return jsonify({'error': 'An internal error occurred'}), 500

@app.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        # Filter expenses from the last 30 days
        today = datetime.utcnow()
        thirty_days_ago = today - timedelta(days=30)
        expenses = Expense.query.filter(Expense.date >= thirty_days_ago).all()

        # Aggregate category-wise totals
        summary = {}
        for expense in expenses:
            summary[expense.category] = summary.get(expense.category, 0) + expense.amount

        return jsonify(summary)
    except Exception as e:
        logger.exception("An error occurred while fetching the dashboard")
        return jsonify({'error': 'Failed to fetch dashboard data'}), 500

if __name__ == '__main__':
    app.run(debug=True)