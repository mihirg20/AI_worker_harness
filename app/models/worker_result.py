from dataclasses import dataclass


@dataclass
class WorkerResult:
    worker: str
    response: str