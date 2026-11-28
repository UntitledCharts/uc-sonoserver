import argparse
import logging
import os
import sys
from pathlib import Path

import uvicorn

from app.application import CONFIG_ENV, CONSTANTS_ENV
from app.settings import load_config, load_constants


def main() -> None:
    """Start the Sonolus server with uvicorn."""
    parser = argparse.ArgumentParser(description="Run the UntitledCharts Sonolus server")
    parser.add_argument("--config", default="config.yml", help="path to config.yml")
    parser.add_argument("--constants", default="constants.yml", help="path to constants.yml")
    args = parser.parse_args()
    config_path = Path(args.config).resolve()
    constants_path = Path(args.constants).resolve()
    config = load_config(config_path)
    load_constants(constants_path)
    os.environ[CONFIG_ENV] = str(config_path)
    os.environ[CONSTANTS_ENV] = str(constants_path)
    logging.basicConfig(level=logging.DEBUG if config.server.debug else logging.INFO)
    workers = config.server.workers
    if sys.platform == "win32" and workers > 1:
        logging.warning("uvicorn can't serve with several workers on Windows, starting 1")
        workers = 1
    uvicorn.run(
        "app.application:create_app_from_env",
        factory=True,
        host=config.server.host,
        port=config.server.port,
        workers=workers,
        access_log=config.server.debug,
        proxy_headers=False,
    )


if __name__ == "__main__":
    main()
