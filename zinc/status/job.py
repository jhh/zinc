from dataclasses import dataclass
from .replication import Replication


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class InternalJob(Job):
    """Class representing a zrepl internal job."""

    pass


@dataclass(frozen=True)
class PushJob(Job):
    """Class representing a zrepl push job."""

    replication_attempts: list[Replication]
