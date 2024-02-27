# If changes made, run: docker compose up -d --build
FROM python:3.12-slim

# development, test, staging, production
ARG INSTALL_DEV_DEPS

# Install required packages and clean up disc space
RUN apt-get update && \
    apt-get install -y curl emacs && \
    apt clean && \
    rm -rf /var/cache/apt/* && \
    rm -rf /var/lib/apt/lists/*


ENV APP_DIR="/opt/app" \
    # Poetry Configuration
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

# https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425
SHELL [ "/bin/bash", "-o", "pipefail", "-c" ]

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=${POETRY_HOME} python3 - --version ${POETRY_VERSION} && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry

WORKDIR $APP_DIR

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* $APP_DIR
RUN poetry install $(test "$INSTALL_DEV_DEPS" == 'false' && echo "--only main") --no-root --no-interaction --no-ansi

COPY . $APP_DIR
ENV PATH "$PATH:$APP_DIR/scripts"

RUN useradd -m -d ${APP_DIR} -s /bin/bash dev && \
    chown -R dev:dev ${APP_DIR}/*

USER dev

EXPOSE 8000
CMD ["uvicorn", "--reload", "--host=0.0.0.0", "--port=8000", "src.main:app"]