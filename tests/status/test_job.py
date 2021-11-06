from fixtures import *
from zinc.status.job import PushJob
from zinc.status.pruning import Pruning
from zinc.status.replication import Replication
from zinc.status.snapshotting import SnapShotting


def test_push_job(push_job_dict, repl_dict, pruning_dict, snapshotting_dict):
    push_job = PushJob.from_dict("backup", push_job_dict)
    assert push_job == PushJob(
        name="backup",
        replication=Replication.from_dict(repl_dict),
        pruning_sender=Pruning.from_dict(pruning_dict),
        pruning_receiver=Pruning.from_dict(pruning_dict),
        snapshotting=SnapShotting.from_dict(snapshotting_dict),
    )
