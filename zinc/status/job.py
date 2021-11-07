from dataclasses import dataclass
from typing import Union

from .pruning import Pruning
from .snapshotting import SnapShotting
from .replication import Replication


@dataclass(frozen=True)
class Job:
    """Class representing a zrepl job."""

    name: str

    @staticmethod
    def from_dict(name: str, job: dict) -> "Job":
        job_type = job["type"]

        if "push" == job_type:
            push = job["push"]
            return PushJob(
                name=name,
                replication=Replication.from_dict(push["Replication"]),
                pruning_sender=Pruning.from_dict(push["PruningSender"]),
                pruning_receiver=Pruning.from_dict(push["PruningReceiver"]),
                snapshotting=SnapShotting.from_dict(push["Snapshotting"]),
            )

        if "snap" == job_type:
            snap = job["snap"]
            return SnapJob(
                name=name,
                pruning=Pruning.from_dict(snap["Pruning"]),
                snapshotting=SnapShotting.from_dict(snap["Snapshotting"]),
            )

        if "internal" == job_type:
            return InternalJob(name=name)

        raise NotImplementedError(f"unrecognized job type: {job_type}")


@dataclass(frozen=True)
class PushJob(Job):
    """Class representing a zrepl push job."""

    replication: Union[Replication, None]
    pruning_sender: Union[Pruning, None]
    pruning_receiver: Union[Pruning, None]
    snapshotting: Union[SnapShotting, None]


@dataclass(frozen=True)
class SnapJob(Job):
    """Class representing a zrepl snapshot job."""

    pruning: Union[Pruning, None]
    snapshotting: Union[SnapShotting, None]


@dataclass(frozen=True)
class InternalJob(Job):
    """Class representing a zrepl internal job."""

    pass
