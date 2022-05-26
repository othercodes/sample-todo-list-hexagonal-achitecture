from typing import TypeVar, Iterable, Generic, Union, Callable, Optional, Iterator

T = TypeVar('T')


class Collection(Iterable, Generic[T]):
    def __init__(self, items: Union[Iterable, Callable[[], Iterable]], total: Optional[int] = None):
        self._items = items

        def _count(items: Union[Iterable, Callable[[], Iterable]]) -> int:
            return sum(1 for _ in items()) if callable(items) else len(list(items))

        self._total = total if total else _count(items)

    @property
    def items(self) -> Iterable:
        return self._items() if callable(self._items) else self._items

    @property
    def total(self) -> int:
        return self._total

    def __len__(self) -> int:
        return self.total

    def __iter__(self) -> Iterator:
        return iter(self.items)
