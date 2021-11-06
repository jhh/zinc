from zinc.status.pruning import Attempt, SnapShot, Pruning
from tests.status.fixtures import *


def test_snapshot(
    prune_snapshot_dict, snapshot_name, prune_snapshot_replicated, date
):
    snapshot = SnapShot.from_dict(prune_snapshot_dict)
    assert snapshot == SnapShot(
        name=snapshot_name,
        replicated=prune_snapshot_replicated,
        date=date,
    )


def test_attempt(
    prune_attempt_dict,
    fs_name,
    prune_skip_reason,
    prune_last_error,
    prune_snapshot_dict,
):
    attempt = Attempt.from_dict(prune_attempt_dict)
    assert attempt == Attempt(
        file_system=fs_name,
        skip_reason=prune_skip_reason,
        last_error=prune_last_error,
        snapshot_list=[SnapShot.from_dict(prune_snapshot_dict)],
        destroy_list=[SnapShot.from_dict(prune_snapshot_dict)],
    )


def test_pruning(pruning_dict, state, prune_last_error, prune_attempt_dict):
    pruning = Pruning.from_dict(pruning_dict)
    assert pruning == Pruning(
        state=state,
        error=prune_last_error,
        pending=[Attempt.from_dict(prune_attempt_dict)],
        completed=[Attempt.from_dict(prune_attempt_dict)],
    )
