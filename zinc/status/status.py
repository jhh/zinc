from dataclasses import dataclass
from flask import json
from .job import Job


@dataclass(frozen=True)
class Status:
    """Class representing zrepl status."""

    jobs: list[Job]

    @staticmethod
    def from_json(status_json: str) -> "Status":
        status = json.loads(status_json)
        jobs_dict = status["Jobs"]
        jobs = [Job.from_dict(name, jobs_dict[name]) for name in jobs_dict.keys()]
        return Status(jobs=jobs)
