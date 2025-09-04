import typer
from pathlib import Path

from app.core.engine import PipelineEngine


app = typer.Typer()


@app.command()
def run(
    input: str = typer.Option("data/docs", help="Input directory with documents"),
    out: str = typer.Option("out", help="Output directory"),
    config: str = typer.Option("config/config.yaml", help="Path to config.yaml"),
    query: str = typer.Option("Project requirements", help="High-level query context")
):
    engine = PipelineEngine(config)
    result = engine.run(input, out, query)
    typer.echo(result)


if __name__ == "__main__":
    app()


