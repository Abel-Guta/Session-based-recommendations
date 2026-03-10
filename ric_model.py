
from collections import defaultdict

class RICRecommender:
    def __init__(self, alpha=0.3):
        self.alpha = alpha 
        self.co_occurrences = defaultdict(int)  
        self.single_counts = defaultdict(int)   
        self.total_sessions = 0
        self.all_items = set()


    def recommend(self, session, top_k=2):
        """
        Generates recommendations by updating weights click-by-click.
        """
        weights = {}
        
        for item in self.all_items:
            weights[item] = 0.0

      
        for current_item in session:
            for target_item in self.all_items:
                pair = tuple(sorted([current_item, target_item]))
                
                if self.co_occurrences[pair] > 0:
                    c_t = self.co_occurrences[pair] / self.single_counts[current_item]
                else:
                    c_t = self.single_counts[target_item] / self.total_sessions 

                weights[target_item] = (self.alpha * weights[target_item]) + ((1 - self.alpha) * c_t)

      
        sorted_items = [k for k, v in sorted(weights.items(), key=lambda x: x[1], reverse=True)]

        
        last_clicked = session[-1]
        
        if last_clicked in sorted_items:
            sorted_items.remove(last_clicked)
            sorted_items.append(last_clicked) 

        
        return sorted_items[:top_k]

    def train(self, sessions):
        """
        Loops through historical sessions to build the co-occurrence graph.
        """
        for session in sessions:
            self.total_sessions += 1
            
            
            unique_items = list(set(session))
            
            for i in range(len(unique_items)):
                item_A = unique_items[i]
                self.single_counts[item_A] += 1
                self.all_items.add(item_A)
                
                
                for j in range(i + 1, len(unique_items)):
                    item_B = unique_items[j]
                    
                    
                    pair = tuple(sorted([item_A, item_B]))
                    self.co_occurrences[pair] += 1
                    
        print("RIC Graph successfully built!")
        
