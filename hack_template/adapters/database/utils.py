import os
from argparse import Namespace
from enum import Enum
from pathlib import Path
from typing import Any, Final

import sqlalchemy.dialects.postgresql as pg
from alembic.config import Config
from hasql.asyncsqlalchemy import PoolManager

PROJECT_PATH: Final = Path(__file__).parent.parent.parent


async def create_pool(
    dsn: str,
    pool_size: int,
    pool_timeout: int,
    replicas_count: int,
    max_overflow: int = 5,
) -> PoolManager:
    pool = PoolManager(
        dsn=dsn,
        acquire_timeout=pool_timeout,
        fallback_master=True,
        pool_factory_kwargs=dict(pool_size=pool_size, max_overflow=max_overflow),
    )
    await pool.ready(masters_count=1, replicas_count=replicas_count)
    return pool


def make_alembic_config(
    cmd_opts: Namespace, pg_url: str, base_path: Path = PROJECT_PATH
) -> Config:
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = str(base_path / "adapters/database" / cmd_opts.config)

    config = Config(
        file_=cmd_opts.config,
        ini_section=cmd_opts.name,
        cmd_opts=cmd_opts,
    )

    alembic_location = config.get_main_option("script_location")
    if not alembic_location:
        raise ValueError

    if not os.path.isabs(alembic_location):
        config.set_main_option("script_location", str(base_path / alembic_location))

    config.set_main_option("sqlalchemy.url", pg_url)

    config.attributes["configure_logger"] = False

    return config


def make_pg_enum(enum_cls: type[Enum], **kwargs: Any) -> pg.ENUM:
    return pg.ENUM(
        enum_cls,
        values_callable=_choices,
        **kwargs,
    )


def _choices(enum_cls: type[Enum]) -> tuple[str, ...]:
    return tuple(map(str, enum_cls))
