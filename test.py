from connectors.github_conector import get_github_data
from connectors.logs_connector import get_logs_data
from connectors.slack_connector import get_slack_data
from connectors.metrics_connector import get_metrics_data

print(get_github_data())
print(get_metrics_data())
print(get_logs_data())
print(get_slack_data())
