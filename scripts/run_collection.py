import argparse
from pathlib import Path

import ezmsg.core as ez
from loguru import logger

from slumber import settings
from slumber.dag.utils import CollectionConfig
from slumber.utils.helpers import load_yaml
from slumber.utils.logger import setup_logging


def parse_args():
    parser = argparse.ArgumentParser(description="Run a collection.")
    parser.add_argument("config_file", type=Path, help="Path to the configuration file")
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=Path("."),
        help="Path to the directory where logs will be stored",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    setup_logging(args.log_dir, settings["logging"])

    collection_config = load_yaml(args.config_file)
    collection_config = CollectionConfig.model_validate(collection_config)
    logger.info(
        f"Running collection {collection_config.name if collection_config.name else ''}"
        f": Components: {list(collection_config.components.keys())}"
        f" - {len(collection_config.connections)} connections"
        f" - Process components: {list(collection_config.process_components)}"
    )
    ez.run(**collection_config.model_dump(by_alias=True))


if __name__ == "__main__":
    main()
