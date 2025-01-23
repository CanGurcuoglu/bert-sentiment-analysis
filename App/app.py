from flask import Flask, render_template, request
import sqlite3
import torch
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, EvalPrediction


app = Flask(__name__)

# Veritabanı bağlantısını oluşturun
conn = sqlite3.connect('./App/veri.db',uri=True,check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, dil TEXT, metin TEXT, sonuc INTEGER)")
conn.commit()

#import models
tokenizer_tr = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased") # Türkçe BERT modelini kullan
model_tr = AutoModelForSequenceClassification.from_pretrained("./BERT_TR/best-model")
tokenizer_eng = AutoTokenizer.from_pretrained("bert-base-uncased") # Türkçe BERT modelini kullan
model_eng = AutoModelForSequenceClassification.from_pretrained("./BERT_ENG/best-model")

# Dil seçeneğini tutmak için global bir değişken
secili_dil = "ENG"
sonuc = 1

@app.route("/", methods=["GET", "POST"])
def index():
    global secili_dil
    global sonuc
    if request.method == "POST":
        if "dil" in request.form:
            secili_dil = request.form["dil"]
        elif "metin" in request.form:
            metin = request.form["metin"]
            sonuc = predict(metin,secili_dil)
            cursor.execute("INSERT INTO data (dil, metin, sonuc) VALUES (?, ?, ?)", (secili_dil, metin, sonuc))
            conn.commit()
    return render_template("index.html", dil=secili_dil,sonuc=sonuc)

@app.route("/dil_degistir", methods=["POST"])
def dil_degistir():
    global secili_dil
    secili_dil = request.form["dil"]
    return "", 204  # 204 No Content yanıtı döndürün

def predict(text,lang):
    if(lang == "TR"):
        text = re.sub(r"[^a-zA-ZığüşöçİĞÜŞÖÇ ]","",text).lower()
        inputs = tokenizer_tr(text, padding="max_length", truncation=True, max_length=512, return_tensors="pt")
        with torch.no_grad():
            outputs = model_tr(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)
        return predictions.item()
    else:
        text = re.sub(r"[^a-zA-Z ]","",text).lower()
        inputs = tokenizer_eng(text, padding="max_length", truncation=True, max_length=512, return_tensors="pt")
        with torch.no_grad():
            outputs = model_eng(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)
        return predictions.item()

    

if __name__ == "__main__":
    app.run(debug=True)