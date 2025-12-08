import pandas as pd
import gc
import torch

from datetime import datetime
from prompts import prompt_strategies
from qwen4 import Qwen3_4_Analyzer
from qwen8 import Qwen3_8_Analyzer
from qwen14 import Qwen3_14_Analyzer
from metrics import measure_bertscore_similarity, measure_compression_ratio, flesch_index, cleanup_bertscore

if __name__ == "__main__":
    llm_configs = {
        "qwen3-4B": Qwen3_4_Analyzer,
        "qwen3-8B": Qwen3_8_Analyzer,
        "qwen3-14B": Qwen3_14_Analyzer,
    }

    df = pd.read_csv("corpus_orig.csv")

    df['flesch_original'] = df['text'].apply(
        lambda text: f"{flesch_index(text):.2f}".replace('.', ',')
    )

    for llm_name, llm_class in llm_configs.items():
        llm = llm_class()
        print(f"{llm_name} loaded\n")

        for prompt_name, prompt_template in prompt_strategies.items():
            column_base = f"{llm.get_name()}_{prompt_name}"
            print(f"\nProcessing: {prompt_name}")

            summaries = []
            flesch_scores = []
            bertscore_f1 = []
            compression_ratios = []

            for idx, original_text in enumerate(df['text'], 1):
                print(f"  Text {idx}/{len(df)}", end="... ")

                prompt = prompt_template(original_text)
                summary = llm.analyze(prompt)
                summaries.append(summary)

                flesch = flesch_index(summary)
                flesch_scores.append(f"{flesch:.2f}".replace('.', ','))

                bert_results = measure_bertscore_similarity(original_text, summary)
                bertscore_f1.append(f"{bert_results['bert_f1']:.3f}".replace('.', ','))

                comp_ratio = measure_compression_ratio(original_text, summary)
                compression_ratios.append(f"{comp_ratio:.3f}".replace('.', ','))

                gc.collect()
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()

            df[f"{column_base}_summary"] = summaries
            df[f"{column_base}_flesch"] = flesch_scores
            df[f"{column_base}_bert_f1"] = bertscore_f1
            df[f"{column_base}_compression_ratio"] = compression_ratios

        print(f"\nUnloading {llm_name}...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"result_corpus_{llm.get_name()}_{timestamp}.csv"
        df.to_csv(output_file, index=False)

        del llm
        cleanup_bertscore()
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()
        print(f"{llm_name} unloaded\n")

    cleanup_bertscore()

    final_output_file = "result_corpus_FINAL.csv"
    df.to_csv(final_output_file, index=False)

