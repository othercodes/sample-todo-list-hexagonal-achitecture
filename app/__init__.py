from __future__ import annotations
from typing import Any

import pinject
from pinject.errors import NothingInjectableForArgError

from app.configuration import logger, main
from app.providers import ServiceProvider


class Container:
    """ Container for dependency injection. """

    def __init__(self, specification: ServiceProvider):
        """
        Initialize container.

        :param specification: ServiceProvider instance.
        """
        self.__container = pinject.new_object_graph(
            binding_specs=[specification],
            # disable the auto-search for implicit bindings.
            modules=None,
        )

    def get(self, cls) -> Any:
        """
        Get instance of class.

        :param cls: Class to get instance of.
        :return: Instance of class.
        """
        try:
            return self.__container.provide(cls)
        except NothingInjectableForArgError as e:
            raise ValueError(str(e))
