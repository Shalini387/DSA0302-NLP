from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "Helsinki-NLP/opus-mt-en-fr"

print("======================================")
print("     ENGLISH TO FRENCH TRANSLATOR")
print("======================================")

print("\nLoading translation model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

print("Model loaded successfully.")

text = input("\nEnter English text: ")

if not text.strip():
    print("Error: Text cannot be empty.")
else:
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    translated_tokens = model.generate(
        **inputs,
        max_length=100
    )

    translation = tokenizer.decode(
        translated_tokens[0],
        skip_special_tokens=True
    )

    print("\n======================================")
    print("           TRANSLATION")
    print("======================================")
    print("English :", text)
    print("French  :", translation)
    print("======================================")