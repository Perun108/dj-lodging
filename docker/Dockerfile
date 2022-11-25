FROM python:3.10-slim-bullseye AS base

FROM base AS builder

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/runtime/bin" \
    PYTHONPATH="$PYTHONPATH:/runtime/lib/python3.10/site-packages" \
    POETRY_VERSION=1.1.14

RUN apt-get update && apt-get install -y --no-install-recommends wget nginx
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /src

# Generate requirements and install *all* dependencies.
COPY ./src/pyproject.toml ./src/poetry.lock /src/
RUN poetry export --dev --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt
RUN pip install --prefix=/runtime --force-reinstall -r requirements.txt


COPY . /src

FROM base AS runtime
COPY --from=builder /runtime /usr/local
COPY ./src /app
COPY docker/init.sh /app
ADD docker/nginx/default.conf /etc/nginx/sites-enabled/default
WORKDIR /app

ENTRYPOINT [ "/app/init.sh" ]
CMD gunicorn --bind localhost:80 djlodging.django_app.django_app.wsgi
