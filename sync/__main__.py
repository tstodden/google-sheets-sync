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


async def main():
    logging.basicConfig(format=LOG_MSG_FORMAT, level=logging.INFO)

    creds = CredentialsController().get()
    spreadsheet_controller = SpreadsheetController(creds.oauth)
    postgres_controller = PostgresController(creds.postgres)

    with open(CONFIG_PATH, "r") as f:
        config_list = yaml.full_load(f)

    begin = time.perf_counter()
    for name in config_list:
        config = Config(config_list[name]) 
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


if __name__ == "__main__":
    asyncio.run(main())
