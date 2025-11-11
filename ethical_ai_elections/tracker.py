# tracker.py
import pandas as pd
import os
from datetime import datetime

class UserTracker:
    def __init__(self, log_path="data/interaction_log.csv"):
        self.log_path = log_path
        self.left_score = 0.5
        self.right_score = 0.5

        if not os.path.exists(os.path.dirname(log_path)):
            os.makedirs(os.path.dirname(log_path))
        
        if not os.path.exists(log_path):
            pd.DataFrame(columns=['timestamp','headline','article_bias','action','left_score','right_score']).to_csv(log_path, index=False)
    
    def update_profile(self, bias, action):
        delta = 0.08 if action == 'read' else 0.15
        if bias == 'left':
            self.left_score += delta
        elif bias == 'right':
            self.right_score += delta
        # Normalize
        total = self.left_score + self.right_score
        self.left_score /= total
        self.right_score /= total

    def log_interaction(self, headline, bias, action):
        self.update_profile(bias, action)
        new_entry = {
            'timestamp': datetime.now().isoformat(),
            'headline': headline,
            'article_bias': bias,
            'action': action,
            'left_score': self.left_score,
            'right_score': self.right_score
        }
        df = pd.DataFrame([new_entry])
        df.to_csv(self.log_path, mode='a', header=False, index=False)
