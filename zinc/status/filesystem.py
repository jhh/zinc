from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
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
