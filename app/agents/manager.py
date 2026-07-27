import json

from app.agents.worker import Worker


class Manager:

    def __init__(self):

        self.worker = Worker("manager")

    def decide(self, task: str):

        response = self.worker.run(task)

        # return json.loads(response)
        try:
            return json.loads(response)

        except json.JSONDecodeError:

            raise Exception(
                "Manager returned invalid JSON:\n\n"
                + response
            )