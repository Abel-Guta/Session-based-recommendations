# main.py
from dataset import training_sessions, active_user_session
from hsp_model import HSPRecommender
from ric_model import RICRecommender

print("--- TRAINING MODELS ---")

hsp = HSPRecommender()
hsp.train(training_sessions)


ric = RICRecommender(alpha=0.3)
ric.train(training_sessions)

print(f"\ncurrent session: {active_user_session}")


hsp_recs = hsp.recommend(active_user_session, top_k=2)
print(f"HSP Recommends:    {hsp_recs}")


ric_recs = ric.recommend(active_user_session, top_k=2)
print(f"RIC Recommends: {ric_recs}")