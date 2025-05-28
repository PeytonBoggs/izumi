import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_NAME = "arnir0/Tiny-LLM"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

def generate_text(prompt, model, tokenizer, max_length=512, temperature=1, top_k=50, top_p=0.95):
    inputs = tokenizer.encode(prompt, return_tensors="pt")

    outputs = model.generate(
        inputs,
        max_length=max_length,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        do_sample=True
    )


    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

prompt = "Tell me about quantum mechanics"

generated_text = generate_text(prompt, model, tokenizer)

print(generated_text)