from server.graders import easy_grader, medium_grader, hard_grader

TASKS = [
    {
        "name": "easy",
        "description": "Classify email priorities",
        "grader": easy_grader
    },
    {
        "name": "medium",
        "description": "Generate meaningful responses",
        "grader": medium_grader
    },
    {
        "name": "hard",
        "description": "Optimize full inbox handling",
        "grader": hard_grader
    }
]