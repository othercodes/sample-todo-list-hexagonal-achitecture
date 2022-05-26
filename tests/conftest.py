from datetime import timezone
from typing import Optional, Callable

import pytest
from complexheart.domain.criteria import Criteria

from to_do_list.shared.domain.models import Collection
from to_do_list.tasks.domain.contracts import TaskSource, TaskRepository
from faker import Faker

from to_do_list.tasks.domain.models import Task
from to_do_list.tasks.domain.services import build_task

fake = Faker()


@pytest.fixture
def task_source_factory():
    class __Source(TaskSource):
        def __init__(self, data: Optional[dict] = None):
            self._data = {} if data is None else data

        def id(self) -> Optional[str]:
            return self._data.get('id')

        def description(self) -> str:
            return self._data.get('description', fake.sentence(
                nb_words=10
            ))

        def due_date(self) -> str:
            return self._data.get('due_date', fake.future_datetime(
                end_date='+2d',
                tzinfo=timezone.utc
            ).strftime('%Y/%m/%d %H:%M:%S'))

        def created(self) -> Optional[str]:
            return self._data.get('created', fake.past_datetime(
                start_date='-2d',
                tzinfo=timezone.utc
            ).strftime('%Y/%m/%d %H:%M:%S'))

    def __(data: dict) -> TaskSource:
        return __Source(data)

    return __


@pytest.fixture
def task_factory(task_source_factory):
    def __(data: dict) -> Task:
        return build_task(task_source_factory(data))

    return __


@pytest.fixture
def task_repository_factory():
    class _Repository(TaskRepository):
        def __init__(
                self,
                on_all: Optional[Callable[[], Collection[Task]]] = None,
                on_find: Optional[Callable[[int], Optional[Task]]] = None,
                on_save: Optional[Callable[[Task], Task]] = None,
                on_match: Optional[Callable[[Criteria], Collection[Task]]] = None,
                on_delete: Optional[Callable[[int], None]] = None,
        ):
            self._on_all = on_all or (lambda: Collection([]))
            self._on_find = on_find or (lambda _: None)
            self._on_save = on_save or (lambda _: _)
            self._on_match = on_match or (lambda _: Collection([]))
            self._on_delete = on_delete or (lambda _: None)

        def all(self) -> Collection[Task]:
            return self._on_all()

        def find(self, id: int) -> Optional[Task]:
            return self._on_find(id)

        def save(self, task: Task) -> Task:
            return self._on_save(task)

        def match(self, criteria: Criteria) -> Collection[Task]:
            return self._on_match(criteria)

        def delete(self, id: int) -> None:
            self._on_delete(id)

    def __(
            on_all: Optional[Callable[[], Collection[Task]]] = None,
            on_find: Optional[Callable[[int], Optional[Task]]] = None,
            on_save: Optional[Callable[[Task], Task]] = None,
            on_match: Optional[Callable[[Criteria], Collection[Task]]] = None,
            on_delete: Optional[Callable[[Task], None]] = None,
    ) -> TaskRepository:
        return _Repository(on_all, on_find, on_save, on_match, on_delete)

    return __
