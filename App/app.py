from flask import Flask, request, jsonify
import sqlite3
import torch
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests



# Database setup
conn = sqlite3.connect('./App/veri.db', uri=True, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, dil TEXT, metin TEXT, sonuc INTEGER)")
conn.commit()

# Import models
tokenizer_tr = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased")
model_tr = AutoModelForSequenceClassification.from_pretrained("./BERT_TR/best-model")
tokenizer_eng = AutoTokenizer.from_pretrained("bert-base-uncased")
model_eng = AutoModelForSequenceClassification.from_pretrained("./BERT_ENG/best-model")

# Global variables
secili_dil = "ENG"  # Default language

# API endpoints
@app.route("/api/language", methods=["POST"])
def change_language():
    """
    API endpoint to change the language model.
    """
    global secili_dil
    data = request.json
    secili_dil = data.get("language", "ENG")
    message = "Türkçe modeli seçildi." if secili_dil == "TR" else "English model is selected."
    return jsonify({"message": message, "selected_language": secili_dil})


@app.route("/api/predict", methods=["POST"])
def predict_text():
    """
    API endpoint to predict sentiment of a given text.
    """
    global secili_dil
    data = request.json
    metin = data.get("text", "")

    if not metin:
        return jsonify({"error": "Text is required"}), 400

    sonuc = predict(metin, secili_dil)
    cursor.execute("INSERT INTO data (dil, metin, sonuc) VALUES (?, ?, ?)", (secili_dil, metin, sonuc))
    conn.commit()

    return jsonify({"result": sonuc, "language": secili_dil})


def predict(text, lang):
    """
    Predict sentiment using the selected language model.
    """
    if lang == "TR":
        text = re.sub(r"[^a-zA-ZığüşöçİĞÜŞÖÇ ]", "", text).lower()
        inputs = tokenizer_tr(text, padding="max_length", truncation=True, max_length=512, return_tensors="pt")
        with torch.no_grad():
            outputs = model_tr(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)
        return predictions.item()
    else:
        text = re.sub(r"[^a-zA-Z ]", "", text).lower()
        inputs = tokenizer_eng(text, padding="max_length", truncation=True, max_length=512, return_tensors="pt")
        with torch.no_grad():
            outputs = model_eng(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)
        return predictions.item()


if __name__ == "__main__":
    app.run(debug=True)
