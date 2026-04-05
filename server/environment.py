from models import Observation, Action, Email


class EmailEnv:

    def __init__(self):
        self.max_steps = 10
        self.reset()

    def _generate_emails(self):
        return [
            Email(id=1, subject="Urgent: Payment Failed", body="Fix now", priority="high"),
            Email(id=2, subject="Meeting Tomorrow", body="Schedule", priority="medium"),
            Email(id=3, subject="Sale Offer", body="Buy now", priority="low"),
        ]

    def reset(self):
        self.emails = self._generate_emails()
        self.processed = 0
        self.correct = 0
        self.steps = 0
        self.total_reward = 0.0

        return self._get_obs()

    def step(self, action: Action):
        try:
            self.steps += 1
            reward = 0.0

            # find email
            email = None
            for e in self.emails:
                if e.id == action.email_id:
                    email = e
                    break

            if email is None:
                return self._get_obs(), -0.5, True, {}

            # classification
            if action.action_type == "classify":
                if email.priority == "high":
                    reward += 0.5
                    self.correct += 1
                else:
                    reward += 0.2

            # reply
            elif action.action_type == "reply":
                if action.response and len(action.response) > 20:
                    reward += 0.6
                    self.correct += 1
                else:
                    reward -= 0.3

            # ignore
            elif action.action_type == "ignore":
                if email.priority == "high":
                    reward -= 0.7
                else:
                    reward += 0.2

            # efficiency penalty
            reward -= 0.02

            self.total_reward += reward
            self.processed += 1

            done = self.steps >= self.max_steps

            return self._get_obs(), reward, done, {}

        except Exception as e:
            print("ERROR IN STEP:", str(e))
            return self._get_obs(), -1.0, True, {}

    def _get_obs(self):
        return Observation(
            emails=self.emails,
            processed=self.processed,
            correct=self.correct
        )

    def state(self):
        return {
            "steps": self.steps,
            "processed": self.processed,
            "total_reward": self.total_reward
        }