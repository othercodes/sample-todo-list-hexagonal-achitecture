from datetime import datetime
from typing import Dict, Any, Optional

from to_do_list.tasks.domain.contracts import TaskSource


class DictTaskSource(TaskSource):
    def __init__(self, data: Dict[str, Any]):
        self.__data = data

    def id(self) -> Optional[str]:
        return self.__data.get('id')

    def description(self) -> str:
        return self.__data.get('description')

    def due_date(self) -> str:
        return self.__data.get('due_date')

    def created(self) -> Optional[str]:
        return self.__data.get('created', datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
