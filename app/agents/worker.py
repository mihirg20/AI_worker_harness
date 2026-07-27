from pathlib import Path

from app.llm.delegate import ask


class Worker:

    def __init__(self, name: str):

        self.name = name

        self.prompt = Path(
            f"harness/agents/{name}.md"
        ).read_text(
            encoding="utf-8"
        )

    def run(self, task: str) -> str:

        return ask(
            system_prompt=self.prompt,
            user_prompt=task,
        )