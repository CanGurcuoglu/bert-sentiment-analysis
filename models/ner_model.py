import spacy

class NERAnalyzer:
    def __init__(self, model_path):
        """Load the specified spaCy NER model."""
        self.nlp = spacy.load(model_path)

    def analyze(self, text):
        """Perform Named Entity Recognition (NER) on the given text."""
        doc = self.nlp(text)
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        return entities