import pytest
from fixtures import *
from zinc.status.job import PushJob, SnapJob
from zinc.status.status import Status


def test_status_complete():
    with open("tests/status/_data/status_complete.json", "r") as j:
        status_json = j.read()
    status = Status.from_json(status_json)
    assert status.jobs[0].name == "_control"
    assert status.jobs[1].name == "_prometheus"
    backups = status.jobs[2]
    assert isinstance(backups, PushJob)
    assert backups.name == "backups"


def test_status_inprogress():
    with open("tests/status/_data/status_inprogress.json", "r") as j:
        status_json = j.read()
    status = Status.from_json(status_json)
    assert status.jobs[0].name == "_control"
    assert status.jobs[1].name == "_prometheus"

    backups = status.jobs[2]
    assert isinstance(backups, PushJob)
    assert backups.name == "backups"

    time_machine = status.jobs[3]
    assert time_machine.name == "time_machine"
    assert isinstance(time_machine, SnapJob)

