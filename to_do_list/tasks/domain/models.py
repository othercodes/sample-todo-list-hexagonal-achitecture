from __future__ import annotations
import datetime as datetime
from typing import Optional

from to_do_list.tasks.domain.exceptions import InvalidTaskDescription, InvalidTaskDueDate


class Task:
    def __init__(self, id: Optional[int], description: str, due_date: datetime, created: datetime):
        self.id = id
        self.description = description
        self.due_date = due_date
        self.created = created

        self._invariant_description_must_max_length()
        self._invariant_due_date_must_be_greater_than_created()

    def _invariant_description_must_max_length(self):
        if len(self.description) > 255:
            raise InvalidTaskDescription('Task description {description} must be less than 255 characters'.format(
                description=self.description
            ))

    def _invariant_due_date_must_be_greater_than_created(self):
        if self.due_date < self.created:
            raise InvalidTaskDueDate('Task due date {due_date} must be greater than created date {created}'.format(
                due_date=self.due_date,
                created=self.created
            ))

    def with_description(self, description: str) -> Task:
        return self.__class__(
            id=self.id,
            description=description,
            due_date=self.due_date,
            created=self.created
        )

    def with_due_date(self, due_date: datetime) -> Task:
        return self.__class__(
            id=self.id,
            description=self.description,
            due_date=due_date,
            created=self.created
        )

    def __eq__(self, other: Task) -> bool:
        return isinstance(other, Task) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        return '#{id} {description} due {due_date} created at {created}.'.format(
            id=self.id,
            description=self.description,
            due_date=self.due_date,
            created=self.created
        )
