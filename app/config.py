"""All configuration comes from environment variables (never hardcode secrets)."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    db_path: str
    log_level: str


def get_settings() -> Settings:
    return Settings(
        db_path=os.environ.get("DB_PATH", "data/tickets.db"),
        log_level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    )
