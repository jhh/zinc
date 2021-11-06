import pytest
from datetime import datetime, timedelta
from flask import json


@pytest.fixture
def status_json():
    with open("tests/status.json", "r") as j:
        data = j.read()
    return data


@pytest.fixture
def state():
    return "done"


@pytest.fixture
def date():
    return datetime.utcnow()


@pytest.fixture
def date_json(date):
    return date.isoformat()


@pytest.fixture
def offset_date(date):
    return date + timedelta(minutes=1)


@pytest.fixture
def offset_date_json(offset_date):
    return offset_date.isoformat()


@pytest.fixture
def step_from_snapshot():
    return "@zrepl_20211101_214856_000"


@pytest.fixture
def step_to_snapshot():
    return "@zrepl_20211101_220356_000"


@pytest.fixture
def step_resumed():
    return False


@pytest.fixture
def step_encrypted():
    return False


@pytest.fixture
def step_encrypted_json(step_encrypted):
    return "yes" if step_encrypted else "no"


@pytest.fixture
def step_bytes_expected():
    return 1024


@pytest.fixture
def step_bytes_replicated():
    return 1024


@pytest.fixture
def step_json(
    step_from_snapshot,
    step_to_snapshot,
    step_resumed,
    step_encrypted_json,
    step_bytes_expected,
    step_bytes_replicated,
):
    return f"""
    {{
      "Info": {{
        "From": "{step_from_snapshot}",
        "To": "{step_to_snapshot}",
        "Resumed": {json.dumps(step_resumed)},
        "Encrypted": "{step_encrypted_json}",
        "BytesExpected": {step_bytes_expected},
        "BytesReplicated": {step_bytes_replicated}
      }}
    }}
    """


@pytest.fixture
def step_dict(step_json):
    return json.loads(step_json)


@pytest.fixture
def fs_name():
    return "rpool/safe/home/root"


@pytest.fixture
def fs_plan_error():
    return None


@pytest.fixture
def fs_step_error():
    return "error"


@pytest.fixture
def fs_current_step():
    return 1


@pytest.fixture
def fs_json(fs_name, state, fs_plan_error, fs_step_error, fs_current_step, step_json):
    return f"""
    {{
      "Info": {{
        "Name": "{fs_name}"
      }},
      "State": "{state}",
      "PlanError": {json.dumps(fs_plan_error)},
      "StepError": {json.dumps(fs_step_error)},
      "CurrentStep": {fs_current_step},
      "Steps": [ {step_json} ]
    }}
    """


@pytest.fixture
def repl_plan_error():
    return None


@pytest.fixture
def attempt_json(state, date_json, offset_date_json, repl_plan_error, fs_json):
    return f"""
    {{
      "State": "{state}",
      "StartAt": "{date_json}",
      "FinishAt": "{offset_date_json}",
      "PlanError": {json.dumps(repl_plan_error)},
      "Filesystems": [ {fs_json} ]
    }}
    """


@pytest.fixture
def attempt_dict(attempt_json):
    return json.loads(attempt_json)


@pytest.fixture
def repl_json(date_json, offset_date_json, attempt_json):
    return f"""
    {{
      "StartAt": "{date_json}",
      "FinishAt": "{offset_date_json}",
      "WaitReconnectSince": "{date_json}",
      "WaitReconnectUntil": "{date_json}",
      "WaitReconnectError": null,
      "Attempts": [ {attempt_json} ]
    }}
    """


@pytest.fixture
def repl_dict(repl_json):
    return json.loads(repl_json)


@pytest.fixture
def fs_dict(fs_json):
    return json.loads(fs_json)


@pytest.fixture
def snapshot_name():
    return "zrepl_20211018_204856_000"


@pytest.fixture
def prune_snapshot_replicated():
    return False


@pytest.fixture
def prune_snapshot_json(snapshot_name, prune_snapshot_replicated, date_json):
    return f"""
    {{
      "Name": "{snapshot_name}",
      "Replicated": {json.dumps(prune_snapshot_replicated)},
      "Date": "{date_json}"
    }}
    """


@pytest.fixture
def prune_snapshot_dict(prune_snapshot_json):
    return json.loads(prune_snapshot_json)


@pytest.fixture
def prune_skip_reason():
    return "because"


@pytest.fixture
def prune_last_error():
    return "error"


@pytest.fixture
def prune_attempt_json(
    fs_name, prune_snapshot_json, prune_skip_reason, prune_last_error
):
    return f"""
    {{
      "Filesystem": "{ fs_name }",
      "SnapshotList": [ { prune_snapshot_json } ],
      "DestroyList": [ { prune_snapshot_json } ],
      "SkipReason": "{ prune_skip_reason }",
      "LastError": "{ prune_last_error }"
    }}
    """


@pytest.fixture
def prune_attempt_dict(prune_attempt_json):
    return json.loads(prune_attempt_json)


@pytest.fixture
def pruning_json(state, prune_last_error, prune_attempt_json):
    return f"""
    {{
      "State": "{ state }",
      "Error": "{ prune_last_error }",
      "Pending": [{ prune_attempt_json }],
      "Completed": [{ prune_attempt_json }]
    }}
    """


@pytest.fixture
def pruning_dict(pruning_json):
    return json.loads(pruning_json)


@pytest.fixture
def snapshot_snapshot_state():
    return 4


@pytest.fixture
def had_error():
    return False


@pytest.fixture
def hooks():
    return "1 Ok 296ms snapshot"


@pytest.fixture
def snapshot_snapshot_json(
    fs_name,
    snapshot_snapshot_state,
    snapshot_name,
    date_json,
    offset_date_json,
    had_error,
    hooks,
):
    return f"""
    {{
      "Path": "{fs_name}",
      "State": {snapshot_snapshot_state},
      "SnapName": "{snapshot_name}",
      "StartAt": "{date_json}",
      "DoneAt": "{offset_date_json}",
      "HooksHadError": {json.dumps(had_error)},
      "Hooks": "{hooks}"
    }}
    """


@pytest.fixture
def snapshot_snapshot_dict(snapshot_snapshot_json):
    return json.loads(snapshot_snapshot_json)


@pytest.fixture
def snapshotting_error():
    return ""


@pytest.fixture
def snapshotting_json(
    snapshot_snapshot_state, date_json, snapshotting_error, snapshot_snapshot_json
):
    return f"""
    {{
      "State": {snapshot_snapshot_state},
      "SleepUntil": "{date_json}",
      "Error": "{snapshotting_error}",
      "Progress": [{snapshot_snapshot_json}]
    }}
    """

@pytest.fixture
def snapshotting_dict(snapshotting_json):
    return json.loads(snapshotting_json)
