import logging
from typing import Dict, List, Tuple

from . import constants
from .auth import Credentials
from .config import Config
from .postgres import PostgresController
from .thread import SyncThread, SyncThreadFactory


class ApplicationService:
    def __init__(self, config: Dict[str, dict], creds: Credentials):
        self._config = config
        self._creds = creds
        self._threads: List[SyncThread] = []
        self._postgres_controller = self._initialize_postgres()

    def queueThreads(self):
        factory = SyncThreadFactory(
            postgres_controller=self._postgres_controller,
            credentials=self._creds.oauth
        )
        for name in self._config:
            thread = factory.create_thread(
                name=name,
                config=Config(config=self._config[name])
            )
            self._threads.append(thread)
            logging.info(f"{name} queued")

    def startThreads(self):
        logging.info("Starting execution...")
        for thread in self._threads:
            thread.start()
        for thread in self._threads:
            thread.join()
        complete, failed = self._complete()

        if complete > 0:
            logging.info(
                f"{complete}/{len(self._threads)} threads finished sucessfully"
            )
        if failed > 0:
            logging.error(
                constants.FAIL +
                f"{failed}/{len(self._threads)} threads failed" +
                constants.ENDC
            )

    def _complete(self) -> Tuple[int, int]:
        complete, failed = 0, 0
        for thr in self._threads:
            if thr.iscomplete == True:
                complete += 1
            else:
                failed += 1
        return complete, failed

    def _initialize_postgres(self) -> PostgresController:
        return PostgresController(self._creds.postgres)
