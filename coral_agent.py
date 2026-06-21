import subprocess

from engine import investigate_incident


def run_coral_query(sql):
    result = subprocess.run(
        ["coral", "sql", sql],
        capture_output=True,
        text=True
    )

    return result.stdout


def get_recent_prs(owner, repo):

    sql = f"""
    SELECT
        number,
        title,
        state,
        created_at
    FROM github.pulls
    WHERE owner = '{owner}'
    AND repo = '{repo}'
    LIMIT 5
    """

    result = run_coral_query(sql)

    return parse_prs(result)


def get_workflows(owner, repo):

    sql = f"""
    SELECT
        id,
        name,
        state
    FROM github.workflows
    WHERE owner = '{owner}'
    AND repo = '{repo}'
    LIMIT 10
    """

    result = run_coral_query(sql)

    return parse_workflows(result)


def get_workflow_runs(owner, repo, workflow_id):

    sql = f"""
    SELECT
        status,
        conclusion,
        created_at
    FROM github.repo_action_workflow_runs
    WHERE owner = '{owner}'
    AND repo = '{repo}'
    AND workflow_id = {workflow_id}
    LIMIT 10
    """

    result = run_coral_query(sql)

    return parse_workflow_runs(result)


def investigate(owner, repo):

    incident_data = investigate_incident()

    prs = get_recent_prs(owner, repo)

    workflows = get_workflows(owner, repo)

    workflow_runs = []

    if workflows:

        workflow_id = workflows[0]["id"]

        workflow_runs = get_workflow_runs(
            owner,
            repo,
            workflow_id
        )

    return {
        "repository": f"{owner}/{repo}",
        "incident_context": incident_data,
        "recent_prs": prs,
        "workflows": workflows,
        "workflow_runs": workflow_runs
    }


def parse_prs(output):

    lines = output.splitlines()

    prs = []

    for line in lines:

        if "|" not in line:
            continue

        if "number" in line and "title" in line:
            continue

        if "---" in line:
            continue

        parts = [x.strip() for x in line.split("|") if x.strip()]

        if len(parts) >= 4:

            prs.append({
                "number": parts[0],
                "title": parts[1],
                "state": parts[2],
                "created_at": parts[3]
            })

    return prs


def parse_workflows(output):

    lines = output.splitlines()

    workflows = []

    for line in lines:

        if "|" not in line:
            continue

        if "id" in line and "name" in line:
            continue

        if "---" in line:
            continue

        parts = [x.strip() for x in line.split("|") if x.strip()]

        if len(parts) >= 3:

            workflows.append({
                "id": parts[0],
                "name": parts[1],
                "state": parts[2]
            })

    return workflows


def parse_workflow_runs(output):

    lines = output.splitlines()

    runs = []

    for line in lines:

        if "|" not in line:
            continue

        if "status" in line and "conclusion" in line:
            continue

        if "---" in line:
            continue

        parts = [x.strip() for x in line.split("|") if x.strip()]

        if len(parts) >= 3:

            runs.append({
                "status": parts[0],
                "conclusion": parts[1],
                "created_at": parts[2]
            })

    return runs