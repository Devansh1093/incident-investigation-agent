from connectors.github_conector import get_github_data
from connectors.metrics_connector import get_metrics_data
from connectors.logs_connector import get_logs_data
from connectors.slack_connector import get_slack_data


def investigate_incident():

    github = get_github_data()
    metrics = get_metrics_data()
    logs = get_logs_data()
    slack = get_slack_data()

    report = {
        "deployment": github,
        "metrics": metrics,
        "logs": logs,
        "discussion": slack
    }

    return report