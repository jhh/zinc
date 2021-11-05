from dataclasses import dataclass
from datetime import datetime
from typing import Union
from dateutil.parser import isoparse


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
class FileSystem:
    """Class representing a replicated file system."""

    name: str
    state: str
    plan_error: Union[str, None]
    step_error: Union[str, None]
    current_step: int
    steps: list[Step]

    @staticmethod
    def from_dict(fs: dict) -> "FileSystem":
        return FileSystem(
            name=fs["Info"]["Name"],
            state=fs["State"],
            plan_error=fs["PlanError"],
            step_error=fs["StepError"],
            current_step=fs["CurrentStep"],
            steps=[Step.from_dict(s) for s in fs["Steps"]],
        )


@dataclass(frozen=True)
class Attempt:
    """Class representing a replication attempt."""

    state: str
    start_at: datetime
    finish_at: datetime
    file_systems: list[FileSystem]

    @staticmethod
    def from_dict(a: dict) -> "Attempt":
        return Attempt(
            state=a["State"],
            start_at=isoparse(a["StartAt"]),
            finish_at=isoparse(a["FinishAt"]),
            file_systems=[FileSystem.from_dict(fs) for fs in a["Filesystems"]],
        )


@dataclass(frozen=True)
class Replication:
    """Class representing attempt from replication stage of a push job."""

    start_at: datetime
    finish_at: datetime
    wait_reconnect_since: datetime
    wait_reconnect_until: datetime
    wait_reconnect_error: Union[str, None]
    attempts: list[Attempt]

    @staticmethod
    def from_dict(r: dict) -> "Replication":
        return Replication(
            start_at=isoparse(r["StartAt"]),
            finish_at=isoparse(r["FinishAt"]),
            wait_reconnect_since=isoparse(r["WaitReconnectSince"]),
            wait_reconnect_until=isoparse(r["WaitReconnectUntil"]),
            wait_reconnect_error=r["WaitReconnectError"],
            attempts=[Attempt.from_dict(a) for a in r["Attempts"]],
        )
