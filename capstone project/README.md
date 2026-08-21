# Sentiment Analysis of Product Reviews

**Classifying customer reviews as Positive, Neutral, or Negative using NLP and Machine Learning**

This project is a complete, web-based Sentiment Analysis application. It features a Natural Language Processing (NLP) text cleaning pipeline, term vectorization using TF-IDF, and classification powered by a trained Naive Bayes algorithm. The front end is served by a Flask server with SQLite query logging and interactive Chart.js visualizations.

---

## Project Structure

```text
project/
│
├── app.py                     # Main Flask web server (routes, API, and SQLite database)
├── generate_dataset.py        # Utility script to generate the synthetic product review dataset
├── train_model.py             # Script to train, evaluate, and save the Naive Bayes classifier
├── requirements.txt           # File containing Python packages to install
├── README.md                  # Setup and execution instructions (this file)
│
├── dataset/
│   └── reviews.csv            # Preprocessed dataset of product reviews (created by generate_dataset.py)
│
├── model/
│   ├── sentiment_model.pkl    # Saved trained Naive Bayes classifier
│   ├── tfidf_vectorizer.pkl   # Saved trained TF-IDF vectorizer
│   └── evaluation.json        # Saved model evaluation metrics for the dashboard
│
├── notebooks/
│   └── model_training.ipynb   # Step-by-step Jupyter Notebook explaining training and evaluation
│
├── static/
│   ├── css/
│   │   └── style.css          # Styling tokens, responsive grid layouts, and cards
│   └── js/
│       └── script.js          # AJAX fetch submissions, DOM elements rendering, and Chart.js wrappers
│
└── templates/
    ├── base.html              # Core layout (header navbar, Bootstrap, Chart.js CDNs, footer)
    ├── index.html             # Home page (overview, purpose of sentiment analysis)
    ├── predict.html           # Prediction page (interactive text analyzer & history table)
    ├── product_analysis.html   # Product Analysis page (product-specific statistics & keywords)
    ├── dashboard.html         # Dashboard (dataset counts, user charts, and confusion matrix)
    └── about.html             # About page (pipeline steps, Naive Bayes formulas, tech stack details)
```

---

## Requirements & Prerequisites

* Python 3.8 or higher.
* The application runs locally and has been validated on **Windows** using the standard Python Launcher (`py`).

---

## Setup and Installation

### 1. Initialize Virtual Environment
Open a terminal in the project directory (`c:\Users\navan\Desktop\Sentiment_Analysis_Project`) and run:
```bash
py -m venv venv
```

### 2. Activate the Virtual Environment
* **On Windows (Command Prompt / VS Code Cmd terminal):**
  ```cmd
  venv\Scripts\activate
  ```
* **On Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

### 3. Install Dependencies
Ensure pip is upgraded and install requirements:
```bash
venv\Scripts\python -m pip install --upgrade pip
venv\Scripts\pip install -r requirements.txt
```

---

## Running the Project

Follow these steps in sequence:

### Step 1: Generate the Product Review Dataset
Create a dataset containing 480 balanced reviews across various categories with a dedicated `Product` column by running:
```bash
venv\Scripts\python generate_dataset.py
```
This writes the dataset to `dataset/reviews.csv`.

### Step 2: Train and Save the Model
Process the dataset, train the Naive Bayes model using TF-IDF features, and output evaluation metrics by running:
```bash
venv\Scripts\python train_model.py
```
This saves:
* `model/sentiment_model.pkl`
* `model/tfidf_vectorizer.pkl`
* `model/evaluation.json` (used to load stats on the web dashboard)

### Step 3: Run the Flask Web Application
Start the local server by running:
```bash
venv\Scripts\python app.py
```
Once initialized, open your web browser and navigate to:
```text
http://127.0.0.1:5000/
```

---

## Key Features

1. **Home**: Introduces the project scope, business significance of automated sentiment tracking, and NLP preprocessing details.
2. **Product Analysis**: Select products (e.g. Smart Watch, Running Shoes) from a dropdown to check total reviews, average ratings, positive/neutral/negative percentage splits, rating distribution charts, negative keywords/complaints, and raw negative reviews.
3. **Predict Sentiment**: Let users select a product category and write custom reviews. Clicking **Analyze Sentiment** submits an AJAX post request. The model yields predictions and confidence levels, logging results in a local SQLite database history table (`predictions.db`) mapping products to reviews.
4. **Dashboard**: Evaluates the model using test metrics (Accuracy, Precision, Recall, F1 Score) and visualizes the Confusion Matrix. Renders dynamic charts (Pie/Doughnut for dataset split, Bar Chart for active user query frequencies) via Chart.js.
5. **About**: Explores Bayes' theorem mathematics, NLP pipeline details (lowercasing, cleaning, tokenization, stopword removal), and the project technology stack.
