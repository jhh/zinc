from dataclasses import dataclass
from datetime import datetime
from typing import Union
from dateutil.parser import isoparse

from .filesystem import FileSystem


@dataclass(frozen=True)
class Step:
    """Class representing a replication step."""

    from_snapshot: str
    to_snapshot: str
    resumed: bool
    bytes_expected: int
    bytes_replicated: int
    encrypted: bool = False

    @staticmethod
    def from_dict(step: dict) -> "Step":
        info = step["Info"]
        return Step(
            from_snapshot=info["From"],
            to_snapshot=info["To"],
            resumed=info["Resumed"],
            bytes_expected=info["BytesExpected"],
            bytes_replicated=info["BytesReplicated"],
        )


@dataclass(frozen=True)
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
