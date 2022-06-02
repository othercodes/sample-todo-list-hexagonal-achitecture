from typing import Optional

from complexheart.domain.criteria import Criteria
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from to_do_list.tasks.domain.models import Task
from to_do_list.tasks.infrastructure.persistence.relational import RelationalTaskRepository, DBInstaller

db_engine: Optional[Engine] = None


def setup_function():
    global db_engine
    db_engine = create_engine('sqlite:///:memory:')
    DBInstaller(db_engine).install()


def test_repository_should_save_new_task_successfully(task_factory):
    session = sessionmaker(bind=db_engine)()

    repository = RelationalTaskRepository(session)
    task = repository.save(task_factory({}))

    assert session.query(Task).get(task.id)


def test_repository_should_find_task_successfully(task_factory):
    session = sessionmaker(bind=db_engine)()

    repository = RelationalTaskRepository(session)
    task = repository.save(task_factory({}))

    assert repository.find(task.id)


def test_repository_should_match_task_by_criteria_successfully(task_factory):
    session = sessionmaker(bind=db_engine)()

    repository = RelationalTaskRepository(session)

    for i in range(11):
        repository.save(task_factory({'description': 'My task {i}'.format(i=i)}))

    tasks = repository.match(
        Criteria() \
            .filter('description', 'like', '%task 1%') \
            .order_by(['id'])
    )

    for task in tasks:
        assert isinstance(task, Task)
    assert len(tasks) == 2


def test_repository_should_get_all_tasks_successfully(task_factory):
    session = sessionmaker(bind=db_engine)()

    repository = RelationalTaskRepository(session)

    for i in range(10):
        repository.save(task_factory({'description': 'My task {i}'.format(i=i)}))

    tasks = repository.all()

    for task in tasks:
        assert isinstance(task, Task)
    assert len(tasks) == 10
