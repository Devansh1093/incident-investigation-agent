from engine import investigate_incident
from coral_agent import get_workflow_runs


def generate(owner,repo):

    data = investigate_incident()

    github = data["deployment"]
    metrics = data["metrics"]
    logs = data["logs"]
    slack = data["discussion"]

    workflow_runs = get_workflow_runs()

    root_cause = "Unknown"

    
    if "Database timeout" in logs["error"]:
        root_cause = (
            f"Deployment {github['pr']} likely introduced "
            f"database connection issues causing request failures."
        )

    
    
    workflow_failures = any(
    run["conclusion"] == "failure"
    for run in workflow_runs
)

    if workflow_failures:
       root_cause += " GitHub workflow failures detected."

    elif "action_required" in workflow_runs:
        root_cause += (
            " GitHub Actions requires manual intervention."
        )

    return {
        "root_cause": root_cause,
        "evidence": {
            "deployment": github,
            "metrics": metrics,
            "logs": logs,
            "discussion": slack,
            "workflow_runs": workflow_runs
        }
    }