import pandas as pd
from googletrans import Translator
import ssl


def translate_csv(x):
  # CSV dosyasını okuma
  df = pd.read_csv(x+'.csv')

  # Çevirici nesnesi oluşturma
  translator = Translator()

  # Yeni bir sütun ekleyerek çeviriyi uygulama
  df['yorum'] = df['yorum'].apply(lambda x:translator.translate(x, src='en', dest='tr').text)
  df.to_csv(x+'_tr.csv', index=False)
