from taskchampion import Replica, WorkingSet, Status, Operation
from pathlib import Path
import pytest
import uuid


@pytest.fixture
def working_set(tmp_path: Path):
    r = Replica(str(tmp_path), True)

    ops = []
    task, op = r.create_task(str(uuid.uuid4()))
    ops.extend(op)
    ops.extend(task.set_status(Status.Pending))

    task, op = r.create_task(str(uuid.uuid4()))
    ops.extend(op)
    ops.extend(task.set_status(Status.Pending))

    ops.extend(task.start())
    r.commit_operations(ops)

    return r.working_set()


def test_len(working_set: WorkingSet):
    assert len(working_set) == 2


def test_largest_index(working_set: WorkingSet):
    assert working_set.largest_index() == 2


def test_is_empty(working_set: WorkingSet):
    assert not working_set.is_empty()


def test_by_index(working_set: WorkingSet):
    assert working_set.by_index(1) is not None


@pytest.mark.skip()
def test_iter(working_set: WorkingSet):
    assert iter(working_set)


@pytest.mark.skip()
def test_next(working_set: WorkingSet):
    assert next(working_set)[0] == 1
    assert next(working_set)[0] == 2
    with pytest.raises(OSError):
        next(working_set)
