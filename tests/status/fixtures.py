import pytest
from datetime import datetime, timedelta
from flask import json


@pytest.fixture
def status_json():
    with open("tests/status.json", "r") as j:
        data = j.read()
    return data


@pytest.fixture
def fs_name():
    return "rpool/safe/home/root"


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
def fs_plan_error():
    return None


@pytest.fixture
def fs_step_error():
    return "error"


@pytest.fixture
def fs_json(fs_name, state, fs_plan_error, fs_step_error, step_json):
    return f"""
    {{
      "Info": {{
        "Name": "{fs_name}"
      }},
      "State": "{state}",
      "PlanError": {json.dumps(fs_plan_error)},
      "StepError": {json.dumps(fs_step_error)},
      "CurrentStep": 1,
      "Steps": [ {step_json} ]
    }}
    """


@pytest.fixture
def repl_plan_error():
    return None


@pytest.fixture
def repl_json(state, date_json, offset_date_json, repl_plan_error, fs_json):
    return f"""
    {{
      "StartAt": "2021-11-01T18:03:56.157969708-04:00",
      "FinishAt": "0001-01-01T00:00:00Z",
      "WaitReconnectSince": "0001-01-01T00:00:00Z",
      "WaitReconnectUntil": "0001-01-01T00:00:00Z",
      "WaitReconnectError": null,
      "Attempts": [
        {{
          "State": "{state}",
          "StartAt": "{date_json}",
          "FinishAt": "{offset_date_json}",
          "PlanError": {json.dumps(repl_plan_error)},
          "Filesystems": [ {fs_json} ]
        }}
      ]
    }}
    """


@pytest.fixture
def repl_dict(repl_json):
    repl = json.loads(repl_json)
    # replication obj is really one of the attempts in the replication stage
    return repl["Attempts"][0]


@pytest.fixture
def fs_dict(fs_json):
    return json.loads(fs_json)


@pytest.fixture
def snapshot_name():
    return "zrepl_20211018_204856_000"


@pytest.fixture
def snapshot_replicated():
    return False


@pytest.fixture
def snapshot_json(snapshot_name, snapshot_replicated, date_json):
    return f"""
    {{
      "Name": "{snapshot_name}",
      "Replicated": {json.dumps(snapshot_replicated)},
      "Date": "{date_json}"
    }}
    """


@pytest.fixture
def snapshot_dict(snapshot_json):
    return json.loads(snapshot_json)
