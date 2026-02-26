# ILINA Technical Track Code Sample
# Project: Prompt Sensitivity & Evaluation Robustness Framework

import random
import numpy as np
from typing import List, Dict
from dataclasses import dataclass
import json

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

@dataclass
class Example:
    base_prompt: str
    label: int

def model_predict(prompt: str) -> int:
    base_score = sum(ord(c) for c in prompt) % 2
    noise = random.random()
    if noise < 0.1:
        return 1 - base_score
    return base_score

def generate_variants(prompt: str) -> List[str]:
    return [
        prompt,
        prompt + " Please answer clearly.",
        "In your view, " + prompt.lower(),
        prompt.replace("Is", "Would you say"),
        prompt + " Be precise.",
    ]

def compute_stability(predictions: List[int]) -> float:
    most_common = max(set(predictions), key=predictions.count)
    return predictions.count(most_common) / len(predictions)

def run_experiment(dataset: List[Example]) -> Dict:
    results = []
    stability_scores = []
    for example in dataset:
        variants = generate_variants(example.base_prompt)
        preds = [model_predict(p) for p in variants]
        stability = compute_stability(preds)
        stability_scores.append(stability)
        results.append({
            "prompt": example.base_prompt,
            "predictions": preds,
            "stability": stability
        })
    overall_stability = float(np.mean(stability_scores))
    return {
        "overall_stability": overall_stability,
        "detailed_results": results
    }

dataset = [
    Example("Is this text about economics?", 1),
    Example("Is this sentence discussing sports?", 0),
    Example("Is the topic related to politics?", 1),
    Example("Is this about cooking recipes?", 0),
]

if __name__ == "__main__":
    output = run_experiment(dataset)
    print("Overall Stability Score:", output["overall_stability"])
    with open("evaluation_results.json", "w") as f:
        json.dump(output, f, indent=4)
