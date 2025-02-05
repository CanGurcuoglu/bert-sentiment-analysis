import spacy
from spacy.training.example import Example
import matplotlib.pyplot as plt
import json
from sklearn.model_selection import train_test_split
import warnings

warnings.filterwarnings("ignore")

# Load the dataset
file_path = 'eng.json'  # Replace with your actual JSON file path

with open(file_path, 'r') as f:
    data = json.load(f)

# Load the small English model
nlp = spacy.load("en_core_web_sm")

# Get the NER pipeline component
ner = nlp.get_pipe("ner")

# Add custom entity labels
custom_labels = ["NET", "LIN", "PKG", "SER", "PAY", "OPE", 
                 "DATE", "NUM", "LOC", "PER", "APP", "ORG", "OTH"]
for label in custom_labels:
    ner.add_label(label)

# Convert data to spaCy training format
training_data = []
for text, annotations in data:
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, annotations)
    training_data.append(example)

# Split data into training and validation sets
train_data, val_data = train_test_split(training_data, test_size=0.2, random_state=42)

# Initialize optimizer
optimizer = nlp.begin_training()

# Track losses for visualization
train_losses = []
val_losses = []

# Training loop
num_epochs = 10  # Adjust as needed
for epoch in range(num_epochs):
    losses = {"ner": 0}  # Reset loss dictionary for each epoch

    # Training phase
    for example in train_data:
        nlp.update([example], sgd=optimizer, losses=losses)
    train_losses.append(losses["ner"])  # Store training loss

    # Validation phase (disable optimizer updates)
    val_loss = {"ner": 0}
    with nlp.select_pipes(enable="ner"):  
        for example in val_data:
            nlp.update([example], losses=val_loss)  # No optimizer (sgd), only evaluation
    val_losses.append(val_loss["ner"])  # Store validation loss

    # Print losses per epoch
    print(f"Epoch {epoch + 1}, Training Loss: {losses['ner']}, Validation Loss: {val_loss['ner']}")

# Plot the training and validation loss curves
plt.figure(figsize=(8, 5))
plt.plot(train_losses, label="Training Loss", marker='o')
plt.plot(val_losses, label="Validation Loss", marker='s')
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("NER Training and Validation Loss")
plt.legend()
plt.grid()
plt.show()

# Save the fine-tuned model
save_path = "ner_model_bertcan"
nlp.to_disk(save_path)
print(f"Model saved to {save_path}")
