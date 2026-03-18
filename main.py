import pickle
import os
from hsp_model import HSPRecommender
from ric_model  import RICRecommender
from evaluate   import evaluate


CACHE_FILE = "data/sessions_cache.pkl"
print("Loading sessions from cache...")
with open(CACHE_FILE, "rb") as f:
    all_sessions = pickle.load(f)

split = int(len(all_sessions) * 0.8)
test_sessions = all_sessions[split:]


test_sessions = test_sessions[:200]
print(f"Evaluating on {len(test_sessions)} test sessions...\n")


PAPER = {
    "Recall@10": 0.5693, "MRR@10": 0.2755,
    "Recall@20": 0.6559, "MRR@20": 0.2815,
}


print("Running HSP evaluation...")
hsp = HSPRecommender()
hsp_results = evaluate(hsp, test_sessions, k_values=[10, 20])
hsp.close()


print("Running RIC evaluation...")
ric = RICRecommender(alpha=0.3)
ric_results = evaluate(ric, test_sessions, k_values=[10, 20])
ric.close()

print("\n" + "="*55)
print(f"  {'Model':<12} {'Recall@10':>9} {'MRR@10':>8} {'Recall@20':>10} {'MRR@20':>8}")
print("  " + "-"*51)
for name, res in [("HSP (here)", hsp_results), ("RIC (here)", ric_results)]:
    print(f"  {name:<12} {res['Recall@10']:>9.4f} {res['MRR@10']:>8.4f} "
          f"{res['Recall@20']:>10.4f} {res['MRR@20']:>8.4f}")
print("  " + "-"*51)
print(f"  {'RIC (paper)':<12} {PAPER['Recall@10']:>9.4f} {PAPER['MRR@10']:>8.4f} "
      f"{PAPER['Recall@20']:>10.4f} {PAPER['MRR@20']:>8.4f}")
print("="*55)
    