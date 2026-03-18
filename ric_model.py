from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()
URI      = os.getenv("NEO4J_URI")
USER     = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

class RICRecommender:
    def __init__(self, alpha=0.3):
        self.alpha = alpha
        self.driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    def recommend(self, session, top_k=20):
        session = [str(i) for i in session]
        clicked = set(session)
        weights = {}

        with self.driver.session() as db:
            for clicked_item in session:

                result = db.run("""
                    MATCH (t:Item {id:$t})-[r:IN_SAME_SESSION]-(c:Item)
                    WITH c.id AS item, r.count AS cooc,
                         [(t)-[rx:IN_SAME_SESSION]-() | rx.count] AS all_counts
                    RETURN item, cooc, reduce(s=0, x IN all_counts | s+x) AS t_total
                """, t=clicked_item)

                for row in result:
                    candidate = row["item"]
                    t_total   = row["t_total"] or 1
                    co_prob   = row["cooc"] / t_total

                    old = weights.get(candidate, 0.0)
                    weights[candidate] = self.alpha * old + (1 - self.alpha) * co_prob

        
        sorted_items = sorted(
            [(item, w) for item, w in weights.items() if item not in clicked],
            key=lambda x: x[1], reverse=True
        )
        return [item for item, _ in sorted_items[:top_k]]

    def close(self):
        self.driver.close()
