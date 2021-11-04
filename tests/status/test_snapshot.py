from zinc.status import SnapShot
from tests.status.fixtures import *


def test_snapshot(snapshot_dict, snapshot_name, snapshot_replicated, date):
    snapshot = SnapShot.from_dict(snapshot_dict)
    assert snapshot == SnapShot(
        name=snapshot_name,
        replicated=snapshot_replicated,
        date=date,
    )


