import json

def get_logs_data():
    with open("data/logs.json") as f:
        return json.load(f)