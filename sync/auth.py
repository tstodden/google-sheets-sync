import os
from typing import NamedTuple

from google.oauth2.service_account import Credentials as OAuthCredentials

from .constants import OAUTH_CONFIG_PATH, OAUTH_SCOPES


class PostgresCredentials:
    def __init__(self):
        self.host = os.environ.get("SYNC_DB_HOST")
        self.dbname = os.environ.get("SYNC_DB_NAME")
        self.user = os.environ.get("SYNC_DB_USER")
        self.password = os.environ.get("SYNC_DB_PASSWORD")


class Credentials(NamedTuple):
    postgres: PostgresCredentials
    oauth: OAuthCredentials


class CredentialsController:
    def get(self) -> Credentials:
        credentials = Credentials(
            postgres=PostgresCredentials(), oauth=self._get_creds_from_google()
        )
        return credentials

    def _get_creds_from_google(self) -> OAuthCredentials:
        credentials = OAuthCredentials.from_service_account_file(
            OAUTH_CONFIG_PATH, scopes=OAUTH_SCOPES
        )
        return credentials
