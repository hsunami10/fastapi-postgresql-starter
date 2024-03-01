# FastAPI + PostgreSQL Project Starter

## Setup

1. `cp .env.template .env` (do not alter contents of .env.template)
2. `docker compose up -d --build`

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

Run `docker compose up -d --build` on these changes:
- .env file variables (not .py)
- Dockerfile
- compose.*.yml

```sh
# Workflow:

docker compose up -d # --build

# Terminal docker compose services
docker compose down # -v (to delete persisted volumes/data)

# Attach to see terminal output
docker compose attach <service_name>

# Start a terminal in a service
docker compose exec <service_name> bash
```

Services:

- `backend-api` - FastAPI web server
- `pg-db` - PostgreSQL database server

## [Migrations (Alembic)](https://medium.com/@johnidouglasmarangon/using-migrations-in-python-sqlalchemy-with-alembic-docker-solution-bd79b219d6a)

```sh
# Make a new migration
docker compose exec backend-api makemigrations "migration name"

# Run all migrations
docker compose exec backend-api migrate

# Downgrade by x (ex. 1) migration
docker compose exec backend-api downgrade -1
```

## Resources

- [SQLAlchemy Core Syntax](https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_core_selecting_rows.htm)

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

#### Sample Apps

- https://docs.docker.com/compose/samples-for-compose/
- https://github.com/zhanymkanov/fastapi_production_template
- https://github.com/tiangolo/full-stack-fastapi-postgresql

#### Poetry with Docker

- https://github.com/orgs/python-poetry/discussions/1879
- https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
- https://github.com/svx/poetry-fastapi-docker/blob/main/Dockerfile

### Extra Code (for future reference)

**Converting Python datetime object to JSON date string (UTC)**
See [this link](https://stackoverflow.com/questions/10805589/convert-json-date-string-to-python-datetime) for converting the other way around

```python
def convert_datetime_to_utc(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=timezone.utc)

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


# Replaces Pydantic v1 json_encoders
# https://github.com/pydantic/pydantic/discussions/7199#discussioncomment-7798544
UTCDateTime = Annotated[
    datetime, PlainSerializer(func=convert_datetime_to_utc, return_type=str)
]
```

## TODOs

### FastAPI

- [add scripts for alembic migrations](https://github.com/zhanymkanov/fastapi_production_template/tree/main/scripts)
- [use ruff](https://docs.astral.sh/ruff/) instead of isort, black, and flake8
- add pre-commit hooks (type-checking, linting, formatting)

### Docker

- scripts need `chmod +x` (executable) permissions on host computer to work... which doesn't require permissions from the container's user. is that secure?
- split `compose.yml` file into `compose.yml` and `compose.override.yml` + clean up
  - [working with multiple compose files](https://docs.docker.com/compose/multiple-compose-files/)
  - [compose in prod](https://docs.docker.com/compose/production/)

- [properly use env vars](https://docs.docker.com/compose/environment-variables/) in `compose.*.yml` files
- [handle using secrets](https://docs.docker.com/compose/use-secrets/)
