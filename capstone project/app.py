import os
import re
import json
import sqlite3
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Paths
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "sentiment_model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "tfidf_vectorizer.pkl")
EVAL_PATH = os.path.join(MODEL_DIR, "evaluation.json")
DB_PATH = "predictions.db"

# Load ML Model and TF-IDF Vectorizer
model = None
vectorizer = None

def load_ml_components():
    global model, vectorizer
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        try:
            model = joblib.load(MODEL_PATH)
            vectorizer = joblib.load(VECTORIZER_PATH)
            print("Model and Vectorizer loaded successfully.")
        except Exception as e:
            print(f"Error loading model/vectorizer: {e}")
    else:
        print("Warning: Model or Vectorizer files not found. Run train_model.py first.")

# Initial load
load_ml_components()

# NLTK Stopwords fallback logic
import nltk
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    STOPWORDS = set(stopwords.words('english'))
    USE_NLTK = True
except Exception as e:
    print(f"NLTK failed to initialize in Flask app ({e}). Using manual fallback.")
    USE_NLTK = False
    STOPWORDS = set([
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", 
        "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", 
        "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", 
        "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", 
        "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", 
        "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", 
        "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", 
        "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", 
        "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", 
        "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", 
        "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", 
        "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
    ])

def preprocess_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'<[^>]*>', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    if USE_NLTK:
        try:
            tokens = word_tokenize(text)
        except Exception:
            tokens = text.split()
    else:
        tokens = text.split()
    cleaned_tokens = [token for token in tokens if token not in STOPWORDS and len(token) > 1]
    return " ".join(cleaned_tokens)

# Retrieve unique product list from dataset
def get_products():
    try:
        df = pd.read_csv("dataset/reviews.csv")
        return sorted(df["Product"].unique().tolist())
    except Exception as e:
        print(f"Error reading products from dataset: {e}")
        return ["Wireless Headphones", "Smart Watch", "Air Fryer", "Running Shoes", 
                "Ergonomic Office Chair", "Electric Toothbrush", "Bluetooth Speaker", 
                "Espresso Machine", "Robot Vacuum", "Laptop Stand"]

# SQLite Database Initialization
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Schema check for updates
    cursor.execute("PRAGMA table_info(predictions)")
    columns = [info[1] for info in cursor.fetchall()]
    if columns and "product" not in columns:
        print("Schema out of date. Dropping old predictions table.")
        cursor.execute("DROP TABLE predictions")
        
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product TEXT NOT NULL,
            review_text TEXT NOT NULL,
            predicted_sentiment TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Helper function to query DB
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    global model, vectorizer
    if request.method == "POST":
        if model is None or vectorizer is None:
            load_ml_components()
            if model is None or vectorizer is None:
                return jsonify({"error": "Machine learning model files not found on server. Train the model first."}), 500
        
        data = request.get_json()
        if not data or "review" not in data or "product" not in data:
            return jsonify({"error": "Missing review text or product selection."}), 400
            
        review_text = data["review"].strip()
        product = data["product"].strip()
        
        if not review_text:
            return jsonify({"error": "Review text cannot be empty."}), 400
        if not product:
            return jsonify({"error": "Product selection cannot be empty."}), 400
            
        # 1. Preprocess review text
        cleaned_text = preprocess_text(review_text)
        if not cleaned_text.strip():
            cleaned_text = review_text.lower()
            
        # 2. Vectorize using TF-IDF
        features = vectorizer.transform([cleaned_text])
        
        # 3. Model Prediction
        prediction = model.predict(features)[0]
        
        # 4. Get confidence (probability)
        probabilities = model.predict_proba(features)[0]
        class_idx = np.where(model.classes_ == prediction)[0][0]
        confidence = float(probabilities[class_idx])
        
        # 5. Log prediction to SQLite database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO predictions (product, review_text, predicted_sentiment, confidence) VALUES (?, ?, ?, ?)",
                (product, review_text, prediction, confidence)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database logging error: {e}")
            
        return jsonify({
            "product": product,
            "review": review_text,
            "sentiment": prediction,
            "confidence": round(confidence * 100, 2)
        })
        
    # GET Request: Fetch history and render template
    predictions_history = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT product, review_text, predicted_sentiment, confidence, timestamp FROM predictions ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        for row in rows:
            predictions_history.append({
                "product": row["product"],
                "review_text": row["review_text"],
                "predicted_sentiment": row["predicted_sentiment"],
                "confidence": round(row["confidence"] * 100, 2),
                "timestamp": row["timestamp"]
            })
        conn.close()
    except Exception as e:
        print(f"Error fetching history: {e}")
        
    return render_template("predict.html", history=predictions_history, products=get_products())

@app.route("/product_analysis")
def product_analysis():
    products = get_products()
    selected_product = request.args.get("product", products[0] if products else "")
    
    stats = {}
    negative_reviews = []
    complaint_keywords = []
    
    try:
        df = pd.read_csv("dataset/reviews.csv")
        prod_df = df[df["Product"] == selected_product]
        
        if not prod_df.empty:
            total_reviews = len(prod_df)
            avg_rating = round(float(prod_df["Rating"].mean()), 2)
            
            # Sentiment distribution
            sent_counts = prod_df["Sentiment"].value_counts().to_dict()
            pos_count = sent_counts.get("Positive", 0)
            neu_count = sent_counts.get("Neutral", 0)
            neg_count = sent_counts.get("Negative", 0)
            
            pos_pct = round((pos_count / total_reviews) * 100, 1) if total_reviews > 0 else 0.0
            neu_pct = round((neu_count / total_reviews) * 100, 1) if total_reviews > 0 else 0.0
            neg_pct = round((neg_count / total_reviews) * 100, 1) if total_reviews > 0 else 0.0
            
            # Rating distribution (1 to 5 stars)
            rating_counts = prod_df["Rating"].value_counts().to_dict()
            ratings_dist = [rating_counts.get(r, 0) for r in [1, 2, 3, 4, 5]]
            
            # List of negative reviews
            neg_reviews_df = prod_df[prod_df["Sentiment"] == "Negative"]
            negative_reviews = neg_reviews_df[["Review_Text", "Rating"]].to_dict(orient="records")
            
            # Extract common complaints keywords from negative reviews
            neg_texts = " ".join(neg_reviews_df["Review_Text"].astype(str).tolist())
            cleaned_neg_text = preprocess_text(neg_texts)
            words = cleaned_neg_text.split()
            
            # Filter out product names and noise terms
            exclude_words = set([
                "product", "bought", "got", "would", "one", "get", "like", "use",
                "arrived", "received", "purchase", "day", "week", "first",
                "completely", "after", "even", "recommend", "avoid", "terrible", "worst",
                "flimsy", "bad"
            ] + [selected_product.lower()] + [w.lower() for w in selected_product.split()])
            
            filtered_words = [w for w in words if w not in exclude_words and len(w) > 2]
            
            from collections import Counter
            word_counts = Counter(filtered_words)
            complaint_keywords = [{"word": w, "count": c} for w, c in word_counts.most_common(8)]
            
            stats = {
                "product_name": selected_product,
                "total_reviews": total_reviews,
                "avg_rating": avg_rating,
                "pos_count": pos_count,
                "pos_pct": pos_pct,
                "neu_count": neu_count,
                "neu_pct": neu_pct,
                "neg_count": neg_count,
                "neg_pct": neg_pct,
                "ratings_dist": ratings_dist
            }
    except Exception as e:
        print(f"Error computing product stats: {e}")
        
    return render_template(
        "product_analysis.html",
        products=products,
        selected_product=selected_product,
        stats=stats,
        negative_reviews=negative_reviews,
        complaint_keywords=complaint_keywords
    )

@app.route("/dashboard")
def dashboard():
    eval_metrics = {}
    if os.path.exists(EVAL_PATH):
        try:
            with open(EVAL_PATH, "r") as f:
                eval_metrics = json.load(f)
        except Exception as e:
            print(f"Error loading evaluation metrics: {e}")
            
    db_stats = {
        "user_predictions_count": 0,
        "pos_count": 0,
        "neu_count": 0,
        "neg_count": 0
    }
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM predictions")
        db_stats["user_predictions_count"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT predicted_sentiment, COUNT(*) FROM predictions GROUP BY predicted_sentiment")
        sentiment_counts = cursor.fetchall()
        for row in sentiment_counts:
            sentiment = row[0]
            count = row[1]
            if sentiment == "Positive":
                db_stats["pos_count"] = count
            elif sentiment == "Neutral":
                db_stats["neu_count"] = count
            elif sentiment == "Negative":
                db_stats["neg_count"] = count
                
        conn.close()
    except Exception as e:
        print(f"Error compiling DB statistics: {e}")
        
    return render_template("dashboard.html", evaluation=eval_metrics, db_stats=db_stats)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/clear_history", methods=["POST"])
def clear_history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions")
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Prediction history cleared."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
