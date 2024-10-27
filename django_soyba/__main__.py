#!/bin/env python
import os
import subprocess
from pathlib import Path

from gunicorn.app.wsgiapp import run as gunicorn_run
from gunicorn.util import logging
from typer import Typer

typer = Typer()


class NoVenvError(Exception):
    pass


def sh(command: str):
    return subprocess.run(command.split(), check=True)


@typer.command(help="Install this script in virtual environment. It should be available as 'cli' or 'run'.")
def install_cli():
    venv_path = os.getenv("VIRTUAL_ENV")
    if not venv_path:
        message = "You should not install this script globally"
        raise NoVenvError(message)
    venv_bin = Path(venv_path) / "bin"
    os.symlink(__file__, venv_bin / "cli")
    os.symlink(__file__, venv_bin / "run")


@typer.command()
def build():
    sh("docker compose build --no-cache")


@typer.command()
def up():
    sh("docker compose up -d")


@typer.command()
def down():
    sh("docker compose down")


@typer.command("format")
def format_():
    sh("black .")


@typer.command()
def test():
    sh("pytest tests")


@typer.command()
def logs():
    sh("docker compose logs")


@typer.command()
def run_api():
    logging.info("Collecting static files...")
    sh("python manage.py collectstatic --noinput")
    logging.info("Applying database migrations...")
    sh("python manage.py migrate")
    logging.info("Starting Gunicorn server...")
    gunicorn_run(["-w", "4", "-b", "127.0.0.1:8000", "myapp:app"])


@typer.command()
def run_celery_worker():
    sh("celery -A config worker -l info --concurrency=10")


typer()
