# analysis.py
import pandas as pd
import matplotlib.pyplot as plt

def plot_drift(log_path="data/interaction_log.csv"):
    df = pd.read_csv(log_path)
    df['step'] = range(1, len(df)+1)
    plt.plot(df['step'], df['left_score'], label="Left leaning")
    plt.plot(df['step'], df['right_score'], label="Right leaning")
    plt.xlabel("Interaction step")
    plt.ylabel("Score")
    plt.title("Political Leaning Drift Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()
