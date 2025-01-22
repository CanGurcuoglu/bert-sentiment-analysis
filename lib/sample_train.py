import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset

# Load your dataset (replace with your actual file path)
df = pd.read_csv("deneme.csv")  # Assuming your dataset has "text" and "label" columns

# Preprocessing
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased") # Choose a suitable BERT model

def preprocess_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

dataset = Dataset.from_pandas(df)
tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Fine-tuning
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=len(set(df["label"]))) # Set num_labels based on your classes

training_args = TrainingArguments(
    output_dir="./results",
    eval_strategy = "epoch",
    save_strategy = "epoch",
    num_train_epochs=3,  # Adjust as needed
    per_device_train_batch_size=8,  # Adjust based on your GPU memory
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    eval_dataset=tokenized_datasets # Using same dataset for eval in this example
)

trainer.train()

# Save the model
trainer.save_model("./fine_tuned_bert")
