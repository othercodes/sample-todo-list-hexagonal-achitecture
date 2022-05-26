from complexheart.domain.criteria import Criteria

from to_do_list.shared.domain.models import Collection
from to_do_list.tasks.domain.contracts import TaskRepository, TaskSource
from to_do_list.tasks.domain.exceptions import TaskNotFound
from to_do_list.tasks.domain.models import Task
from to_do_list.tasks.domain.services import build_task


class TaskCreator:
    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository

    def create(self, source: TaskSource) -> Task:
        task = build_task(source)

        self._task_repository.save(task)

        return task


class TaskFinder:
    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository

    def all(self) -> Collection[Task]:
        return self._task_repository.all()

    def by_id(self, id: int) -> Task:
        task = self._task_repository.find(id)
        if task is None:
            raise TaskNotFound("Task with id {id} not found".format(
                id=id
            ))

        return task

    def by_criteria(self, criteria: Criteria) -> Collection[Task]:
        return self._task_repository.match(criteria)


class TaskDeleter:
    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository

    def delete(self, id: int):
        self._task_repository.delete(id)
