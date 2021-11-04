import logging
import time
import asyncio

import yaml

from sync.config import Config
from sync.converter import create_converter
from sync.postgres import PostgresController
from sync.spreadsheet import SpreadsheetController
from .auth import CredentialsController
from .constants import CONFIG_PATH, LOG_MSG_FORMAT


logging.basicConfig(format=LOG_MSG_FORMAT, level=logging.INFO)

creds = CredentialsController().get()
spreadsheet_controller = SpreadsheetController(creds.oauth)
postgres_controller = PostgresController(creds.postgres)


async def run(config: Config, begin: float) -> None:
    try:
        response = spreadsheet_controller.get_spreadsheet(id_=config.spreadsheet_id)
        converter = create_converter(config)
        if config.validate:
            validator = postgres_controller.get_validator(config)
            converter.set_validator(validator)
        sets = converter.convert(response.get_sheets())
        postgres_controller.update(config.target, sets)

        end = time.perf_counter()
        logging.info(f"Completed in {end - begin:.2f} sec")
    except:
        logging.exception("Failed")


async def main():
    with open(CONFIG_PATH, "r") as f:
        config_file = yaml.full_load(f)
    config_list = [Config(config_file[job]) for job in config_file]

    begin = time.perf_counter()
    asyncio.gather(*[run(config, begin) for config in config_list])


if __name__ == "__main__":
    asyncio.run(main())
