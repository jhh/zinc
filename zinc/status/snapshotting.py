from dataclasses import dataclass
from datetime import datetime
from typing import List, Union
from dateutil.parser import isoparse


@dataclass(frozen=True)
class SnapShot:
    """Class representing a snapshot scheduled during snapshotting stage."""

    path: str
    state: int
    snap_name: str
    start_at: datetime
    done_at: datetime
    hooks: str
    hooks_had_error: bool

    @staticmethod
    def from_dict(ss: dict) -> "SnapShot":
        return SnapShot(
            path=ss["Path"],
            state=ss["State"],
            snap_name=ss["SnapName"],
            start_at=isoparse(ss["StartAt"]),
            done_at=isoparse(ss["DoneAt"]),
            hooks=ss["Hooks"],
            hooks_had_error=ss["HooksHadError"],
        )


@dataclass(frozen=True)
class SnapShotting:
    """Class representing snapshotting stage of a job."""

    state: int
    sleep_until: datetime
    error: Union[str, None]
    progress: List[SnapShot]

    @staticmethod
    def from_dict(ss: dict) -> "SnapShotting":
        return SnapShotting(
            state=ss["State"],
            sleep_until=isoparse(ss["SleepUntil"]),
            error=ss["Error"],
            progress=[SnapShot.from_dict(p) for p in ss["Progress"]],
        )
