from typing import Optional

import pytest
from complexheart.domain.criteria import Criteria

from to_do_list.shared.domain.models import Collection
from to_do_list.tasks.application.services import TaskCreator, TaskFinder, TaskDeleter
from to_do_list.tasks.domain.exceptions import TaskNotFound, InvalidTaskDescription, InvalidTaskDueDate
from to_do_list.tasks.domain.models import Task


def test_task_creator_should_successfully_create_a_task(task_source_factory, task_repository_factory):
    def assert_on_save(task: Task) -> Task:
        assert task.id is None
        return Task(1, task.description, task.due_date, task.created)

    task_repository = task_repository_factory(on_save=assert_on_save)
    task_creator = TaskCreator(task_repository)
    source = task_source_factory({})

    task_creator.create(source)


def test_task_creator_should_raise_exception_on_invalid_task_description(task_source_factory, task_repository_factory):
    task_repository = task_repository_factory()
    source = task_source_factory({
        'description': 'a' * 256
    })

    with pytest.raises(InvalidTaskDescription):
        task_creator = TaskCreator(task_repository)
        task_creator.create(source)


def test_task_creator_should_raise_exception_on_invalid_task_due_date(task_source_factory, task_repository_factory):
    task_repository = task_repository_factory()
    source = task_source_factory({
        'due_date': '2022/12/01 00:00:00',
        'created': '2022/12/31 00:00:00'
    })

    with pytest.raises(InvalidTaskDueDate):
        task_creator = TaskCreator(task_repository)
        task_creator.create(source)


def test_task_finder_should_find_a_task_by_id(task_factory, task_repository_factory):
    def on_find(id: int) -> Optional[Task]:
        return task_factory({'id': id})

    task_repository = task_repository_factory(on_find=on_find)
    task_finder = TaskFinder(task_repository)

    task = task_finder.by_id(1)

    assert task.id == 1


def test_task_finder_should_raise_exception_on_task_not_found(task_repository_factory):
    with pytest.raises(TaskNotFound):
        task_repository = task_repository_factory(on_find=(lambda id: None))
        task_finder = TaskFinder(task_repository)

        task_finder.by_id(1)


def test_task_finder_should_match_tasks_by_criteria(task_repository_factory):
    task_repository = task_repository_factory(on_match=(lambda _: Collection([])))
    task_finder = TaskFinder(task_repository)

    criteria = Criteria()
    criteria.filter('due_date', '>', '2020-01-01 00:00:00')
    criteria.order_by(['description'], 'DESC')

    tasks = task_finder.by_criteria(criteria)

    assert len(tasks) == 0


def test_task_deleter_should_successfully_delete_a_task_by_id(task_repository_factory):
    def assert_on_delete(id: int) -> None:
        assert isinstance(id, int)

    task_repository = task_repository_factory(on_delete=assert_on_delete)
    task_deleter = TaskDeleter(task_repository)

    task_deleter.delete(1)
