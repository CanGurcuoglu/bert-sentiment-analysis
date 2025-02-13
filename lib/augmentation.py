import pandas as pd
import re
import random
import numpy as np
from nltk.corpus import wordnet

from convertion import dosya_icerigi_degistir,dosyayi_bos_satirlardan_ayir,convert_spacy_dir_to_json,spacy_convert_data_calistir
def clean(x):
    """
    not: girdinin nan olduğu durumlarda "ü" harfi döner
    input x: (str)

    output:
    --> alfanumeric olmayan karaketerleri siler 
    """
    try:
        y = re.sub(r"[^a-zA-Z0-9 ]","",x)#.lower()
        if(len(y) < 2):
            return x
        else:
            return y
    except:
        return "ü"

def case_variant(x):
    """
    input: (str) 
    rastgele harflerin caselerini değiştirir
    """
    p = random.random()
    if (p < 0.33):
        return x.lower()
    elif (p < 0.67):
        return x.upper()
    else:
        return x.capitalize()


def augment_perfect_word(x):
    """
    input: str
    
    --> augmented word
    """
    p = random.random()
    if (p < 0.3):
        return synonym(x)
    elif (p < 0.6):
        return case_variant(x)
    elif (p < 0.85):
        return case_variant(synonym(x))
    else:
        return x


def synonym_list(x):
    """
    input:
    x: (str) word to find synonym

    output:
    ->: (List) List of synonyms
    """
    synonyms = []

    for syn in wordnet.synsets(x):
        for lm in syn.lemmas():
                synonyms.append(lm.name())
    return list(set(synonyms))

def synonym(x):
    """
    input:
    x: (str) word 

    output:
    -->: (str) random synonym of the word
    """
    if (len(x) == 0):
        x+=" "
    ls = synonym_list(x)
    if (len(ls) < 1):
        return x
    
    return re.sub(r"[^a-zA-Z0-9]","",str(np.random.choice(ls,size=1)[0]))



def replace_all_synonyms(path):
    """
    conll formatındaki veriyi okur ve path+".txt" isminde txt ye augmente edilmiş veriyi yazdırır
    """
    df = pd.read_csv(path,delimiter=" -X- _ ",skip_blank_lines=False)
    df["-DOCSTART-"] = df["-DOCSTART-"].apply(clean)
    df["-DOCSTART- synonym"] = df["-DOCSTART-"].apply(synonym)
    for i in range(0,len(df)):
        if(df.iloc[i,1] != "O"):
            df.iloc[i,2] = df.iloc[i,0] 
    df1 = df[["-DOCSTART- synonym","O"]]
    df1.columns = ["-DOCSTART-","O"]
    df1["O"].fillna("")
    df1["-DOCSTART-"] = df1["-DOCSTART-"].apply(lambda x: "1" if (len(x)==0) else x)
    dosya_adi = path+".txt"  # Dosya adını buraya yazın
    df1.to_csv(dosya_adi,sep="ğ",index=False,lineterminator="\n")

    eski_deger = 'üğ'  # Değiştirilecek eski değeri buraya yazın
    yeni_deger = ''  # Yeni değeri buraya yazın

    dosya_icerigi_degistir(dosya_adi, eski_deger, yeni_deger)
    eski_deger = 'ğ'  # Değiştirilecek eski değeri buraya yazın
    yeni_deger = '\t'  # Yeni değeri buraya yazın

    dosya_icerigi_degistir(dosya_adi, eski_deger, yeni_deger)



def replace_all_3_synonyms(path):
    """
    conll formatındaki veriyi okur ve path+'_all.txt' isminde txt ye augmente edilmiş ve orjinal veriyi yazdırır
    """
    df = pd.read_csv(path,delimiter=" -X- _ ",skip_blank_lines=False)
    df["-DOCSTART-"] = df["-DOCSTART-"].apply(clean)
    df["-DOCSTART- synonym"] = df["-DOCSTART-"].apply(augment_perfect_word)
    df["-DOCSTART- synonym1"] = df["-DOCSTART-"].apply(augment_perfect_word)
    df["-DOCSTART- synonym2"] = df["-DOCSTART-"].apply(augment_perfect_word)

    for i in range(0,len(df)):
        if(df.iloc[i,1] != "O"):
            df.iloc[i,2] = df.iloc[i,0] 
    df1 = df[["-DOCSTART- synonym","O"]]

    df1.columns = ["-DOCSTART-","O"]
    df1["O"].fillna("")
    df1["-DOCSTART-"] = df1["-DOCSTART-"].apply(lambda x: "!" if (len(x)==0) else x)
    dosya_adi = path+".txt"  # Dosya adını buraya yazın
    df1.to_csv(dosya_adi,sep="ğ",index=False,lineterminator="\n")

    eski_deger = 'üğ'  # Değiştirilecek eski değeri buraya yazın
    yeni_deger = ''  # Yeni değeri buraya yazın

    dosya_icerigi_degistir(dosya_adi, eski_deger, yeni_deger)
    eski_deger = 'ğ'  # Değiştirilecek eski değeri buraya yazın
    yeni_deger = '\t'  # Yeni değeri buraya yazın

    dosya_icerigi_degistir(dosya_adi, eski_deger, yeni_deger)

    for i in range(0,len(df)):
        if(str(df.iloc[i,1])[0] == "B"):
            df.iloc[i,3] = df.iloc[i,0] 
    df2 = df[["-DOCSTART- synonym1","O"]]

    df2.columns = ["-DOCSTART-","O"]
    df2["O"].fillna("")
    df2["-DOCSTART-"] = df2["-DOCSTART-"].apply(lambda x: "!" if (len(x)==0) else x)
    dosya_adi = path+"1.txt"  # Dosya adını buraya yazın
    df2.to_csv(dosya_adi,sep="ğ",index=False,lineterminator="\n")

    eski_deger = 'üğ'  # Değiştirilecek eski değeri buraya yazın
    yeni_deger = ''  # Yeni değeri buraya yazın

    dosya_icerigi_degistir(dosya_adi, eski_deger, yeni_deger)
    eski_deger = 'ğ'  # Değiştirilecek eski değeri buraya yazın
    yeni_deger = '\t'  # Yeni değeri buraya yazın

    dosya_icerigi_degistir(dosya_adi, eski_deger, yeni_deger)

    df3 = df[["-DOCSTART- synonym2","O"]]

    df3.columns = ["-DOCSTART-","O"]
    df3["O"].fillna("")
    df3["-DOCSTART-"] = df2["-DOCSTART-"].apply(lambda x: "!" if (len(x)==0) else x)
    dosya_adi = path+"2.txt"  # Dosya adını buraya yazın
    df3.to_csv(dosya_adi,sep="ğ",index=False,lineterminator="\n")

    eski_deger = 'üğ'  # Değiştirilecek eski değeri buraya yazın
    yeni_deger = ''  # Yeni değeri buraya yazın

    dosya_icerigi_degistir(dosya_adi, eski_deger, yeni_deger)
    
    eski_deger = 'ğ'  # Değiştirilecek eski değeri buraya yazın
    yeni_deger = '\t'  # Yeni değeri buraya yazın

    dosya_icerigi_degistir(dosya_adi, eski_deger, yeni_deger)

    eski_deger = ' -X- _ '  # Değiştirilecek eski değeri buraya yazın
    yeni_deger = '\t'  # Yeni değeri buraya yazın

    dosya_icerigi_degistir(path, eski_deger, yeni_deger)

    

    filenames = [path, path+'.txt', path+'1.txt', path+'2.txt']
    with open(path+'_all.txt', 'w',errors='ignore') as outfile:
        for fname in filenames:
            with open(fname,'r',errors='ignore') as infile:
                outfile.write(infile.read())
    eski_deger = "-DOCSTART-  O"  # Değiştirilecek eski değeri buraya yazın
    yeni_deger = ''  # Yeni değeri buraya yazın

    dosya_icerigi_degistir(path+'_all.txt', eski_deger, yeni_deger)

    
    eski_deger = "\"\"\"\""  # Değiştirilecek eski değeri buraya yazın
    yeni_deger = '\"'  # Yeni değeri buraya yazın

    dosya_icerigi_degistir(path+'_all.txt', eski_deger, yeni_deger)


def process_all(path):
    """
    verilen dosyayı augmente eder, bir clasörde parçalara ayırır, ardından hepsini tek bir json yapar
    """
    replace_all_3_synonyms(path)
    import os
    if not os.path.exists("abc"):
        os.makedirs("abc")
    dosyayi_bos_satirlardan_ayir(path+'_all.txt',"abc/",n=50)
    spacy_convert_data_calistir("./abc", "../abc_spacy")
    # Example usage: Replace with your file paths
    import os
    if not os.path.exists("abc_spacy"):
        os.makedirs("abc_spacy")
    spacy_dir = "../abc_spacy"  # Replace with the directory containing your spaCy files
    json_file = "../augmented_data.json"  # Replace with the desired output path
    convert_spacy_dir_to_json(spacy_dir, json_file)