import logging

import yaml

from .app import ApplicationService
from .auth import CredentialsController
from .constants import CONFIG_PATH, LOG_MSG_FORMAT


def main():
    logging.basicConfig(format=LOG_MSG_FORMAT, level=logging.INFO)

    creds = CredentialsController().get()
    with open(CONFIG_PATH, "r") as f:
        config = yaml.full_load(f)
    app = ApplicationService(config, creds)

    app.queueThreads()
    app.startThreads()


if __name__ == "__main__":
    main()
