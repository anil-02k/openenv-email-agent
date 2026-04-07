def easy_grader(state):
    processed = state.get("processed", 0)
    correct = state.get("correct", 0)
    if processed == 0:
        return 0.0
    return min(1.0, correct / processed)


def medium_grader(state):
    correct = state.get("correct", 0)
    return min(1.0, correct / 3)


def hard_grader(state):
    total_reward = state.get("total_reward", 0.0)
    return max(0.0, min(1.0, total_reward / 3))