from fixtures import *
from zinc.status.snapshotting import SnapShot, SnapShotting


def test_snapshot(
    snapshot_snapshot_dict,
    fs_name,
    snapshot_snapshot_state,
    snapshot_name,
    date,
    offset_date,
    had_error,
    hooks,
):
    snapshot = SnapShot.from_dict(snapshot_snapshot_dict)
    assert snapshot == SnapShot(
        path=fs_name,
        state=snapshot_snapshot_state,
        snap_name=snapshot_name,
        start_at=date,
        done_at=offset_date,
        hooks=hooks,
        hooks_had_error=had_error,
    )


def test_snapshotting(
    snapshotting_dict,
    snapshot_snapshot_state,
    date,
    snapshotting_error,
    snapshot_snapshot_dict,
):
    snapshotting = SnapShotting.from_dict(snapshotting_dict)
    assert snapshotting == SnapShotting(
        state=snapshot_snapshot_state,
        sleep_until=date,
        error=snapshotting_error,
        progress=[SnapShot.from_dict(snapshot_snapshot_dict)],
    )
