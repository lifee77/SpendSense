from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import db, Expense
from utils import parse_categorization
import requests
import base64

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# NVIDIA API Configuration
NVIDIA_API_URL = "https://ai.api.nvidia.com/v1/gr/meta/llama-3.2-11b-vision-instruct/chat/completions"

@app.route('/')
def welcome():
    return 'Welcome to the SpendSense Flask application!'


@app.route('/classify', methods=['POST'])
def classify_receipt():
    receipt_image = request.files.get('receipt_image')
    if not receipt_image:
        return jsonify({'error': 'No receipt image uploaded'}), 400

    # Encode image to Base64
    image_b64 = base64.b64encode(receipt_image.read()).decode()
    if len(image_b64) > 180_000:
        return jsonify({'error': 'Image size too large'}), 400

    # Call NVIDIA API
    payload = {
        "model": 'meta/llama-3.2-11b-vision-instruct',
        "messages": [
            {
                "role": "user",
                "content": f'''
Classify all items in this receipt into categories:

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

Here is the image: <img src="data:image/png;base64,{image_b64}" />
                '''
            }
        ],
        "max_tokens": 512,
        "temperature": 1.00,
        "top_p": 1.00
    }

    headers = {
        "Authorization": f"Bearer {Config.NVIDIA_API_KEY}",
        "Accept": "application/json"
    }
    response = requests.post(NVIDIA_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to classify receipt', 'details': response.json()}), 500

    # Parse response
    api_result = response.json()
    categorized_expenses = api_result.get('choices', [{}])[0].get('message', {}).get('content', '')

    # Extract categorized items and totals
    results = parse_categorization(categorized_expenses)

    # Store results in the database
    for category, items in results['items'].items():
        for item in items:
            db.session.add(Expense(description=item['description'], category=category, amount=item['amount']))
    db.session.commit()

    return jsonify({'message': 'Receipt classified and stored successfully', 'summary': results['totals']})


@app.route('/dashboard', methods=['GET'])
def dashboard():
    expenses = Expense.query.all()
    summary = {}
    for expense in expenses:
        summary[expense.category] = summary.get(expense.category, 0) + expense.amount
    return jsonify(summary)


if __name__ == '__main__':
    app.run(debug=True)
