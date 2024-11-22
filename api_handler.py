import requests
import json
import os

LEADERBOARD_FILE = "data/leaderboard.json"

def load_leaderboard():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump([], f)
    
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def save_leaderboard(scores):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(scores, f)

def add_score(player_name, score):
    scores = load_leaderboard()
    scores.append({"name": player_name, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]  # Keep only top 10
    save_leaderboard(scores)

def fetch_leaderboard():
    scores = load_leaderboard()
    return scores
