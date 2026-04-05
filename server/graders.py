def easy_grader(state):
    return min(1.0, state["correct"] / max(1, state["processed"]))

def medium_grader(state):
    return min(1.0, state["correct"] / 3)

def hard_grader(state):
    return min(1.0, state["total_reward"] / 3)