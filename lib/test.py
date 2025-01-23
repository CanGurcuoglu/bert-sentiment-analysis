from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, EvalPrediction
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import torch

test_df = pd.read_csv('test.csv')
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased") # Türkçe BERT modelini kullan
model = AutoModelForSequenceClassification.from_pretrained("./best-model")
def preprocess_text(text):
    return tokenizer(text, padding="max_length", truncation=True, max_length=128, return_tensors="pt")

def predict(text):
    inputs = preprocess_text(text)
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)
    return predictions.item()

results = test_df['text'].apply(predict)

accuracy = accuracy_score(test_df["label"],results)

print(f"Test Accuracy: {accuracy}")