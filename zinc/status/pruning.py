from dataclasses import dataclass
from datetime import datetime
from dateutil.parser import isoparse
from typing import List, Union


@dataclass(frozen=True)
class SnapShot:
    """Class representing a file system snap shot during pruning."""

    name: str
    replicated: bool
    date: datetime

    @staticmethod
    def from_dict(ss: dict) -> "SnapShot":
        return SnapShot(
            name=ss["Name"], replicated=ss["Replicated"], date=isoparse(ss["Date"])
        )


@dataclass(frozen=True)
class Attempt:
    """
    Class representing a pending or completed file system prune step within
    pruning phase.
    """

    file_system: str
    skip_reason: str
    last_error: Union[str, None]
    snapshot_list: List[SnapShot]
    destroy_list: List[SnapShot]

    @staticmethod
    def from_dict(a: dict) -> "Attempt":
        return Attempt(
            file_system=a["Filesystem"],
            skip_reason=a["SkipReason"],
            last_error=a["LastError"],
            snapshot_list=[SnapShot.from_dict(ss) for ss in a["SnapshotList"]],
            destroy_list=[SnapShot.from_dict(ss) for ss in a["DestroyList"]],
        )


@dataclass(frozen=True)
class Pruning:
    """Class representing pruning stage of a push job."""

    state: str
    error: Union[str, None]
    pending: List[Attempt]
    completed: List[Attempt]

    @staticmethod
    def from_dict(p: dict) -> "Pruning":
        return Pruning(
            state=p["State"],
            error=p["Error"],
            pending=[Attempt.from_dict(a) for a in p["Pending"]],
            completed=[Attempt.from_dict(a) for a in p["Completed"]],
        )
