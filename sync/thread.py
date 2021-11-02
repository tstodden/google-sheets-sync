import logging
import threading
import time

from google.auth.credentials import Credentials as OAuthCredentials

from . import constants
from .config import Config
from .converter import create_converter
from .postgres import PostgresController
from .spreadsheet import SpreadsheetController


class SyncThread(threading.Thread):
    def __init__(
        self,
        name: str,
        config: Config,
        postgres_controller: PostgresController,
        spreadsheet_controller: SpreadsheetController,
    ):
        super().__init__(target=self.run, name=name)
        self.config = config
        self.postgres_controller = postgres_controller
        self.spreadsheet_controller = spreadsheet_controller
        self._iscomplete = False

    @property
    def iscomplete(self) -> bool:
        return self._iscomplete

    def run(self):
        begin = time.perf_counter()
        try:
            response = self.spreadsheet_controller.get_spreadsheet(
                id_=self.config.spreadsheet_id
            )
            converter = create_converter(self.config)
            if self.config.validate:
                validator = self.postgres_controller.get_validator(self.config)
                converter.set_validator(validator)
            sets = converter.convert(response.get_sheets())
            self.postgres_controller.update(self.config.target, sets)

            end = time.perf_counter()
            logging.info(
                constants.OKGREEN
                + f"Completed in {end - begin:.2f} sec"
                + constants.ENDC
            )
            self._iscomplete = True
        except:
            logging.exception(constants.FAIL + "Failed" + constants.ENDC)


class SyncThreadFactory:
    def __init__(
        self, postgres_controller: PostgresController, credentials: OAuthCredentials
    ):
        self.postgres_controller = postgres_controller
        self.credentials = credentials

    def create_thread(self, name: str, config: Config) -> SyncThread:
        return SyncThread(
            name=name,
            config=config,
            postgres_controller=self.postgres_controller,
            spreadsheet_controller=SpreadsheetController(self.credentials),
        )
