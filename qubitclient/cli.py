# -*- coding: utf-8 -*-
# CLI module for qubitclient using typer

import shutil
from pathlib import Path

import typer

from . import __version__

app = typer.Typer(help="qubitclient - Quantum computing analysis client")
serve_app = typer.Typer(help="Server deployment commands")


@app.callback()
def main():
    """qubitclient - Quantum computing analysis client"""
    pass


@serve_app.command("init")
def serve_init(
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite existing files"),
):
    """Initialize deployment files in current directory."""
    current_dir = Path.cwd()
    template_dir = Path(__file__).parent / "serve_templates"

    if not template_dir.exists():
        typer.echo("Error: serve_templates not found", err=True)
        raise typer.Exit(1)

    # Copy entire serve_templates folder
    dest_dir = current_dir / "serve_templates"
    if dest_dir.exists():
        if overwrite:
            shutil.rmtree(dest_dir)
        else:
            typer.echo(f"Warning: {dest_dir} already exists, skipping")
            raise typer.Exit(0)

    shutil.copytree(template_dir, dest_dir)
    typer.echo(f"Copied: {dest_dir.relative_to(current_dir)}")

    typer.echo(f"\nDeployment files initialized in {current_dir}")
    typer.echo("You can run: docker-compose up -d")


app.add_typer(serve_app, name="serve")


def cli_main():
    app()


if __name__ == "__main__":
    app()