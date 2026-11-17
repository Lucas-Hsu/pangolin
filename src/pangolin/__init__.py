"""Pangolin desktop application."""


def main():
    """Load Qt only when starting the desktop application."""
    try:
        from .app import main as run
    except ModuleNotFoundError as exc:
        if exc.name == "PyQt6" or (exc.name and exc.name.startswith("PyQt6.")):
            raise SystemExit(
                "PyQt6 is not installed in this Python environment.\n"
                "From the project folder, run: uv run pangolin\n"
                "Or open Start-Pangolin.command on macOS."
            ) from None
        raise
    return run()
