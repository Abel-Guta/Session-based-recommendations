
from collections import defaultdict

class HSPRecommender:
    def __init__(self):
        
        self.single_counts = defaultdict(int)     
        self.pair_counts = defaultdict(int)       
        self.triplet_counts = defaultdict(int)     
        self.total_item_clicks = 0
    def recommend(self, session, top_k=2):
        """
        Generates recommendations using the Triplets -> Pairs -> Singles hierarchy.
        """
        recommendations = []
        
        def add_to_recs(sorted_candidates):
            for item in sorted_candidates:
                if item not in recommendations:
                    recommendations.append(item)
                if len(recommendations) >= top_k:
                    return True 
            return False

        
        if len(session) >= 2:
            item_A, item_B = session[-2], session[-1]
            candidates = {}
            for (a, b, c), count in self.triplet_counts.items():
                if a == item_A and b == item_B:
                   
                    candidates[c] = count / self.pair_counts[(a, b)]
            
            
            sorted_items = [k for k, v in sorted(candidates.items(), key=lambda x: x[1], reverse=True)]
            if add_to_recs(sorted_items): return recommendations

      
        if len(session) >= 1:
            item_A = session[-1]
            candidates = {}
            for (a, b), count in self.pair_counts.items():
                if a == item_A:
                    
                    candidates[b] = count / self.single_counts[a]
                    
            sorted_items = [k for k, v in sorted(candidates.items(), key=lambda x: x[1], reverse=True)]
            if add_to_recs(sorted_items): return recommendations

        
        candidates = {}
        for a, count in self.single_counts.items():
           
            candidates[a] = count / self.total_item_clicks
            
        sorted_items = [k for k, v in sorted(candidates.items(), key=lambda x: x[1], reverse=True)]
        add_to_recs(sorted_items)
        
        return recommendations

    def train(self, sessions):
        """
        Loops through historical sessions to build the sequence graph.
        """
        for session in sessions:
            for i in range(len(session)):
                item = session[i]
                self.single_counts[item] += 1
                self.total_item_clicks += 1
                if i < len(session) - 1:
                    pair = (session[i], session[i+1])
                    self.pair_counts[pair] += 1
                if i < len(session) - 2:
                    triplet = (session[i], session[i+1], session[i+2])
                    self.triplet_counts[triplet] += 1
                    
    

   