from pathlib import Path

import ezmsg.core as ez
from loguru import logger

from slumber import settings
from slumber.dag.utils import CollectionConfig
from slumber.sources.zmax import ZMax
from slumber.utils.helpers import load_yaml
from slumber.utils.logger import setup_logging

CONFIG_FILE = Path("./configs/collections/home_lucid_dreaming.yaml")


def main():
    config = load_yaml(CONFIG_FILE)

    with ZMax() as zmax:
        config["components"]["ZMAX"]["settings"]["zmax"] = zmax
        collection_config = CollectionConfig.model_validate(config)
        logger.info(
            f"Starting collection with {len(collection_config.components)} components."
        )
        ez.run(**collection_config.model_dump())


if __name__ == "__main__":
    log_dir = Path(settings["data_dir"])
    setup_logging(log_dir, settings["logging"])
    main()
