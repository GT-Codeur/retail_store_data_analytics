# Retail Store Data Analytics

A self-contained example project that demonstrates an end-to-end Airflow-driven ETL pipeline for retail store sales data, with extract/load logic, transformation scripts, SQL assets, and local Docker-based orchestration.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
	- [Prerequisites](#prerequisites)
	- [Quick start (Docker Compose)](#quick-start-docker-compose)
	- [Local development (Python)](#local-development-python)
- [Running the ETL DAG](#running-the-etl-dag)
- [Project Structure](#project-structure)
- [Scripts and SQL](#scripts-and-sql)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Maintainers / Contact](#maintainers--contact)

## Project Overview

This repository provides a reproducible example of building a small-scale retail analytics pipeline. It includes:

- An Airflow DAG that orchestrates extraction, transformation, and load (ETL) tasks.
- Example sales data and scripts that transform and load data into analytical tables.
- Docker Compose configuration for running Airflow and dependencies locally.

The code is intentionally simple and geared toward demonstration, debugging, and iteration.

## Features

- Orchestrated ETL using Apache Airflow.
- Modular extraction and load logic in Python (see `scripts/`).
- Example SQL assets for analytical transformations (see `include/sql/`).
- Sample dataset: `dags/data/pos_sales_data_30k.json` for local testing.

## Architecture

The pipeline is structured around an Airflow DAG (`dags/etl_dag.py`) which calls Python scripts in `dags/scripts/` and top-level `scripts/` to perform extract, transform, and load work. SQL transformation assets are stored under `include/sql/`.

Core components:

- Orchestrator: Apache Airflow (`docker-compose.yaml` boots services).
- ETL code: Python scripts in `dags/scripts/` and `scripts/`.
- Data assets: `dags/data/pos_sales_data_30k.json` (sample sales records).

## Getting Started

### Prerequisites

- Docker & Docker Compose (recommended for reproducible local runs).
- Python 3.10+ (for local development without Docker).

### Quick start (Docker Compose)

1. Build and start services:

```bash
docker compose up --build
```

2. Open the Airflow web UI (by default at http://localhost:8080) and trigger the DAG named in `dags/etl_dag.py`.

3. To stop and remove containers, volumes, and images (use cautiously):

```bash
sudo docker compose down -v --rmi all
```

> Note: the Compose setup is intended for local evaluation. Customize memory/CPU limits if your machine is constrained.

### Local development (Python)

If you prefer not to use Docker, create a virtual environment and install dependencies used by the scripts. There is no centralized `requirements.txt` in this repository — install the packages you need (for example `apache-airflow`, `pandas`, and `sqlalchemy`) depending on which parts you run locally.

Example (Linux/macOS):

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pandas sqlalchemy
```

Run scripts directly to iterate on transformations. For example:

```bash
python scripts/extract_load_logic.py
```

## Running the ETL DAG

- The Airflow DAG is defined in `dags/etl_dag.py`.
- Trigger runs from the Airflow UI or use the Airflow CLI inside the running scheduler/container.

Files of interest: [dags/etl_dag.py](dags/etl_dag.py), [dags/scripts/extract_load_logic.py](dags/scripts/extract_load_logic.py)

## Project Structure

- `docker-compose.yaml` — Development compose configuration (Airflow + dependencies).
- `dags/` — Airflow DAG definitions and packaged DAG helpers.
	- `dags/etl_dag.py` — Main ETL DAG.
	- `dags/data/` — Example datasets used by the DAG.
	- `dags/scripts/` — DAG-scoped helper scripts.
- `scripts/` — Utility scripts for analytics, extraction, and loading (`analytics_tbl.py`, `extract_load_logic.py`).
- `include/sql/` — SQL transformation assets (e.g. `exploded_products.sql`).
- `config/` — Airflow and environment configuration files (e.g. `airflow.cfg`).
- `logs/` — Airflow run logs (generated during execution).

## Scripts and SQL

- `scripts/extract_load_logic.py` — Example extraction/load logic used by the DAG.
- `scripts/analytics_tbl.py` — Helper scripts for analytics table generation.
- `include/sql/exploded_products.sql` — Example transformation SQL.

Refer to each file header for usage details and requirements.

## Testing

This repository does not include an automated test suite. Recommendations:

- Add unit tests for transformation logic using `pytest`.
- Add integration tests that run the DAG in an isolated test Airflow instance (or use the Docker Compose setup).

## Contributing

Contributions are welcome. Suggested workflow:

1. Fork the repository and create a feature branch.
2. Implement changes and add tests where appropriate.
3. Open a pull request describing your changes.

Please follow the project code style and update documentation when adding features.

## License

This repository does not include a license file. If you intend to share or publish this project, add an appropriate LICENSE file (for example, MIT).

## Maintainers / Contact

For questions about this repository, open an issue or contact the maintainer via the project hosting platform.

---

If you'd like, I can:

- add a `requirements.txt` or `pyproject.toml` for reproducible installs,
- add basic `pytest` tests for the core transformation functions, or
- update `docker-compose.yaml` with labels/override examples for CI runs.

Tell me which of those you'd like next.
