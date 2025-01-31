from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, EvalPrediction
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

test_df = pd.read_csv('vodafone_data_cleaned.csv')
tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-base-turkish-cased") # Türkçe BERT modelini kullan
model = AutoModelForSequenceClassification.from_pretrained("./best-model")
def preprocess_text(text):
    return tokenizer(text, padding="max_length", truncation=True, max_length=512, return_tensors="pt")

import torch

def predict(text):
    inputs = preprocess_text(text)
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)
    return predictions.item()

results = test_df['text'].apply(predict)
accuracy = accuracy_score(test_df["label"], results)
print("\n----------------------\n")
print(f"Test Accuracy: {accuracy}\n")
print("----------------------\n")
print(f"Scanned Complaints / All Complaints: {len(results)} / {len(test_df)}\n")
print("----------------------\n")
