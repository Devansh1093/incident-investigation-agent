from engine import investigate_incident
from coral_agent import get_workflow_runs


def generate_timeline():

    incident = investigate_incident()
    workflow_runs = get_workflow_runs()

    timeline = []

    timeline.append({
        "time": incident["deployment"]["deployment_time"],
        "event": f"Deployment {incident['deployment']['pr']} completed"
    })

    timeline.append({
        "time": "10:04",
        "event": f"CPU usage increased to {incident['metrics']['cpu']}%"
    })

    timeline.append({
        "time": "10:06",
        "event": incident["logs"]["error"]
    })

    if any(run["conclusion"] == "failure" for run in workflow_runs):
        timeline.append({
            "time": "10:08",
            "event": "GitHub workflow failures detected"
        })

    timeline.append({
        "time": "10:10",
        "event": "Incident alert triggered"
    })

    return timeline