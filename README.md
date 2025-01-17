
# 🧾 SpendSense

**SpendSense** is a Flask-powered application that helps you analyze and categorize receipt data into meaningful expense categories. Leveraging AI for receipt classification and offering real-time insights, SpendSense is your ultimate personal finance assistant.

---

## 🌟 Features

- **Receipt Classification**: Upload receipt images to classify items into categories like Produce, Dairy, Snacks, and more.
- **Expense Summaries**: Automatically calculate category-wise totals for each receipt.
- **Dashboard**: View your categorized expenses over the past 30 days.
- **AI Integration**: Uses NVIDIA's cutting-edge AI API for accurate classification.
- **Secure Backend**: Developed using Flask with robust logging and error handling.

---

## 🛠️ Technologies Used

- **Backend**: Flask, Flask-SQLAlchemy
- **Frontend**: React.js
- **Database**: SQLite (can be switched to other relational databases)
- **AI Integration**: NVIDIA API
- **Other Tools**: Requests, Certifi, Logging, Base64 Encoding

---

## 🚀 Getting Started

Follow these steps to set up SpendSense locally.

### Prerequisites

1. **Python 3.12+**
2. **Node.js** (for React frontend)
3. **Pipenv** (or any Python virtual environment tool)
4. **Docker** (optional, for containerized deployment)

---

### Backend Setup (Flask)

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/SpendSense.git
   cd SpendSense/flask-backend
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Mac/Linux
   venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your NVIDIA API Key to the environment:
   ```bash
   export NVIDIA_API_KEY="your-api-key-here"
   ```

5. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the Flask app:
   ```bash
   flask run
   ```
   The app will be available at `http://127.0.0.1:5000`.

---

### Frontend Setup (React)

1. Navigate to the React app:
   ```bash
   cd ../react-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   The frontend will run at `http://localhost:3000`.

---

## 🖼️ Application Workflow

1. **Upload Receipt**:
   Upload your receipt image via the web interface.
   
2. **Classification**:
   The app uses the NVIDIA API to classify items into categories.

3. **Expense Tracking**:
   Categorized expenses are stored in a database and visualized in the dashboard.

4. **Dashboard Insights**:
   View and analyze your spending habits over the last 30 days.

---

## 📂 Project Structure

```plaintext
SpendSense/
├── flask-backend/
│   ├── app.py                # Main Flask application
│   ├── config.py             # App configurations
│   ├── models.py             # Database models
│   ├── utils.py              # Helper functions
│   ├── requirements.txt      # Backend dependencies
│   └── templates/            # HTML templates (if any)
├── react-frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── App.js            # Main App component
│   │   └── index.js          # Entry point
│   ├── public/
│   ├── package.json          # Frontend dependencies
│   └── README.md             # Frontend README
└── README.md                 # Project README
```

---

## 📊 Expense Categories

SpendSense supports the following categories for classification:

1. **Produce**: Fruits, vegetables, fresh herbs.
2. **Dairy**: Milk, cheese, yogurt, butter.
3. **Meat & Seafood**: Chicken, beef, fish, shrimp.
4. **Pantry Staples**: Rice, pasta, flour, sugar, spices.
5. **Snacks**: Chips, nuts, chocolates.
6. **Beverages**: Coffee, tea, juices, soft drinks.
7. **Frozen Items**: Ice cream, frozen meals, vegetables.
8. **Bakery**: Bread, rolls, pastries.
9. **Household Supplies**: Cleaning products, paper towels.
10. **Personal Care**: Shampoo, soap, toothpaste.
11. **Other**: Miscellaneous items like pet food, specialty goods.

---

## 🔧 Debugging Common Issues

- **SSL Errors**:
  Ensure your Python environment uses the latest `certifi` certificates:
  ```bash
  pip install --upgrade certifi
  ```

- **API Key Errors**:
  Double-check your NVIDIA API key is set correctly in `config.py`.

- **Database Errors**:
  Run the following commands to reset the database:
  ```bash
  flask db downgrade
  flask db upgrade
  ```

---

## 🎉 Contributions

We welcome contributions! Here's how you can help:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m "Add a meaningful message"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Create a Pull Request.

---


## 📧 Contact

If you have any questions or feedback, feel free to reach out:

- **Author**: Jeevan Bhatta
- **Email**: jeevan@uni.minerva.edu

Happy Tracking! 🚀
```