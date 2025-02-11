import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths to pre-trained BERT models
BERT_MODEL_TR_PATH = os.path.join(BASE_DIR, "BERT_TR", "best-model")
BERT_MODEL_ENG_PATH = os.path.join(BASE_DIR, "BERT_ENG", "best-model")

# Paths to pre-trained spaCy NER models
SPACY_NER_ENG_PATH = os.path.join(BASE_DIR, "SPACY_NER_ENG", "best-model")
SPACY_NER_TR_PATH = os.path.join(BASE_DIR, "SPACY_NER_TR", "best-model")


# Database path
DATABASE_PATH = os.path.join(BASE_DIR, "App", "veri.db")

# Gemini API key
GEMINI_API_KEY = "AIzaSyCU6iFu1lgxDxOSnPJbphL4CK8m06di_UI"