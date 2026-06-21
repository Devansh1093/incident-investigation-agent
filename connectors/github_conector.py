import json

def get_github_data():
    with open("data/github.json") as f:
        return json.load(f)