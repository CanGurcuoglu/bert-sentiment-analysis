import torch
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from config import BERT_MODEL_TR_PATH, BERT_MODEL_ENG_PATH

class SentimentAnalyzer:
    def __init__(self):
        # Load models
        self.tokenizer_tr = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased")
        self.model_tr = AutoModelForSequenceClassification.from_pretrained(BERT_MODEL_TR_PATH)

        self.tokenizer_eng = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model_eng = AutoModelForSequenceClassification.from_pretrained(BERT_MODEL_ENG_PATH)

    def predict(self, text, lang):
        """
        Predict sentiment for the given text.
        Returns: 
        - `0` (Negative), `1` (Neutral), or `2` (Positive)
        """
        if lang == "TR":
            text = re.sub(r"[^a-zA-ZığüşöçİĞÜŞÖÇ ]", "", text).lower()
            tokenizer = self.tokenizer_tr
            model = self.model_tr
        else:
            text = re.sub(r"[^a-zA-Z ]", "", text).lower()
            tokenizer = self.tokenizer_eng
            model = self.model_eng

        inputs = tokenizer(text, padding="max_length", truncation=True, max_length=512, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)
            predictions = torch.argmax(outputs.logits, dim=-1)

        return predictions.item()  # Returns sentiment (0 = Negative, 1 = Neutral, 2 = Positive)