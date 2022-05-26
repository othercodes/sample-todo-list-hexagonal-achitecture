import os

import click as click

from dotenv import load_dotenv

from app import Container, ServiceProvider
from app.configuration import database, logger, main
from to_do_list.tasks.application.services import TaskCreator, TaskFinder, TaskDeleter
from to_do_list.tasks.application.sources import DictTaskSource
from to_do_list.tasks.infrastructure.persistence.relational import DBInstaller


@click.group()
@click.pass_context
def cli(ctx: click.core.Context):
    if os.path.exists(os.path.join(os.getcwd(), '.env')):
        load_dotenv()

    ctx.obj = Container(ServiceProvider({
        'app': main(),
        'db': database(),
        'logger': logger(),
    }))


@cli.command(name='init')
@click.pass_obj
def cmd_init(container: Container):
    use_case = container.get(DBInstaller)  # type: DBInstaller
    use_case.install()


@cli.command(name='add')
@click.argument('description')
@click.argument('due_date')
@click.pass_obj
def cmd_add(container: Container, description: str, due_date: str):
    use_case = container.get(TaskCreator)  # type: TaskCreator
    task = use_case.create(DictTaskSource({
        'description': description,
        'due_date': due_date,
    }))

    click.echo(f'New task added: {task}')


@cli.command(name='list')
@click.pass_obj
def cmd_list(container: Container):
    use_case = container.get(TaskFinder)  # type: TaskFinder

    for task in use_case.all():
        click.echo(f'{task}')


@cli.command(name='delete')
@click.argument('task_id', type=int)
@click.pass_obj
def cmd_delete(container: Container, task_id: int):
    use_case = container.get(TaskDeleter)  # type: TaskDeleter
    use_case.delete(task_id)

    click.echo(f'Task #{task_id} deleted!')
