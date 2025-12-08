import re
import gc
import torch

from evaluate import load
from typing import List, Dict

_bertscore_metric = None

def count_word_syllables(word):
    word = word.lower()
    word = re.sub(r'[^a-záéíóúàâêôãõç]', '', word)
    groups = re.findall(r'[aeiouáéíóúàâêôãõ]+', word)
    return max(1, len(groups))


def flesch_index(text):
    clean_text = re.sub(r'\n+', ' ', text.strip())
    sentences = re.split(r'[.!?]+', clean_text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return 0.0

    words = re.findall(r'\b[\wáéíóúàâêôãõç]+\b', clean_text.lower())

    if not words:
        return 0.0

    total_syllables = sum(count_word_syllables(w) for w in words)
    num_sentences = len(sentences)
    num_words = len(words)

    asl = num_words / num_sentences
    asw = total_syllables / num_words

    flesch = 248.835 - (1.015 * asl) - (84.6 * asw)

    return float(flesch)


def measure_bertscore_similarity(original_text: str, summarized_text: str) -> Dict[str, float]:
    global _bertscore_metric

    if _bertscore_metric is None:
        _bertscore_metric = load("bertscore")

    candidates: List[str] = [summarized_text]
    references: List[str] = [original_text]

    results = _bertscore_metric.compute(
        predictions=candidates,
        references=references,
        lang="pt"
    )

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return {
        "bert_f1": results["f1"][0],
        "bert_precision": results["precision"][0],
        "bert_recall": results["recall"][0]
    }


def measure_compression_ratio(original_text: str, summarized_text: str) -> float:
    count_words = lambda text: len([word for word in text.split() if word])

    original_length = count_words(original_text)
    summary_length = count_words(summarized_text)

    if original_length == 0:
        compression_ratio = 0.0
    else:
        compression_ratio = summary_length / original_length

    return compression_ratio

def cleanup_bertscore():
    global _bertscore_metric
    if _bertscore_metric is not None:
        del _bertscore_metric
        _bertscore_metric = None
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()