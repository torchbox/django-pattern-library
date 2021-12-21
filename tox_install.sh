#!/bin/sh
set -e

poetry install

if [ ! -z "$@" ]
then
    poetry run python -m pip install $@
fi
