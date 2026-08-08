# Repository guidance

## Development workflow

- Use mise for project setup and routine commands.
- Run the application with `mise run pytickrs -- [arguments]`.
- Before committing, run:
  - `mise run format`
  - `mise run lint`
  - `mise run mypy`
  - `mise run tests`
- The `test_single_ticker` test contacts Yahoo Finance and requires network
  access.

## Project conventions

- Treat the version in `pyproject.toml` as the single source of truth.
- Keep Yahoo Finance requests and other blocking work off the Textual UI thread.
- Handle missing or malformed market fields without failing the entire
  watchlist refresh.
- Preserve successful ticker results when individual ticker requests fail.
- Resolve bundled default files independently of the caller's working
  directory.

## Generated files

- Do not commit `.venv`, Python caches, Ruff or mypy caches, or `main.log`.
