import json

def get_metrics_data():
    with open("data/metrics.json") as f:
        return json.load(f)
    

    