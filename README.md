# Salomon Project Template

This template uses:

* `uv` for dependency management
* `pytest` for testing
* `ruff` for linting and formatting

---

## Quick start

Install dependencies:

```bash
uv sync --dev
```

Run tests:

```bash
uv run pytest
```

Run linter:

```bash
uv run ruff check .
```

Run the project:

```bash
uv run python -m salomon.cli
```

## Environment variables

Copy `.env.example` to `.env` and fill in required values:

```bash
cp .env.example .env
```

## Project structure

```text
.
├── .github/
│   └── workflows/
│       ├── lint.yml
│       └── test.yml
├── .gitignore
├── .env.example
├── README.md
├── TEMPLATE_README.md
├── pyproject.toml
├── uv.lock
├── data/
│   ├── raw/
│   ├── interim/
│   ├── external/
│   └── processed/
├── docs/
├── notebooks/
├── scripts/
├── src/
│   └── salomon/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── dataset.py
│       ├── features.py
│       ├── plots.py
│       ├── extraction/
│           ├── file_discovery.py
│           ├── function_extractor.py
│           ├── models.py
│           └── git_tools.py
│       └── modeling/
│           ├── __init__.py
│           ├── train.py
│           └── predict.py
└── tests/
    └── test_showcase.py
```


* `src/` – source root
* `salomon/` – main project package
* `cli.py` – entrypoint
* `config.py` – configuration
* `modeling/`, `dataset.py`, etc. – example structure for data/ML workflows
* `scripts/` – one-off scripts
* `tests/` – unit tests
* `.github/workflows/` – CI

---