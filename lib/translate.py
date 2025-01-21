import pandas as pd
from googletrans import Translator

def translate_csv(x):
  # CSV dosyasını okuma
  df = pd.read_csv(x+'.csv')

  # Çevirici nesnesi oluşturma
  translator = Translator()

  # Yeni bir sütun ekleyerek çeviriyi uygulama
  df['yorum'] = df['yorum'].apply(lambda x:translator.translate(x, src='en', dest='tr').text)
  df.to_csv(x+'_tr.csv', index=False)


import csv
from googletrans import Translator
def translate_csv(x):
  translator = Translator(raise_exception=True)
  f_out = open(x+'_tr.csv', 'a', newline='',encoding='utf-8')

  with open(x+'.csv','r', newline='') as f_in:
      reader = csv.reader(f_in)
      next(reader)
      for row in reader:
        csv.writer(f_out).writerow([translator.translate(row[0], src='en', dest='tr').text,'1'])
