import json

def get_slack_data():
    with open("data/slack.json") as f:
        return json.load(f)