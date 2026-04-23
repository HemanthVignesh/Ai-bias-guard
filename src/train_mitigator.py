import pandas as pd
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer

def main():
    print("Loading synthetic dataset...")
    df = pd.read_csv("data/synthetic_bias_data.csv")
    
    # We only need biased_sentence and mitigated_sentence
    # df has: input_sentence, bias_score, is_biased, bias_type, mitigated_sentence
    df = df[["input_sentence", "bias_type", "mitigated_sentence"]]
    
    # Convert to HuggingFace dataset
    dataset = Dataset.from_pandas(df)
    
    # Let's split it into train and validation sets
    dataset = dataset.train_test_split(test_size=0.1, seed=42)
    train_dataset = dataset["train"]
    val_dataset = dataset["test"]

    print("Loading FLAN-T5-small model and tokenizer...")
    model_name = "google/flan-t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    # Determine device
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
        
    model = model.to(device)

    def preprocess_function(examples):
        # T5 expects a task prefix with bias type
        inputs = ["mitigate " + b_type + " bias: " + doc for b_type, doc in zip(examples["bias_type"], examples["input_sentence"])]
        targets = examples["mitigated_sentence"]
        model_inputs = tokenizer(inputs, text_target=targets, max_length=128, truncation=True, padding="max_length")

        return model_inputs

    print("Preprocessing datasets...")
    tokenized_train = train_dataset.map(preprocess_function, batched=True)
    tokenized_val = val_dataset.map(preprocess_function, batched=True)
    
    # Remove original columns to avoid un-collated types
    tokenized_train = tokenized_train.remove_columns(["input_sentence", "bias_type", "mitigated_sentence"])
    tokenized_val = tokenized_val.remove_columns(["input_sentence", "bias_type", "mitigated_sentence"])
    
    # Training arguments
    # Note: T5 might need more epochs for fine-tuning on a small dataset, but for demonstration we use 10
    training_args = Seq2SeqTrainingArguments(
        output_dir="./models/t5_mitigator_checkpoints",
        eval_strategy="epoch",
        learning_rate=2e-4,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        weight_decay=0.01,
        save_total_limit=1,
        num_train_epochs=10,
        predict_with_generate=True,
        fp16=False # disable fp16 for mps/cpu compatibility unless cuda
    )

    # Use DataCollator for Seq2Seq
    from transformers import DataCollatorForSeq2Seq
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    print("Initializing trainer...")
    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
        processing_class=tokenizer,
        data_collator=data_collator,
    )

    print("Starting training...")
    trainer.train()

    print("Saving the best model...")
    save_path = "./models/t5_mitigator"
    trainer.save_model(save_path)
    tokenizer.save_pretrained(save_path)
    print(f"Model saved fully to {save_path}")

if __name__ == "__main__":
    main()
