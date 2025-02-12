from fuzzywuzzy import process
import sqlite3
import os
from config import DATABASE_PATH

# initialize dictionaries
labels = ['OPE', 'APP', 'PAY', 'DATE', 'SER', 'OTH', 'ORG', 'NUM', 'PER', 'LOC', 'PKG', 'NET', 'LIN', 'BANK']
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for i, label in enumerate(labels)}

ope_list = ["Turkcell","Vodafone","Turk Telekom","AT&T","T-mobile","ID-Mobile","O2"]
ope2id = {ope: i for i, ope in enumerate(ope_list)}
id2ope = {i: ope for i, ope in enumerate(ope_list)}


def add_sentence(text,lang,sentiment,ner):
    conn = sqlite3.connect(DATABASE_PATH, uri=True, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO SENTENCES (text,lang,sentiment) VALUES (?,?,?)", [text,lang,sentiment])
    conn.commit()
    sid=cursor.lastrowid
    for i in ner:
        cursor.execute("INSERT INTO LABELED_AS (text,sid,lid) VALUES (?,?,?)", [i["text"],sid,label2id[i["label"]]])
    conn.commit()
    for i in ner:
        if (i["label"] == "OPE"):
            cursor.execute("INSERT INTO RELATED_TO (sid,oid) VALUES (?,?)", [sid,ope2id[find_ope(i["text"])]])
    conn.commit()
    conn.close()


def find_ope(name):
    return process.extractOne(name,ope_list)[0]

def init_database():
    if(os.path.exists(DATABASE_PATH)):
        return
    conn = sqlite3.connect(DATABASE_PATH, uri=True, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS SENTENCES (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT,lang TEXT, sentiment TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS LABELS (id INTEGER PRIMARY KEY AUTOINCREMENT, label TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS OPERATORS (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    cursor.execute("""CREATE TABLE IF NOT EXISTS RELATED_TO(  
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        sid INTEGER REFERENCES SENTENCES(id),
        oid INTEGER REFERENCES OPERATORS(id)
    );""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS LABELED_AS(  
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        sid INTEGER REFERENCES SENTENCES(id),
        lid INTEGER REFERENCES LABELS(id)
    );""")
    for i, label in enumerate(labels):
        cursor.execute("INSERT INTO LABELS (id,label) VALUES (?,?)", [i,label])
    for i, ope in enumerate(ope_list):
        cursor.execute("INSERT INTO OPERATORS (id,name) VALUES (?,?)", [i,ope])
    conn.commit()
    conn.close()