from datetime import datetime

from to_do_list.tasks.domain.contracts import TaskSource
from to_do_list.tasks.domain.models import Task


def build_task(source: TaskSource) -> Task:
    return Task(
        id=source.id(),
        description=source.description(),
        due_date=datetime.strptime(source.due_date(), '%Y/%m/%d %H:%M:%S'),
        created=datetime.strptime(source.created(), '%Y/%m/%d %H:%M:%S')
    )
