# -*- coding: utf-8 -*-
# CLI module for qubitclient using typer

import subprocess
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


@app.command("init")
def client_init(
    overwrite: bool = typer.Option(False, "--overwrite", help="Overwrite existing files"),
):
    """Initialize configuration files in current directory."""
    current_dir = Path.cwd()
    template_dir = Path(__file__).parent / "config_templates"

    if not template_dir.exists():
        typer.echo("Error: config_templates not found", err=True)
        raise typer.Exit(1)

    # Copy qubitclient.json (from .example template)
    src_config = template_dir / "qubitclient.json.example"
    dest_config = current_dir / "qubitclient.json"
    if dest_config.exists():
        if not overwrite:
            typer.echo(f"Warning: {dest_config} already exists, skipping")
        else:
            dest_config.unlink()
            shutil.copy2(src_config, dest_config)
            typer.echo(f"Copied: {dest_config.relative_to(current_dir)}")
    else:
        shutil.copy2(src_config, dest_config)
        typer.echo(f"Copied: {dest_config.relative_to(current_dir)}")

    # Copy mcp.json
    src_mcp = template_dir / "mcp.json"
    dest_mcp = current_dir / ".mcp.json"
    if dest_mcp.exists():
        if not overwrite:
            typer.echo(f"Warning: {dest_mcp} already exists, skipping")
        else:
            dest_mcp.unlink()
            shutil.copy2(src_mcp, dest_mcp)
            typer.echo(f"Copied: {dest_mcp.relative_to(current_dir)}")
    else:
        shutil.copy2(src_mcp, dest_mcp)
        typer.echo(f"Copied: {dest_mcp.relative_to(current_dir)}")

    typer.echo(f"\nConfiguration files initialized in {current_dir}")


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


@serve_app.command("up")
def serve_up(
    detach: bool = True,
):
    """Start all services via docker-compose."""
    compose_file = Path.cwd() / "serve_templates" / "docker-compose.yml"
    if not compose_file.exists():
        typer.echo("Error: serve_templates/docker-compose.yml not found", err=True)
        typer.echo("Run 'qubitclient serve init' first")
        raise typer.Exit(1)

    typer.echo("Starting services...")
    result = subprocess.run(
        ["docker-compose", "-f", str(compose_file), "up", "-d" if detach else ""],
        cwd=Path.cwd(),
    )
    raise typer.Exit(result.returncode)


app.add_typer(serve_app, name="serve")


def cli_main():
    app()


if __name__ == "__main__":
    app()