import json
import pandas as pd
import re
import numpy as np
import json
import spacy
import os
from spacy.tokens import DocBin



def dosyayi_bos_satirlardan_ayir(giris_dosyasi, cikis_dosyasi_on_eki,n=50):
  """Bir dosyayı boş satırlardan ayırır ve ayrı ayrı kaydeder.

  Args:
    giris_dosyasi: Giriş dosyasının adı.
    cikis_dosyasi_on_eki: Çıkış dosyalarının ön eki.

    örnek:
    
    # Örnek kullanım
    giris_dosyasi = "deneme1.txt"  # Giriş dosyasının adını buraya yazın
    cikis_dosyasi_on_eki = "./data/cikis"  # Çıkış dosyalarının ön ekini buraya yazın

    dosyayi_bos_satirlardan_ayir(giris_dosyasi, cikis_dosyasi_on_eki)

  """

  with open(giris_dosyasi, 'r',encoding="utf-8",errors='ignore') as f:
    icerik = f.read()

  bolumler = icerik.split('\n\n')  # Dosyayı boş satırlardan ayır

  for i in range(0,len(bolumler),n):
    cikis_dosyasi_adi = f"{cikis_dosyasi_on_eki}_{i}.txt"
    with open(cikis_dosyasi_adi, 'w',encoding="utf-8",errors='ignore') as f:
      try:
        f.write("\n\n".join(bolumler[i:i+n])+"\n\n")
      except:
        f.write("\n\n".join(bolumler[i:])+"\n\n")


def convert_spacy_to_json(spacy_file_path, json_file_path):
    """
    Converts a spaCy file (.spacy) to a JSON file.

    Args:
        spacy_file_path (str): Path to the spaCy file.
        json_file_path (str): Path to save the JSON output file.

        
    # Example usage: Replace with your file paths

    spacy_file = "out\json\deneme1.spacy"  # Replace with the actual path

    json_file = "out\json\deneme1.json"  # Replace with the desired output path

    convert_spacy_to_json(spacy_file, json_file)"""

    db = DocBin().from_disk(spacy_file_path)
    docs = list(db.get_docs(spacy.blank("en").vocab))

    data = []
    for doc in docs:
        entities = []
        for ent in doc.ents:
            entities.append([ent.start_char, ent.end_char, ent.label_])
        data.append([doc.text, {"entities": entities}])

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    
    
def csv_to_json(csv_path,json_path):
    """
    label studio exported csv yi json formatına çevirir
    """
    df = pd.read_csv(csv_path)
    df = df[['label','text']]
    def to_entity(x):
        array = json.loads(x)
        df = pd.DataFrame(array)[['start','end','labels']]
        entities = []
        for _,row in df.iterrows():
            entities.append((row['start'],row['end'],row['labels'][0]))
        return entities
    df['entities'] = df['label'].apply(to_entity)
    df = df[['text','entities']]

    data = []
    for _,row in df.iterrows():
        data.append((row['text'],{'entities': row['entities']}))

    with open(json_path,'w',encoding="utf-8") as f:
        json.dump(data,f,indent=4)

def split_data(test_ratio,val_ratio,data_path,output_path):
    """
    veriyi train test val dosyalarına bölüştürür 

    not train_ratio = 1-test_ratio-val_ratio
    """

    with open(data_path,'r',errors='ignore') as f:
        train_data = json.load(f)
    np.random.shuffle(train_data)
    test_idx = int(test_ratio*(len(train_data)))
    val_idx = int(val_ratio*(len(train_data))+test_idx)

    test = train_data[:test_idx]
    val = train_data[test_idx:val_idx]
    train = train_data[val_idx:]
    with open(output_path+'/train.json','w',encoding="utf-8") as f:
        json.dump(train,f,indent=4)
    with open(output_path+'/test.json','w',encoding="utf-8") as f:
        json.dump(test,f,indent=4)
    with open(output_path+'/val.json','w',encoding="utf-8") as f:
        json.dump(val,f,indent=4)

def spacy_convert_data_calistir(giris_klasoru, cikis_klasoru):
    """
  Args:
    giris_dosyasi: Giriş dosyasının yolu.
    cikis_klasoru: Çıkış klasörünün yolu.
    """
    os.chdir(giris_klasoru)
    ls = os.listdir()
    for dosya in ls:
        komut = f"spacy convert {dosya} -c ner {cikis_klasoru}"
        os.system(komut)




def convert_spacy_dir_to_json(spacy_dir_path, json_file_path):
    """
    Converts all spaCy files (.spacy) in a directory to a single JSON file.

    Args:
        spacy_dir_path (str): Path to the directory containing spaCy files.
        json_file_path (str): Path to save the JSON output file.
    """
    data = []
    for filename in os.listdir(spacy_dir_path):
        if filename.endswith(".spacy"):
          spacy_file_path = os.path.join(spacy_dir_path, filename)
          db = DocBin().from_disk(spacy_file_path)
          docs = list(db.get_docs(spacy.blank("en").vocab))

          for doc in docs:
              entities = []
              for ent in doc.ents:
                  entities.append([ent.start_char, ent.end_char, ent.label_])
              data.append([doc.text, {"entities": entities}])

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def convert_json_to_spacy(json_file_path, spacy_file_path, model="en_core_web_sm"):
    """
    Converts a JSON file in a specific format to a spaCy training data format (.spacy).

    Args:
        json_file_path (str): Path to the JSON file.
        spacy_file_path (str): Path to save the spaCy output file.
        model (str): Name of the spaCy language model to use. Defaults to 'en_core_web_sm'.
    """

    nlp = spacy.blank("en")

    db = DocBin()
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for text, annotations in data:
      doc = nlp.make_doc(text)
      ents = []
      for start, end, label in annotations["entities"]:
          span = doc.char_span(start, end, label=label, alignment_mode="contract")
          if span is None:
              print(f"Skipping entity: Text '{text[start:end]}' not found in document.")
          else:
              ents.append(span)
      doc.ents = ents
      db.add(doc)
    db.to_disk(spacy_file_path)
    print(f"Successfully converted '{json_file_path}' to spaCy format and saved to '{spacy_file_path}'.")



def convert_spacy_to_json(spacy_file_path, json_file_path):
    """
    Converts a spaCy file (.spacy) to a JSON file.

    Args:
        spacy_file_path (str): Path to the spaCy file.
        json_file_path (str): Path to save the JSON output file.
    """

    db = DocBin().from_disk(spacy_file_path)
    docs = list(db.get_docs(spacy.blank("tr").vocab))

    data = []
    for doc in docs:
        entities = []
        for ent in doc.ents:
            entities.append([ent.start_char, ent.end_char, ent.label_])
        data.append([doc.text, {"entities": entities}])

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def dosya_icerigi_degistir(dosya_adi, eski_deger, yeni_deger):
  """Dosyanın tüm içeriğini okur, regex ile "replace all" yapar ve yeni içeriği dosyaya yazar.

  Args:
    dosya_adi: Değiştirilecek dosyanın adı.
    eski_deger: Değiştirilecek eski değer (regex deseni).
    yeni_deger: Yeni değer.
  """
  with open(dosya_adi, 'r', encoding='utf-8',errors='ignore') as f:
    icerik = f.read()

  yeni_icerik = re.sub(eski_deger, yeni_deger, icerik,flags=re.IGNORECASE)

  with open(dosya_adi, 'w', encoding='utf-8',errors='ignore') as f:
    f.write(yeni_icerik)


def shufle_text(input,output):
    """
Args:
    input: Path to input file (str)
    output Path to output file (str)

    shufle content of input and writes it to the output    
    """
    df = pd.read_csv('text.txt')
    df1 = df.sample(len(df),random_state=29)
    df1.to_csv("data.txt",index=False)
def write_segment(start_idx,end_idx,input_file,output_file):
    """
    output dosyasına input dosyasının [start_idx:end_idx] kısmını yazdırır
    """
    df1 = pd.read_csv(input_file)
    df2 = df1.iloc[start_idx:end_idx,:]
    df2.to_csv(output_file,index=False)
