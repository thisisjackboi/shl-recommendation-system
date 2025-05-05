from typing import List, Tuple

def recall_at_k(predicted: List[str], relevant: List[str], k: int) -> float:
    """
    Recall@K = (# of relevant items in top-K) / (total relevant items)
    """
    if not relevant:
        return 0.0
    top_k = set(predicted[:k])
    return len(top_k.intersection(relevant)) / len(set(relevant))

def average_precision_at_k(predicted: List[str], relevant: List[str], k: int) -> float:
    """
    AP@K = (1 / min(K, R)) * sum_{i=1..K}( Precision@i * rel(i) )
    where rel(i)=1 if predicted[i] in relevant else 0.
    """
    if not relevant:
        return 0.0
    hits = 0
    score = 0.0
    for i, p in enumerate(predicted[:k], start=1):
        if p in relevant:
            hits += 1
            score += hits / i
    return score / min(len(relevant), k)

def evaluate(
    model_fn,                       
    test_set: List[Tuple[str, List[str]]],
    k: int = 3
) -> Tuple[float, float]:
    """
    Returns (mean_recall@k, mean_map@k) over the test set.
    """
    recalls = []
    aps = []
    for query, gt in test_set:
        preds = [r["name"] for r in model_fn(query, K=20, N=k)]
        recalls.append(recall_at_k(preds, gt, k))
        aps.append(average_precision_at_k(preds, gt, k))
    mean_recall = sum(recalls) / len(recalls)
    mean_ap     = sum(aps)     / len(aps)
    return mean_recall, mean_ap

if __name__ == "__main__":

    test_set = [
        (
            "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.",
            [
                "Automata - Fix (New)",
                "Core Java (Entry Level) (New)",
                "Java 8 (New)",
                "Core Java (Advanced Level) (New)",
                "Agile Software Development",
            ]
        ),
        (
            "I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options",
            [
                "Entry level Sales 7.1 (International)",
                "Entry Level Sales Sift Out 7.1",
                "Entry Level Sales Solution",
                "Sales Representative Solution",
                "Sales Support Specialist Solution",
                "Technical Sales Associate Solution",
                "SVAR - Spoken English (Indian Accent) (New)",
                "Sales & Service Phone Solution",
                "Sales & Service Phone Simulation",
                "English Comprehension (New)",
            ]
        ),

    ]


    from recommender import get_top_assessments


    mean_rec, mean_map = evaluate(get_top_assessments, test_set, k=3)

    print(f"Mean Recall@3: {mean_rec:.3f}")
    print(f"Mean MAP@3:    {mean_map:.3f}")
