# FastAPI + PostgreSQL Project Starter

## Setup

1. `cp .env.template .env` (do not alter contents of .env.template)
2. `docker compose up -d --build` (1st run only, or on Dockerfile changes)

### [TablePlus](https://tableplus.com/)

Connection Fields:

- Host/Socket: `127.0.0.1` (default, leave blank)
- Port: `5555` 
- Password: `changethis`
- Database: `app`

### VSCode Extensions

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) → should automatically install [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance), [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) (format Python files)
- [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8) (linting)
- [Mypy Type Checker](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker)
- [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort) (import sorting)
- [Even Better TOML](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml)

## Docker

```sh
# Workflow:

# Run with --build if there are changes in: poetry deps, Dockerfile, compose.*.yml
# Otherwise, run without --build
docker compose up -d --build
```

## Alembic

https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a

```sh
# Make a new migration
alembic revision -m "revision name"

# Run all migrations
alembic upgrade head

# Downgrade by x (ex. 1) migration
alembic downgrade -1
```

## Resources

### Project Templates
- https://github.com/zhanymkanov/fastapi_production_template
- https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308
- https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html

### Poetry

- https://www.pythoncheatsheet.org/blog/python-projects-with-poetry-and-vscode-part-1

| Command                                    | Description                                            |
| ------------------------------------------ | ------------------------------------------------------ |
| `poetry new [package-name]`                | Start a new Python Project.                            |
| `poetry init`                              | Create a *pyproject.toml* file interactively.          |
| `poetry install`                           | Install the packages inside the *pyproject.toml* file. |
| `poetry add [package-name]`                | Add a package to a Virtual Environment.                |
| `poetry add --group dev [package-name]`    | Add a dev package to a Virtual Environment.            |
| `poetry remove [package-name]`             | Remove a package from a Virtual Environment.           |
| `poetry remove --group dev [package-name]` | Remove a dev package from a Virtual Environment.       |

### Docker

#### Sample Apps

- https://docs.docker.com/compose/samples-for-compose/
- https://github.com/zhanymkanov/fastapi_production_template
- https://github.com/tiangolo/full-stack-fastapi-postgresql

#### Poetry with Docker

- https://github.com/orgs/python-poetry/discussions/1879
- https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
- https://github.com/svx/poetry-fastapi-docker/blob/main/Dockerfile

## TODOs

### FastAPI

- [dependencies tutorial](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [use ruff](https://docs.astral.sh/ruff/) instead of isort, black, and flake8
- add pre-commit hooks (type-checking, linting, formatting)

### Docker

- split `compose.yml` file into `compose.yml` and `compose.override.yml` + clean up
  - [working with multiple compose files](https://docs.docker.com/compose/multiple-compose-files/)
  - [compose in prod](https://docs.docker.com/compose/production/)

- [properly use env vars](https://docs.docker.com/compose/environment-variables/) in `compose.*.yml` files
- [handle using secrets](https://docs.docker.com/compose/use-secrets/)