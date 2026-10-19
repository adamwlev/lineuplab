"""Read access to the local Postgres corpus.

Connection settings never live in code. ``BASKETBALL_DSN`` overrides
everything; otherwise libpq's own environment (``PGHOST``, ``PGPORT``,
``PGDATABASE``, ``PGUSER``, ``PGPASSWORD``) and ``~/.pgpass`` apply, with the
database name defaulting to ``local`` and the user to the OS account.
"""
import os
from contextlib import closing

DEFAULT_DATABASE = "local"


def dsn():
    """Connection string without any secret in it."""
    return os.environ.get("BASKETBALL_DSN") or f"dbname={os.environ.get('PGDATABASE', DEFAULT_DATABASE)}"


def connect(**kwargs):
    import psycopg2
    return psycopg2.connect(dsn(), **kwargs)


def heights():
    """Listed height in inches by player id (nba.players; static, not outcome data)."""
    import pandas as pd
    with closing(connect()) as conn, conn.cursor() as cur:
        cur.execute("select id, height_inches from nba.players where height_inches is not null")
        rows = cur.fetchall()
    return pd.Series({int(i): float(h) for i, h in rows}, name="height_inches", dtype=float)
