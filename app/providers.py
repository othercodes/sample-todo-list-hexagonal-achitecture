import logging.config
from logging import getLogger, LoggerAdapter
from typing import Optional

from pinject import BindingSpec as Provider

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from to_do_list.tasks.domain.contracts import TaskRepository
from to_do_list.tasks.infrastructure.persistence.relational import RelationalTaskRepository


class ServiceProvider(Provider):
    def __init__(self, configuration: Optional[dict] = None):
        self.configuration = {} if configuration is None else configuration

    def configure(self, bind):
        logger_cfg = self.configuration.pop('logger', None)
        if logger_cfg is not None:
            logging.config.dictConfig(logger_cfg)

        for name, section in self.configuration.items():
            if isinstance(section, dict):
                for key, value in section.items():
                    bind(f"{name}_{key}".lower(), to_instance=value.strip())
            else:
                bind(name.lower(), to_instance=section.strip())

    def provide_db_engine(self, db_uri: str):
        return create_engine(db_uri)

    def provide_db_session(self, db_engine) -> Session:
        return sessionmaker(bind=db_engine)()

    def provide_task_repository(self, db_session) -> TaskRepository:
        return RelationalTaskRepository(db_session)

    def provide_logger(self, app_name: str) -> LoggerAdapter:
        return LoggerAdapter(getLogger(app_name), {})
