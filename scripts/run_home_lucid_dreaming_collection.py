from pathlib import Path

from slumber.dag.utils import CollectionConfig
from slumber.utils.helpers import load_yaml

CONFIG_FILE = Path("./configs/collections/home_lucid_dreaming.yaml")


def main():
    config = load_yaml(CONFIG_FILE)
    config["components"]["ZMAX"]["settings"]["zmax"] = None
    collection_config = CollectionConfig.model_validate(config)
    print(collection_config)

    # with ZMax() as zmax:
    #     config["components"]["ZMAX"]["settings"]["zmax"] = zmax

    #     ez.run(**collection_config.model_dump())


if __name__ == "__main__":
    main()
