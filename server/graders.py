def easy_grader(state):
    if state["processed"] == 0:
        return 0.0
    return min(1.0, state["correct"] / state["processed"])


def medium_grader(state):
    return min(1.0, state["correct"] / 3)


def hard_grader(state):
    return min(1.0, state["total_reward"] / 3)