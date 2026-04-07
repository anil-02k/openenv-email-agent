from server.graders import easy_grader, medium_grader, hard_grader

TASKS = [
    {
        "name": "easy",
        "description": "Classify email priority correctly",
        "grader": easy_grader
    },
    {
        "name": "medium",
        "description": "Generate meaningful replies",
        "grader": medium_grader
    },
    {
        "name": "hard",
        "description": "Maximize total reward",
        "grader": hard_grader
    }
]