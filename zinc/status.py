from dataclasses import dataclass
from flask import json


@dataclass
class Job:
    """Class representing a zrepl job."""

    name: str

    @staticmethod
    def from_dict(name: str, job: dict) -> "Job":
        if "internal" == job["type"]:
            return InternalJob(name=name)
        if "push" == job["type"]:
            return PushJob(name=name)
        else:
            raise NotImplementedError(f"unrecognized job type: {job['type']}")



@dataclass
class InternalJob(Job):
    """Class representing a zrepl internal job."""
    pass


@dataclass
class PushJob(Job):
    """Class representing a zrepl push job."""

    pass


@dataclass
class Status:
    """Class representing zrepl status."""

    jobs: list[Job]

    @staticmethod
    def from_json(status_json: str) -> "Status":
        status = json.loads(status_json)
        jobs_dict = status["Jobs"]
        jobs = [Job.from_dict(name, jobs_dict[name]) for name in jobs_dict.keys()]
        return Status(jobs=jobs)


@dataclass
class Foo:
    def bar(self):
        status = Status.from_json()
