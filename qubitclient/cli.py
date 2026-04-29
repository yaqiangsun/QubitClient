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
    typer.echo("Next steps:")
    typer.echo("  1. Download models: qubitclient serve download")
    typer.echo("  2. Start services: qubitclient serve up -d")


@serve_app.command("up")
def serve_up(
    detach: bool = typer.Option(False, "--detach", "-d", help="Run containers in detached mode"),
):
    """Start all services via docker-compose."""
    compose_file = Path.cwd() / "serve_templates" / "docker-compose.yml"
    if not compose_file.exists():
        typer.echo("Error: serve_templates/docker-compose.yml not found", err=True)
        typer.echo("Run 'qubitclient serve init' first")
        raise typer.Exit(1)

    # Check if model_zoo has actual model files (exclude README)
    model_zoo_dir = Path.cwd() / "serve_templates" / "qubitserving" / "model_zoo"
    has_models = False
    if model_zoo_dir.exists():
        for item in model_zoo_dir.iterdir():
            if item.is_file() and item.name.upper() != "README.md":
                has_models = True
                break
            if item.is_dir():
                has_models = True
                break

    if not has_models:
        typer.echo("Warning: model_zoo folder is empty or missing models", err=True)
        typer.echo("Download models first: qubitclient serve download")

    typer.echo("Starting services...")
    result = subprocess.run(
        ["docker-compose", "-f", str(compose_file), "up", "-d" if detach else ""],
        cwd=Path.cwd(),
    )
    raise typer.Exit(result.returncode)


@serve_app.command("download")
def serve_download(
    model_name: str = typer.Option("yaqiangsun/qubitscope-enc", "--model", "-m", help="ModelScope model ID"),
    target_dir: str = typer.Option("serve_templates/qubitserving/model_zoo", "--dir", "-d", help="Target directory to save model"),
):
    """Download models from ModelScope to model_zoo folder."""
    try:
        from modelscope import snapshot_download
    except ImportError:
        typer.echo("Error: modelscope is not installed", err=True)
        typer.echo("Install with: pip install modelscope")
        raise typer.Exit(1)

    target_path = Path.cwd() / target_dir
    target_path.mkdir(parents=True, exist_ok=True)

    typer.echo(f"Downloading model: {model_name}")
    typer.echo(f"Target directory: {target_path.absolute()}")

    try:
        model_dir = snapshot_download(model_name, local_dir=str(target_path))
        typer.echo(f"Model downloaded successfully to: {model_dir}")
    except Exception as e:
        typer.echo(f"Error downloading model: {e}", err=True)
        raise typer.Exit(1)


@serve_app.command("license")
def serve_license(
    output: str = typer.Option("tmp/device.json", "--output", "-o", help="Output file path"),
):
    """Collect device info using modellock and save to device.json."""
    try:
        from modellock import collect_device_info
    except ImportError:
        typer.echo("Error: modellock is not installed", err=True)
        typer.echo("Install with: pip install modellock")
        raise typer.Exit(1)

    output_path = Path.cwd() / output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    typer.echo(f"Collecting device info to: {output_path.absolute()}")

    try:
        collect_device_info(output=str(output_path))
        typer.echo(f"Device info saved successfully to: {output_path}")
    except Exception as e:
        typer.echo(f"Error collecting device info: {e}", err=True)
        raise typer.Exit(1)


app.add_typer(serve_app, name="serve")


def cli_main():
    app()


if __name__ == "__main__":
    app()