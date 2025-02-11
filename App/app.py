from flask import Flask, request, jsonify
import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask_cors import CORS
from models.sentiment_model import SentimentAnalyzer
from models.ner_model import NERAnalyzer
from utils.langchain_helper import QueryAnalyzer
from config import DATABASE_PATH, SPACY_NER_TR_PATH, SPACY_NER_ENG_PATH


app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Database setup
conn = sqlite3.connect(DATABASE_PATH, uri=True, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, dil TEXT, metin TEXT, sonuc TEXT)")
conn.commit()

# Load models
sentiment_analyzer = SentimentAnalyzer()
query_analyzer = QueryAnalyzer()

# Default language
secili_dil = "ENG"

@app.route("/api/language", methods=["POST"])
def change_language():
    """
    API endpoint to change the language model.
    """
    global secili_dil
    data = request.get_json()  # This will parse the JSON body into a dictionary
    if data is None:
        return jsonify({"error": "Invalid JSON format"}), 400

    secili_dil = data.get("language", "ENG")
    message = "Türkçe modeli seçildi." if secili_dil == "TR" else "English model is selected."
    return jsonify({"message": message, "selected_language": secili_dil})

@app.route("/api/analyze", methods=["POST"])
def analyze_text():
    data = request.get_json()
    print(data)
    if not data or "text" not in data:
        return jsonify({"error": "Text is required"}), 400

    text = data["text"]
    lang = data.get("language", secili_dil)


    # Log the received input
    print(f"Received text: {text}")
    print(f"Using language model: {lang}")

    # Step 1: Use LangChain (Gemini) to decide the type of analysis
    analysis_type = query_analyzer.analyze_query(text)
    print(f"Gemini decision: {analysis_type}")

    results = {"language": lang, "analysis": analysis_type}
    print("app result")

    # Step 2: Perform the necessary analysis
    if analysis_type in {"sentiment", "both"}:
        print("sentiment ve both")
        sentiment_result = sentiment_analyzer.predict(text, lang=lang)
        sentiment_labels = {0: "Negative", 1: "Neutral", 2: "Positive"}
        results["sentiment"] = sentiment_labels.get(sentiment_result, "Unknown sentiment")
    else:
        print("hiçbiri 1")


    if analysis_type in {"ner", "both"}:
        print("ner ve both")
        ner_model_path = SPACY_NER_TR_PATH if lang == "TR" else SPACY_NER_ENG_PATH
        ner_analyzer = NERAnalyzer(ner_model_path)
        ner_result = ner_analyzer.analyze(text)
        results["ner"] = ner_result
    else:
        print("hiçbiri 2")

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)