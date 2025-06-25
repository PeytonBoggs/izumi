from langchain_huggingface import HuggingFacePipeline
import torch

llm = HuggingFacePipeline.from_model_id(
    model_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    device_map="cpu",
    model_kwargs={
        "torch_dtype": torch.bfloat16,
        "low_cpu_mem_usage": True,
        "max_memory": {0: "20GB", "cpu": "64GB"}
    }
)

result = llm.invoke("Give me current baseball standings")

print(result)