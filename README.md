# Sample TODO List with Hexagonal Architecture

Sample of TO-DO List Application using Hexagonal Architecture.

1. **Infrastructure**: Database specific connectors all 3rd part dependant goes here.
2. **Application**: Main use cases.
3. **Domain**: All the business logic goes here.

## Domain

![Class Diagram](/resources/sample-todo-list.png?raw=true)

```bash
to_do_list
    ├── shared
    │         └── domain
    │             └── models.py
    └── tasks
        ├── application
        │         ├── services.py
        │         └── sources.py
        ├── domain
        │         ├── contracts.py
        │         ├── exceptions.py
        │         ├── models.py
        │         └── services.py
        └── infrastructure
            └── persistence
                └── relational.py
```

## CLI Application

```bash
app
    ├── configuration.py
    ├── console.py
    └── providers.py
```

## Installation

Just run poetry to install the dependencies.

```bash
poetry install
```

Next, you need to create and configure the `.env` file.

```bash
# create .env file
cp example.env .env
# create the database file.
touch to_do_list.db
```

## Usage

Once the dependencies are installed, you can run the application using the following command.

```bash
# initialize the database.
poetry run python todo.py init
# use the application.
poetry run python todo.py
```

## Tests

1. **Unit**: tests the domain and application layer.
2. **Integration**: tests the infrastructure layer.

To run test you can use the following command.

```bash
poetry run pytest
```

```bash
tests                         
    ├── conftest.py                                                        
    ├── integration                                                        
    │     └── test_infrastructure_persistence.py                             
    └── unit                                                                               
          └── test_application_services.py
```
