#!/bin/sh

alembic upgrade head

pytest

exec "$@"