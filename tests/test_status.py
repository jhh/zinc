from datetime import datetime, timedelta
import pytest
from zinc.status import FileSystem, SnapShot, Replication
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
def fs_plan_error():
    return None


@pytest.fixture
def fs_step_error():
    return "error"


@pytest.fixture
def fs_json(fs_name, state, fs_plan_error, fs_step_error):
    return f"""
    {{
      "Info": {{
        "Name": "{fs_name}"
      }},
      "State": "{state}",
      "PlanError": {json.dumps(fs_plan_error)},
      "StepError": {json.dumps(fs_step_error)},
      "CurrentStep": 1,
      "Steps": [
        {{
          "Info": {{
            "From": "@zrepl_20211101_214856_000",
            "To": "@zrepl_20211101_220356_000",
            "Resumed": false,
            "Encrypted": "no",
            "BytesExpected": 624,
            "BytesReplicated": 624
          }}
        }}
      ]
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


def test_filesystem(fs_dict, fs_name, state, fs_plan_error, fs_step_error):
    assert FileSystem.from_dict(fs_dict) == FileSystem(
        name=fs_name, state=state, plan_error=fs_plan_error, step_error=fs_step_error
    )


def test_snapshot(snapshot_dict, snapshot_name, snapshot_replicated, date):
    snapshot = SnapShot.from_dict(snapshot_dict)
    assert snapshot == SnapShot(
        name=snapshot_name,
        replicated=snapshot_replicated,
        date=date,
    )


def test_replication(repl_dict, state, date, offset_date, repl_plan_error, fs_dict):
    assert Replication.from_dict(repl_dict) == Replication(
        state=state,
        start_at=date,
        finish_at=offset_date,
        plan_error=repl_plan_error,
        file_systems=[FileSystem.from_dict(fs_dict)],
    )
