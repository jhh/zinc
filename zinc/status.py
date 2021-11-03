from dataclasses import dataclass
from datetime import datetime
from typing import Union
from flask import json
from dateutil.parser import isoparse


@dataclass
class FileSystem:
    """Class representing a replicated file system."""

    name: str
    state: str
    plan_error: Union[str, None]
    step_error: Union[str, None]

    @staticmethod
    def from_dict(fs: dict) -> "FileSystem":
        return FileSystem(
            name=fs["Info"]["Name"],
            state=fs["State"],
            plan_error=fs["PlanError"],
            step_error=fs["StepError"],
        )


@dataclass
class Replication:
    """Class representing attempt from replication stage of a push job."""

    state: str
    start_at: datetime
    finish_at: datetime
    plan_error: Union[str, None]
    file_systems: list[FileSystem]

    @staticmethod
    def from_dict(r: dict) -> "Replication":
        fs_list = [FileSystem.from_dict(fs) for fs in r["Filesystems"]]
        return Replication(
            state=r["State"],
            start_at=isoparse(r["StartAt"]),
            finish_at=isoparse(r["FinishAt"]),
            plan_error=r["PlanError"],
            file_systems=fs_list,
        )


@dataclass
class SnapShot:
    """Class representing a file system snap shot."""

    name: str
    replicated: bool
    date: datetime

    @staticmethod
    def from_dict(ss: dict) -> "SnapShot":
        return SnapShot(
            name=ss["Name"], replicated=ss["Replicated"], date=isoparse(ss["Date"])
        )


@dataclass
class PruningSender:
    """Class representing sender pruning stage of a push job."""

    pass


@dataclass
class PruningReceiver:
    """Class representing receiver pruning stage of a push job."""

    pass


@dataclass
class Job:
    """Class representing a zrepl job."""

    name: str

    @staticmethod
    def from_dict(name: str, job: dict) -> "Job":
        if "internal" == job["type"]:
            return InternalJob(name=name)
        if "push" == job["type"]:
            replication_attempts_list = job["push"]["Replication"]["Attempts"]
            replication_attempts = [
                Replication.from_dict(r_dict) for r_dict in replication_attempts_list
            ]
            return PushJob(name=name, replication_attempts=replication_attempts)
        else:
            raise NotImplementedError(f"unrecognized job type: {job['type']}")


@dataclass
class InternalJob(Job):
    """Class representing a zrepl internal job."""

    pass


@dataclass
class PushJob(Job):
    """Class representing a zrepl push job."""

    replication_attempts: list[Replication]


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
