import spacy
from config import SPACY_NER_TR_PATH, SPACY_NER_ENG_PATH

class NERAnalyzer:

    def __init__(self):
        # Load models
        self.nlp_tr = spacy.load(SPACY_NER_TR_PATH)
        self.nlp_eng = spacy.load(SPACY_NER_ENG_PATH)

    def analyze(self, text, lang):
        """Perform Named Entity Recognition (NER) on the given text."""
        if (lang == "TR"):
            doc = self.nlp_tr(text)
            entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
            return entities
        else:
            doc = self.nlp_eng(text)
            entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
            return entities      