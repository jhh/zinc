from dataclasses import dataclass
from datetime import datetime
from dateutil.parser import isoparse
from typing import Union

from .filesystem import FileSystem


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class FileSystemSnapShotSet:
    """Class representing a file system and associated snapshots."""

    file_system: "FileSystem"
    skip_reason: str
    last_error: Union[str, None]
    snapshot_list: list["SnapShot"]
    destroy_list: list["SnapShot"]
