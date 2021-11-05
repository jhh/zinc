from zinc.status import Replication
from zinc.status.replication import Attempt, FileSystem, Step
from tests.status.fixtures import *


def test_step(
    step_dict,
    step_from_snapshot,
    step_to_snapshot,
    step_resumed,
    step_bytes_expected,
    step_bytes_replicated,
):
    assert Step.from_dict(step_dict) == Step(
        from_snapshot=step_from_snapshot,
        to_snapshot=step_to_snapshot,
        resumed=step_resumed,
        bytes_expected=step_bytes_expected,
        bytes_replicated=step_bytes_replicated,
    )


def test_filesystem(
    fs_dict, fs_name, state, fs_plan_error, fs_step_error, fs_current_step, step_dict
):
    assert FileSystem.from_dict(fs_dict) == FileSystem(
        name=fs_name,
        state=state,
        plan_error=fs_plan_error,
        step_error=fs_step_error,
        current_step=fs_current_step,
        steps=[Step.from_dict(step_dict)],
    )


def test_attempt(attempt_dict, state, date, offset_date, fs_dict):
    assert Attempt.from_dict(attempt_dict) == Attempt(
        state=state,
        start_at=date,
        finish_at=offset_date,
        file_systems=[FileSystem.from_dict(fs_dict)],
    )


def test_replication(repl_dict, date, offset_date, attempt_dict):
    assert Replication.from_dict(repl_dict) == Replication(
        start_at=date,
        finish_at=offset_date,
        wait_reconnect_since=date,
        wait_reconnect_until=date,
        wait_reconnect_error=None,
        attempts=[Attempt.from_dict(attempt_dict)],
    )
