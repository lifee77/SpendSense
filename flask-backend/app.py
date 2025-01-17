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

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
db.init_app(app)

# Initialize database tables
with app.app_context():
    db.create_all()

# NVIDIA API Configuration
NVIDIA_API_URL = "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-11b-vision-instruct/chat/completions"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def welcome():
    return 'Welcome to the SpendSense Flask application!'

from datetime import datetime, timedelta

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
                    "content": f'''
Classify all items in this receipt into strictly these categories:

Produce: Fruits, vegetables, fresh herbs.
Dairy: Milk, cheese, yogurt, butter.
Meat & Seafood: Chicken, beef, fish, shrimp.
Pantry Staples: Rice, pasta, flour, sugar, spices.
Snacks: Chips, nuts, chocolates.
Beverages: Coffee, tea, juices, soft drinks.
Frozen Items: Ice cream, frozen meals, frozen vegetables.
Bakery: Bread, rolls, pastries.
Household Supplies: Cleaning products, paper towels, detergents.
Personal Care: Shampoo, soap, toothpaste.
Other: Miscellaneous items (pet food, specialty items).

Also, sum up expenses in each category.
Write the date in the format YYYY-MM-DD.
Here is the image: <img src="data:image/png;base64,{image_b64}" />
                    '''
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
        response = requests.post(NVIDIA_API_URL, headers=headers, json=payload, verify=False, timeout=120)

        # Retry mechanism
        retry_count = 3
        while response.status_code != 200 and retry_count > 0:
            logger.warning("Retrying NVIDIA API request...")
            response = requests.post(NVIDIA_API_URL, headers=headers, json=payload)
            retry_count -= 1

        if response.status_code != 200:
            logger.error("Failed to classify receipt")
            return jsonify({'error': 'Failed to classify receipt', 'details': response.json()}), 500

        # Parse API response
        api_result = response.json()
        categorized_expenses = api_result.get('choices', [{}])[0].get('message', {}).get('content', '')

        # Extract categorized items and totals
        results = parse_categorization(categorized_expenses)

        # Store results in the database
        today = datetime.utcnow()
        for category, items in results['items'].items():
            for item in items:
                db.session.add(
                    Expense(
                        description=item['description'],
                        category=category,
                        amount=item['amount'],
                        date=today
                    )
                )
        db.session.commit()

        return jsonify({'message': 'Receipt classified and stored successfully', 'summary': results['totals']})

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