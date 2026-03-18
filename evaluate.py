def recall_at_k(recommended, ground_truth, k):
    return 1 if str(ground_truth) in [str(x) for x in recommended[:k]] else 0

def mrr_at_k(recommended, ground_truth, k):
    top_k = [str(x) for x in recommended[:k]]
    if str(ground_truth) in top_k:
        rank = top_k.index(str(ground_truth)) + 1
        return 1.0 / rank
    return 0.0

def evaluate(model, test_sessions, k_values=[10, 20]):
    totals = {f"Recall@{k}": 0.0 for k in k_values}
    totals.update({f"MRR@{k}": 0.0 for k in k_values})
    count = 0

    for session in test_sessions:
        if len(session) < 2:
            continue
        input_session = session[:-1]  
        ground_truth  = session[-1]    

        recs = model.recommend(input_session, top_k=max(k_values))

        for k in k_values:
            totals[f"Recall@{k}"] += recall_at_k(recs, ground_truth, k)
            totals[f"MRR@{k}"]    += mrr_at_k(recs, ground_truth, k)
        count += 1

    return {metric: value/count for metric, value in totals.items()}
