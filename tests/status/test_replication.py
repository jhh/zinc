from zinc.status import FileSystem, Replication
from tests.status.fixtures import *

def test_replication(repl_dict, state, date, offset_date, repl_plan_error, fs_dict):
    assert Replication.from_dict(repl_dict) == Replication(
        state=state,
        start_at=date,
        finish_at=offset_date,
        plan_error=repl_plan_error,
        file_systems=[FileSystem.from_dict(fs_dict)],
    )
