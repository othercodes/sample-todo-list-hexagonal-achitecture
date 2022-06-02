import operator
from typing import Optional, Any, Type

from complexheart.domain.criteria import Criteria, OrderType, Filter
from sqlalchemy import asc, desc, Table, Column, orm, String, Integer, DateTime

from to_do_list.shared.domain.models import Collection
from to_do_list.tasks.domain.contracts import TaskRepository
from to_do_list.tasks.domain.models import Task

mapper = orm.registry()
metadata = mapper.metadata

tasks = Table(
    'tasks',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('description', String(255), nullable=False),
    Column('due_date', DateTime, nullable=False),
    Column('created', DateTime, nullable=False),
)


def start_mappers():
    try:
        orm.class_mapper(Task)
    except orm.exc.UnmappedClassError:
        mapper.map_imperatively(Task, tasks)


class DBInstaller:
    def __init__(self, db_engine):
        self.engine = db_engine

    def install(self):
        metadata.create_all(self.engine)


def _compile_filter(ftr: Filter, cls: Type) -> Any:
    fn = {
        '==': lambda field, value: operator.eq(getattr(cls, field), value),
        '!=': lambda field, value: operator.ne(getattr(cls, field), value),
        '>': lambda field, value: operator.gt(getattr(cls, field), value),
        '>=': lambda field, value: operator.ge(getattr(cls, field), value),
        '<': lambda field, value: operator.lt(getattr(cls, field), value),
        '<=': lambda field, value: operator.le(getattr(cls, field), value),
        'in': lambda field, value: operator.contains(getattr(cls, field), value),
        'not in': lambda field, value: not operator.contains(getattr(cls, field), value),
        'like': lambda field, value: getattr(cls, field).like(value)
    }.get(ftr.operator)

    return fn(ftr.field, ftr.value)


class RelationalTaskRepository(TaskRepository):
    def __init__(self, db_session: orm.Session):
        start_mappers()
        self.session = db_session

    def all(self) -> Collection[Task]:
        query = self.session.query(Task)

        def deferred():
            for task in query:
                yield task

        return Collection(deferred, query.count())

    def find(self, id: int) -> Optional[Task]:
        return self.session.query(Task).get(id)

    def match(self, criteria: Criteria) -> Collection[Task]:
        query = self.session.query(Task)

        for f in criteria.filters:
            query = query.filter(_compile_filter(f, Task))

        ordering_fields = [getattr(Task, field) for field in criteria.order.by]
        ordering_type = desc(*ordering_fields) \
            if criteria.order.type is OrderType.DESC \
            else asc(*ordering_fields)

        query = query.order_by(ordering_type)
        query = query.limit(criteria.page.limit)
        query = query.offset(criteria.page.offset)

        def deferred():
            for task in query:
                yield task

        return Collection(deferred, query.count())

    def save(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()

        return task

    def delete(self, id: int) -> None:
        self.session.delete(self.find(id))
        self.session.commit()
