FROM python:3.10

WORKDIR /app

RUN useradd --create-home dpl && \
    mkdir -p /venv/ && \
    chown -R dpl:dpl /venv/ /app/

ENV PATH=/venv/bin:/home/dpl/.local/bin:$PATH \
    PYTHONPATH=/app/ \
    VIRTUAL_ENV=/venv/ \
    DJANGO_SETTINGS_MODULE=tests.settings.dev

USER dpl

RUN pip install --user "poetry>=1.1.12,<2" && \
    python -m venv /venv/

COPY pyproject.toml ./
RUN poetry install --no-root

CMD django-admin runserver 0.0.0.0:8000
