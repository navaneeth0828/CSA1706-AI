import os
import re
import json
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

# Try to download NLTK data; use fallbacks if offline or blocked
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
    print(f"NLTK download/loading failed ({e}). Using manual fallback list and regex.")
    USE_NLTK = False
    # Standard English stopwords fallback
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

def clean_text(text):
    """
    NLP Preprocessing Steps:
    1. Convert text to lowercase
    2. Remove punctuation and unnecessary characters (numbers, special symbols)
    3. Tokenize the text
    4. Remove stopwords
    """
    if not isinstance(text, str):
        return ""
    
    # 1. Convert to lowercase
    text = text.lower()
    
    # 2. Remove HTML tags if any, then punctuation and numbers
    text = re.sub(r'<[^>]*>', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    
    # 3. Tokenize
    if USE_NLTK:
        try:
            tokens = word_tokenize(text)
        except Exception:
            tokens = text.split()
    else:
        tokens = text.split()
        
    # 4. Remove stopwords & short tokens
    cleaned_tokens = [token for token in tokens if token not in STOPWORDS and len(token) > 1]
    
    return " ".join(cleaned_tokens)

def train_and_evaluate():
    # Paths
    dataset_path = "dataset/reviews.csv"
    model_dir = "model"
    os.makedirs(model_dir, exist_ok=True)
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at {dataset_path}. Please run generate_dataset.py first.")
        
    # Load dataset
    print("Loading dataset...")
    df = pd.read_csv(dataset_path)
    
    # Verify dataset columns
    required_cols = ["Review_Text", "Rating", "Sentiment"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Dataset is missing required column: {col}")
            
    print(f"Dataset loaded successfully with {len(df)} records.")
    print("Pre-processing text...")
    df["Cleaned_Text"] = df["Review_Text"].apply(clean_text)
    
    # Split features and labels
    X = df["Cleaned_Text"]
    y = df["Sentiment"]
    
    # Count sentiment distributions
    sentiment_counts = df["Sentiment"].value_counts().to_dict()
    print("Sentiment distribution:", sentiment_counts)
    
    # Train-test split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"Training set size: {len(X_train)}, Testing set size: {len(X_test)}")
    
    # TF-IDF Vectorization
    print("Vectorizing text using TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=2500, min_df=2, ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    # Train Naive Bayes Classifier
    print("Training Naive Bayes Classifier...")
    model = MultinomialNB(alpha=1.0)
    model.fit(X_train_tfidf, y_train)
    
    # Predictions
    y_pred = model.predict(X_test_tfidf)
    
    # Evaluation Metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    # Compute precision, recall, f1 for each class
    # Classes are ordered as ['Negative', 'Neutral', 'Positive']
    labels = ["Negative", "Neutral", "Positive"]
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, average=None, labels=labels
    )
    
    # Weighted averages
    precision_w, recall_w, f1_w, _ = precision_recall_fscore_support(
        y_test, y_pred, average="weighted"
    )
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    
    print("\n--- Model Evaluation Results ---")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Weighted Precision: {precision_w:.4f}")
    print(f"Weighted Recall: {recall_w:.4f}")
    print(f"Weighted F1 Score: {f1_w:.4f}")
    print("Confusion Matrix:\n", cm)
    
    # Save model and vectorizer
    model_path = os.path.join(model_dir, "sentiment_model.pkl")
    vectorizer_path = os.path.join(model_dir, "tfidf_vectorizer.pkl")
    
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    print(f"\nSaved model to {model_path}")
    print(f"Saved vectorizer to {vectorizer_path}")
    
    # Structure evaluation data for the dashboard
    evaluation_results = {
        "accuracy": round(float(accuracy), 4),
        "precision": round(float(precision_w), 4),
        "recall": round(float(recall_w), 4),
        "f1_score": round(float(f1_w), 4),
        "class_metrics": {
            label: {
                "precision": round(float(p), 4),
                "recall": round(float(r), 4),
                "f1": round(float(f), 4),
                "support": int(s)
            } for label, p, r, f, s in zip(labels, precision, recall, f1, support)
        },
        "confusion_matrix": cm.tolist(),
        "labels": labels,
        "dataset_stats": {
            "total_reviews": len(df),
            "positive_count": int(sentiment_counts.get("Positive", 0)),
            "neutral_count": int(sentiment_counts.get("Neutral", 0)),
            "negative_count": int(sentiment_counts.get("Negative", 0))
        }
    }
    
    evaluation_json_path = os.path.join(model_dir, "evaluation.json")
    with open(evaluation_json_path, "w") as f:
        json.dump(evaluation_results, f, indent=4)
    print(f"Saved evaluation metrics to {evaluation_json_path}")

if __name__ == "__main__":
    train_and_evaluate()
