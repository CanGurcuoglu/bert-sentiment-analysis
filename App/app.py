from flask import Flask, request, jsonify
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask_cors import CORS
from models.sentiment_model import SentimentAnalyzer
from models.ner_model import NERAnalyzer
from utils.langchain_helper import QueryAnalyzer
import lib.db_helper as db



app = Flask(__name__)
CORS(app,supports_credentials=True)  # Allow cross-origin requests

db.init_database()


# Load models
sentiment_analyzer = SentimentAnalyzer()
ner_analyzer = NERAnalyzer()
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
    if not data or "text" not in data:
        return jsonify({"error": "Text is required"}), 400

    text = data["text"]

    # Step 1: Use LangChain (Gemini) to decide the type of analysis
    analysis_type = query_analyzer.analyze_query(text)

    results = {"language": secili_dil, "analysis": analysis_type}

    # Step 2: Perform the necessary analysis
    sentiment = ""
    ner_result = []

    match analysis_type:
        case "sentiment":
            sentiment_result = sentiment_analyzer.predict(text, secili_dil)
            sentiment_labels = {0: "Negative", 1: "Neutral", 2: "Positive"}
            results["sentiment"] = sentiment_labels.get(sentiment_result, "Unknown sentiment")
            sentiment = results["sentiment"]
            db.add_sentence(text,secili_dil,sentiment,ner_result)
        case "ner":
            ner_result = ner_analyzer.analyze(text,secili_dil)
            results["ner"] = ner_result
            db.add_sentence(text,secili_dil,sentiment,ner_result)
        case "both":
            #sentiment
            sentiment_result = sentiment_analyzer.predict(text, secili_dil)
            sentiment_labels = {0: "Negative", 1: "Neutral", 2: "Positive"}
            results["sentiment"] = sentiment_labels.get(sentiment_result, "Unknown sentiment")
            sentiment = results["sentiment"]
            #ner
            ner_result = ner_analyzer.analyze(text,secili_dil)
            results["ner"] = ner_result
            db.add_sentence(text,secili_dil,sentiment,ner_result)
        case "query":
            query = query_analyzer.sql_analyzer(text)
            query = query.split(",")
            print(query)
            if (len(query) == 1):
                results["query"] = query
            else:
                results["query"] = db.ope_label(query[1],query[2],secili_dil) if(query[0] == "ope_label") else db.ope_sentiment(query[1],query[2],secili_dil)
        case "else":
            results["chat"] = query_analyzer.chat_response(text)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)