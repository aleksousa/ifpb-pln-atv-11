import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from llm import LLMAnalyzer


class Qwen3_4_Analyzer(LLMAnalyzer):
    def __init__(self):
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        self.model_name = "Qwen/Qwen3-4B-Instruct-2507"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=quantization_config,
            device_map="auto"
        )
        self.model.eval()

        print(f"Model device: {self.model.device}")

    def analyze(self, prompt):
        start_time = time.time()

        messages = [
            {"role": "user", "content": prompt}
        ]

        input_text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False
        )

        inputs = self.tokenizer(input_text, return_tensors="pt").to(self.model.device)
        input_token_count = inputs.input_ids.shape[1]

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=input_token_count,
                temperature=0.8,
                do_sample=True,
                top_k=20,
                top_p=0.95,
                min_p=0.05
            )

        output_ids = outputs[0][len(inputs.input_ids[0]):]
        content = self.tokenizer.decode(output_ids, skip_special_tokens=True)

        del output_ids
        del outputs
        del inputs
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

        total_time = time.time()
        print(f"  Total time: {total_time - start_time:.2f}s")

        return content

    def get_name(self):
        return "qwen3_4B"