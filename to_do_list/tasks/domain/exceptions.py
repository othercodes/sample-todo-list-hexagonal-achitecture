class TaskException(Exception):
    """
    Base class for exceptions in this module.
    """


class InvalidTaskDescription(TaskException):
    """
    Exception raised when the task description is invalid.
    """


class InvalidTaskDueDate(TaskException):
    """
    Exception raised when the task due date is invalid.
    """


class TaskNotFound(TaskException):
    """
    Exception raised when a task is not found by id.
    """
