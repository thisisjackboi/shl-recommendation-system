import json
import os
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


# —— setup (run once) ——
with open("shl_assessments.json", encoding="utf-8") as f:
    assessments = json.load(f)

# Build BM25 index
docs = []
for a in assessments:
    parts = [a["name"]]
    if desc := a.get("description"):
        parts.append(desc)
    if tt := a.get("test_type"):
        parts += tt if isinstance(tt, list) else [tt]
    docs.append(" ".join(parts).lower())

tokenized = [doc.split() for doc in docs]
bm25 = BM25Okapi(tokenized)

# Initialize embedder
embed_model = SentenceTransformer("all-mpnet-base-v2")

def embed_texts(texts: list[str]) -> np.ndarray:
    return embed_model.encode(texts, convert_to_numpy=True, show_progress_bar=False)

def get_top_assessments(
    query: str,
    K: int = 20,
    N: int = 3,
    bm25_threshold: float = 0.0,
    sim_threshold: float = 0.10
):
    """
    Returns top-N assessments, or [] if the query doesn’t match JSON.
    """
    # 1) BM25 shortlist
    q_tokens = query.lower().split()
    bm25_scores = bm25.get_scores(q_tokens)
    # If no keyword overlap at all, return empty
    if max(bm25_scores) <= bm25_threshold:
        return []

    top_idx = np.argpartition(-bm25_scores, K)[:K]
    top_idx = top_idx[np.argsort(-bm25_scores[top_idx])]
    shortlist = [assessments[i] for i in top_idx]

    # 2) Embed
    query_emb = embed_texts([query])[0]
    cand_texts = [
        " ".join([c["name"]] + (c.get("test_type") or []))
        for c in shortlist
    ]
    cand_embs = embed_texts(cand_texts)

    # 3) Cosine-sim rerank
    sims = [
        float(np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb)))
        for emb in cand_embs
    ]
    # If even the best sim is too low, return empty
    if max(sims) < sim_threshold:
        return []

    # top-N by sim
    best_idx = np.argsort(sims)[-N:][::-1]

    # 5)results
    results = []
    for idx in best_idx:
        a = shortlist[idx]
        results.append({
            "name":           a["name"],
            "url":            a["url"],
            "relevance":      sims[idx],
            "duration":       a.get("duration"),
            "remote_testing": a.get("remote_testing", False),
            "adaptive_irt":   a.get("adaptive_irt", False),
            "test_type":      a.get("test_type", []),
        })
    return results

if __name__ == "__main__":
    print("🔍 SHL Assessment Recommender")
    print("Type a job description and hit enter. Type 'exit' to quit.\n")

    while True:
        query = input("Enter job description (or 'exit' to quit): ").strip()
        if query.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        recs = get_top_assessments(query, K=20, N=3)
        if not recs:
            print("No recommendations found.\n")
            continue

        print("\nTop recommendations:")
        for i, r in enumerate(recs, 1):
            print(f"{i}. {r['name']}  (score: {r['relevance']:.3f})")
            print(f"   URL: {r['url']}")
            if r["duration"] is not None:
                print(f"   Duration: {r['duration']} min")
            print(f"   Remote: {r['remote_testing']}, Adaptive: {r['adaptive_irt']}")
            print(f"   Types: {r['test_type']}\n")
        print("-" * 40 + "\n")

