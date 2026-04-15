from __future__ import annotations

import argparse

from app.config import get_settings
from app.core.version import __version__


def main() -> None:
    p = argparse.ArgumentParser(prog="python -m app")
    sub = p.add_subparsers(dest="cmd", required=True)

    pv = sub.add_parser("version", help="print embedded version string")
    pv.set_defaults(func=_cmd_version)

    pc = sub.add_parser("config", help="print non-secret settings")
    pc.set_defaults(func=_cmd_config)

    args = p.parse_args()
    args.func()


def _cmd_version() -> None:
    print(__version__)


def _cmd_config() -> None:
    s = get_settings()
    print(f"use_mock_data={s.use_mock_data}")
    print(f"cors_origins={s.cors_origins}")


if __name__ == "__main__":
    main()
