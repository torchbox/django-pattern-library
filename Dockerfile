FROM python:3.10

WORKDIR /app

RUN useradd --create-home dpl && \
    pip install "poetry>=1.1.12,<2" && \
    poetry config virtualenvs.create false

COPY pyproject.toml ./
RUN poetry install --no-root

ENV DJANGO_SETTINGS_MODULE=tests.settings.dev \
    PYTHONPATH=.

USER dpl
CMD django-admin runserver 0.0.0.0:8000
