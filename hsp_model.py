from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()
URI      = os.getenv("NEO4J_URI")
USER     = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

class HSPRecommender:
    def __init__(self):
        self.driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    def recommend(self, session, top_k=20):
        session = [str(i) for i in session]
        recs = []

        def add(candidates):
            for item in candidates:
                if item not in recs and item not in session:
                    recs.append(item)
                if len(recs) >= top_k:
                    return True
            return False

        with self.driver.session() as db:


            if len(session) >= 2:
                a, b = session[-2], session[-1]
                result = db.run("""
                    MATCH (a:Item {id:$a})-[ab:NEXT]->(b:Item {id:$b})-[r:NEXT]->(c:Item)
                    RETURN c.id AS item, toFloat(r.count)/toFloat(ab.count) AS prob
                    ORDER BY prob DESC LIMIT $k
                """, a=a, b=b, k=top_k*2)
                if add([row["item"] for row in result]): return recs


            if len(session) >= 1:
                b = session[-1]
                result = db.run("""
                    MATCH (b:Item {id:$b})-[r:NEXT]->(c:Item)
                    RETURN c.id AS item, r.count AS cnt
                    ORDER BY cnt DESC LIMIT $k
                """, b=b, k=top_k*2)
                if add([row["item"] for row in result]): return recs

            result = db.run("""
                MATCH (i:Item)-[r:NEXT]->()
                WITH i.id AS item, sum(r.count) AS total
                ORDER BY total DESC LIMIT $k
                RETURN item
            """, k=top_k*2)
            add([row["item"] for row in result])

        return recs

    def close(self):
        self.driver.close()
