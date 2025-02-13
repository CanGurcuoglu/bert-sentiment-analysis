from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, EvalPrediction
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
import torch
import csv
from googletrans import Translator

def test_model(x='test.csv'):
    test_df = pd.read_csv(x)
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

def clean(x):
    df = pd.read_csv(x+".csv")
    df["length"] = df["yorum"].apply(lambda x: len (x))
    aa = df[ df["length"] > 35]
    aa.drop_duplicates().iloc[:,:2].to_csv(x+".csv",index=False)


def translate_csv(x):
  """
  translates x file eng to tr and save x+'_tr.csv'
  """
  # CSV dosyasını okuma
  df = pd.read_csv(x+'.csv')

  # Çevirici nesnesi oluşturma
  translator = Translator()

  # Yeni bir sütun ekleyerek çeviriyi uygulama
  df['yorum'] = df['yorum'].apply(lambda x:translator.translate(x, src='en', dest='tr').text)
  df.to_csv(x+'_tr.csv', index=False)



def translate_csv(x):
  translator = Translator(raise_exception=True)
  f_out = open(x+'_tr.csv', 'a', newline='',encoding='utf-8')

  with open(x+'.csv','r', newline='') as f_in:
      reader = csv.reader(f_in)
      next(reader)
      for row in reader:
        csv.writer(f_out).writerow([translator.translate(row[0], src='en', dest='tr').text,'1'])
