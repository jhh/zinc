from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class PruningSender:
    """Class representing sender pruning stage of a push job."""

    state: str
    error: Union[str, None]

    pass


@dataclass(frozen=True)
class PruningReceiver:
    """Class representing receiver pruning stage of a push job."""

    pass
