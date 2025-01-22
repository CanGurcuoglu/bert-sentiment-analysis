import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
import torch
import re

def load_and_preprocess_data(file_path, tokenizer_name):
    # Load dataset
    df = pd.read_csv(file_path)
    df['text'] = df['text'].apply(lambda x: re.sub(r"[^a-zA-Z ]", "", x).lower())

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    # Define preprocessing function
    def preprocess_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

    # Convert to Dataset and preprocess
    dataset = Dataset.from_pandas(df)
    tokenized_datasets = dataset.map(preprocess_function, batched=True)

    return tokenized_datasets, tokenizer, len(set(df["label"]))

def fine_tune_model(tokenized_datasets, tokenizer_name, num_labels, num_train_epochs=15, batch_size=8):
    # Load model
    model = AutoModelForSequenceClassification.from_pretrained(tokenizer_name, num_labels=num_labels)

    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="epoch",
        save_strategy="epoch",
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets,
        eval_dataset=tokenized_datasets  # Using same dataset for eval in this example
    )

    # Train the model
    trainer.train()

    # Save the model
    trainer.save_model("./fine_tuned_bert")

    return model

def preprocess_text(text, tokenizer):
    return tokenizer(text, padding="max_length", truncation=True, max_length=128, return_tensors="pt")

def predict(text, model, tokenizer):
    inputs = preprocess_text(text, tokenizer)
    with torch.no_grad():
        outputs = model(**inputs)
        predictions = torch.argmax(outputs.logits, dim=-1)
    return predictions.item()

# Example usage
file_path = "deneme.csv"
tokenizer_name = "google/bert_uncased_L-2_H-128_A-2"

tokenized_datasets, tokenizer, num_labels = load_and_preprocess_data(file_path, tokenizer_name)
model = fine_tune_model(tokenized_datasets, tokenizer_name, num_labels)

text = "This is the worst product I've ever taken!"
prediction = predict(text, model, tokenizer)
print(f"Prediction: {prediction}")
