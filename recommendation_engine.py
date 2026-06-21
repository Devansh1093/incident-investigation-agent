from rca_engine import generate
def generate_recommendations():

    rca = generate()

    recommendations = []

    if "database connection issues" in rca["root_cause"]:
        recommendations.append(
            "Rollback deployment #140"
        )

    if "workflow failures" in rca["root_cause"]:
        recommendations.append(
            "Inspect failing build-and-test workflow"
        )

    recommendations.append(
        "Review recent PRs merged before deployment"
    )

    return recommendations