# FastAPI + PostgreSQL Project Starter

## Setup

1. `cp .env.template .env` (do not alter contents of .env.template)
2. `docker compose up -d --build` (1st run only, or on Dockerfile changes)

### VSCode Extensions

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) → should automatically install [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance), [Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)
- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) (format Python files)
- [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8) (linting)
- [Mypy Type Checker](https://marketplace.visualstudio.com/items?itemName=ms-python.mypy-type-checker) (type checking)
- [isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort) (import sorting)

## Docker

```sh
docker build -t hsunami10/fastapi-postgresql-starter . --build-arg INSTALL_DEV_DEPS=development

docker run -d -p 3000:8000 hsunami10/fastapi-postgresql-starter
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
- https://github.com/orgs/python-poetry/discussions/1879
- https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
- https://github.com/svx/poetry-fastapi-docker/blob/main/Dockerfile
- https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/fe95750e3a3db6418383e7c39c5c3f7a5306773c/src/backend/backend.dockerfile
- https://github.com/zhanymkanov/fastapi_production_template/blob/main/Dockerfile