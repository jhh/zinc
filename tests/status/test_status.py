from fixtures import *
from zinc.status.job import PushJob, SnapJob
from zinc.status.pruning import Pruning
from zinc.status.replication import Replication
from zinc.status.snapshotting import SnapShotting
from zinc.status.status import Status


def test_status_none():
    with open("tests/status/_data/status_none.json", "r") as j:
        status_json = j.read()
    status = Status.from_json(status_json)
    assert status.jobs[0].name == "_control"
    assert status.jobs[1].name == "_prometheus"
    backups = status.jobs[2]
    assert backups.name == "backups"
    assert isinstance(backups, PushJob)
    assert backups.replication is None
    assert backups.pruning_sender is None
    assert backups.pruning_receiver is None
    assert isinstance(backups.snapshotting, SnapShotting)
    assert len(backups.snapshotting.progress) == 0


def test_status_complete():
    with open("tests/status/_data/status_complete.json", "r") as j:
        status_json = j.read()
    status = Status.from_json(status_json)
    assert status.jobs[0].name == "_control"
    assert status.jobs[1].name == "_prometheus"
    backups = status.jobs[2]
    assert backups.name == "backups"
    assert isinstance(backups, PushJob)
    assert isinstance(backups.replication, Replication)
    assert isinstance(backups.pruning_sender, Pruning)
    assert isinstance(backups.pruning_receiver, Pruning)
    assert isinstance(backups.snapshotting, SnapShotting)


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

