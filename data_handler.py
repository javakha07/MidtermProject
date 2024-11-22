import os
import json
from datetime import datetime

if not os.path.exists("logs"):
    os.makedirs("logs")

LOG_FILE = "logs/game_logs.txt"
STATS_FILE = "logs/stats.json"

def save_logs(score, resources):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        with open(LOG_FILE, "a") as file:
            file.write(f"[{timestamp}] Score: {score}, Level: {resources['level']}\n")
        
        update_stats(score)
    except Exception as e:
        print(f"Error saving logs: {e}")

def update_stats(score):
    try:
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, "r") as f:
                stats = json.load(f)
        else:
            stats = {"high_score": 0, "games_played": 0, "total_score": 0}
        
        stats["games_played"] += 1
        stats["total_score"] += score
        stats["high_score"] = max(stats["high_score"], score)
        
        with open(STATS_FILE, "w") as f:
            json.dump(stats, f)
    except Exception as e:
        print(f"Error updating stats: {e}")

def view_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as file:
            logs = file.readlines()[-10:]  # Show last 10 games
        return logs
    return ["No logs available."]

def get_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            return json.load(f)
    return {"high_score": 0, "games_played": 0, "total_score": 0}
