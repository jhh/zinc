import pytest
from zinc.status import Status


@pytest.fixture
def status_json():
    with open("tests/status.json", "r") as j:
        data = j.read()
    return data


def test_init(status_json):
    status = Status.from_json(status_json)
    print(status)
