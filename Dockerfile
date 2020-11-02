FROM python:3.7

WORKDIR /app

RUN useradd dpl && \
    pip install --pre poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml ./
RUN poetry install --no-root

ENV DJANGO_SETTINGS_MODULE=tests.settings.dev \
    PYTHONPATH=.

USER dpl
CMD django-admin runserver 0.0.0.0:8000
