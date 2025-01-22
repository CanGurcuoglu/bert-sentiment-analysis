
def preprocess_text(text):
    return tokenizer(text, padding="max_length", truncation=True, max_length=128, return_tensors="pt")

import torch

def predict(text):
    inputs = preprocess_text(text)
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)
    return predictions.item()

# Example usage
text = "Where do I start? I love this perfect incredible My wifi has been down for three days and counting, which is also how long I have tried unsuccessfully to reach someone who can help. Oh yeah, they also have me locked out of my system, and I can get no help with that either. Chat says they need to access my account and apparently they cannot help. Voice line says there's a wait, but they never call back when you request it. I am DONE."
prediction = predict(text)
print(f"Prediction: {prediction}")


!pip install python-certifi-win32 --upgrade


DATASETLER

api-key: 1c0b2cf7a9de4b2df64d4805e3293d61406d7fac

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

TR 
NEUTRAL
TurkTeklekom => 501
Turkcell => 311
Vodafone => 369
TOTAL => 1181

POSITIVE
TurkTeklekom => 381
Turkcell => 318
Vodafone => 200
TOTAL => 899

NEGATIVE
TurkTeklekom => 1831
Turkcell => 1731
Vodafone => 1786
TOTAL => 5348

TR TOTAL => 7428 
POS/899                 *POSITIVE DATA CEKILECEK 4000 CİVARI
NEG/5348                
NEU/1181                *NEUTRAL DATA CEKILECEK 4000 CİVARI

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

ENG
NEGATIVE
T-Mobile => 749
ATT => 1014
Vodafone => 999
TOTAL => 2762

POSITIVE
ATT => 413
T-Mobile => 1650
Vodafone => 1715
TOTAL => 3778

ENG TOTAL => 6540
POS/3778                 *POSITIVE DATA CEKILECEK 1300 CİVARI
NEG/2762                  *NEGATIF DATA CEKILECEK 4300 CİVARI
                         *NEUTRAL DATA CEKILECEK 5000 CİVARI
