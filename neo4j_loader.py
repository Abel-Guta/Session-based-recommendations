from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import pickle

load_dotenv()

URI      = os.getenv("NEO4J_URI")
USER     = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


def build_graph(driver, sessions, session_batch_size=500):
    total = len(sessions)
    processed = 0

    for start in range(0, total, session_batch_size):
        chunk = sessions[start : start + session_batch_size]

        next_pairs = []
        cooc_pairs = []

        for session in chunk:
            items = [str(i) for i in session]

         
            for i in range(len(items) - 1):
                next_pairs.append({"a": items[i], "b": items[i+1]})

            unique = list(dict.fromkeys(items))
            for i in range(len(unique)):
                for j in range(i+1, len(unique)):
                    cooc_pairs.append({"a": unique[i], "b": unique[j]})

   
        with driver.session() as db:
            if next_pairs:
                db.run("""
                    UNWIND $pairs AS pair
                    MERGE (x:Item {id: pair.a})
                    MERGE (y:Item {id: pair.b})
                    MERGE (x)-[r:NEXT]->(y)
                      ON CREATE SET r.count = 1
                      ON MATCH  SET r.count = r.count + 1
                """, pairs=next_pairs)

            if cooc_pairs:
                db.run("""
                    UNWIND $pairs AS pair
                    MERGE (x:Item {id: pair.a})
                    MERGE (y:Item {id: pair.b})
                    MERGE (x)-[r:IN_SAME_SESSION]-(y)
                      ON CREATE SET r.count = 1
                      ON MATCH  SET r.count = r.count + 1
                """, pairs=cooc_pairs)

        processed += len(chunk)
        print(f"  Progress: {processed}/{total} sessions loaded...")

    print("Graph built successfully!")



CACHE_FILE = "data/sessions_cache.pkl"

if os.path.exists(CACHE_FILE):
    print("Loading sessions from cache (fast)...")
    with open(CACHE_FILE, "rb") as f:
        train_sessions = pickle.load(f)
else:
    print("First time: reading dataset (~3 min)...")
    from dataset import train_sessions
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(train_sessions, f)
    print("Saved to cache for next time!")


train_sessions = train_sessions[:5000]

with driver.session() as db:
    db.run("MATCH (n) DETACH DELETE n")
    print("Cleared old data.")

print(f"Loading {len(train_sessions)} sessions into Neo4j...")
build_graph(driver, train_sessions)
driver.close()