"""postgres entry point."""

from __future__ import annotations

from tap_postgres.tap import Tappostgres

Tappostgres.cli()
