from abc import ABCMeta, abstractmethod
from typing import Optional

from complexheart.domain.criteria import Criteria

from to_do_list.shared.domain.models import Collection
from to_do_list.tasks.domain.models import Task


class TaskSource(metaclass=ABCMeta):
    @abstractmethod
    def id(self) -> Optional[str]:
        """
        :return: Provides the task id.
        """

    @abstractmethod
    def description(self) -> str:
        """
        :return: Provides the task description.
        """

    @abstractmethod
    def due_date(self) -> str:
        """
        :return: Provides the task due date.
        """

    @abstractmethod
    def created(self) -> Optional[str]:
        """
        :return: Provides the task created date.
        """


class TaskRepository(metaclass=ABCMeta):
    @abstractmethod
    def all(self) -> Collection[Task]:
        """
        Returns all tasks
        """

    @abstractmethod
    def find(self, id: int) -> Optional[Task]:
        """
        Finds a task by id
        """

    @abstractmethod
    def save(self, task: Task) -> Task:
        """
        Saves a task
        """

    @abstractmethod
    def match(self, criteria: Criteria) -> Collection[Task]:
        """
        Returns tasks that match the criteria
        """

    @abstractmethod
    def delete(self, id: int) -> None:
        """
        Deletes a task
        """
