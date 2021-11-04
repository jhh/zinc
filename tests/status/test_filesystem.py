from zinc.status import FileSystem
from tests.status.fixtures import *


def test_filesystem(fs_dict, fs_name, state, fs_plan_error, fs_step_error):
    assert FileSystem.from_dict(fs_dict) == FileSystem(
        name=fs_name, state=state, plan_error=fs_plan_error, step_error=fs_step_error
    )


