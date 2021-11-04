from zinc.status import FileSystem, Replication
from zinc.status.replication import Step
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


def test_replication(repl_dict, state, date, offset_date, repl_plan_error, fs_dict):
    assert Replication.from_dict(repl_dict) == Replication(
        state=state,
        start_at=date,
        finish_at=offset_date,
        plan_error=repl_plan_error,
        file_systems=[FileSystem.from_dict(fs_dict)],
    )
