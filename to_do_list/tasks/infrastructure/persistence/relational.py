from typing import Optional

from complexheart.domain.criteria import Criteria
from sqlalchemy import Table, MetaData, Column, orm, String, Integer, DateTime

from to_do_list.shared.domain.models import Collection
from to_do_list.tasks.domain.contracts import TaskRepository
from to_do_list.tasks.domain.models import Task

mapper = orm.registry()
metadata = MetaData()

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
        query = self.session.query(Task) \
            .order_by(criteria.order.by) \
            .limit(criteria.page.limit) \
            .offset(criteria.page.offset)

        # TODO: implement the filters

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
