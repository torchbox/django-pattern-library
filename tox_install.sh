#!/bin/sh
set -e

# For compatibility with Python 3.10.
# See https://github.com/python-poetry/poetry/issues/4210.
poetry config experimental.new-installer false
poetry install

if [ ! -z "$@" ]
then
    poetry run python -m pip install $@
fi
