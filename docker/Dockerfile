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

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
COPY docker/nginx/nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /src

# Generate requirements and install *all* dependencies.
COPY ./src/pyproject.toml ./src/poetry.lock /src/
RUN poetry export --dev --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt
RUN pip install --prefix=/runtime --force-reinstall -r requirements.txt

FROM base AS runtime

COPY --from=builder /runtime /usr/local

ENV PATH=/root/.local/bin:$PATH \
    PYTHONPATH="$PYTHONPATH:/runtime/lib/python3.10/site-packages" \
    DJANGO_SETTINGS_MODULE="djlodging.django_app.django_core.settings"

RUN apt-get update && apt-get install nginx -y
# TODO Use dockrignore to ignore reports, pylint, coverage etc!!!
COPY ./src ./app
# TODO COPY in one go!!!
COPY docker/init.sh /app
# RUN chmod +x /app/init.sh
# COPY docker/nginx.conf /etc/nginx/nginx.conf
WORKDIR /app

# start server
EXPOSE 8020 8010
STOPSIGNAL SIGTERM
CMD ["/app/init.sh"]

# EXPOSE 8020
# ENTRYPOINT [ "/app/init.sh" ]
# RUN python djlodging/django_app/manage.py collectstatic
# RUN python djlodging/django_app/manage.py migrate
# RUN nginx
# CMD gunicorn --bind localhost:80 djlodging.django_app.django_app.wsgi
# CMD gunicorn --bind 0.0.0.0:8010 djlodging.django_app.django_core.wsgi
