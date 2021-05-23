import logging
from typing import List

from google.auth.credentials import Credentials as OAuthCredentials
from google.auth.transport.requests import AuthorizedSession

from .response import SpreadsheetResponse


class SpreadsheetController:
    def __init__(self, creds: OAuthCredentials):
        self.creds = creds
        self._session = AuthorizedSession(creds)

    def get_spreadsheet(self, id_: str) -> SpreadsheetResponse:
        metadata = self._get_spreadsheet_metadata(id_)
        response = SpreadsheetResponse(metadata=metadata)
        contents = self._get_spreadsheet_contents(
            id_=id_, sheets=response.get_sheet_titles()
        )
        response.set_contents(contents)
        return response

    def _get_spreadsheet_metadata(self, id_: str) -> dict:
        try:
            params = {"fields": "properties.title,sheets.properties.title"}
            response = self._session.get(
                f"https://sheets.googleapis.com/v4/spreadsheets/{id_}",
                params=params
            )
        except:
            logging.exception("Error executing API request")
        return response.json()

    def _get_spreadsheet_contents(self, id_: str, sheets: List[str]) -> dict:
        try:
            params = {
                "fields": "valueRanges(range,values)",
                "ranges": sheets
            }
            response = self._session.get(
                f"https://sheets.googleapis.com/v4/spreadsheets/{id_}/values:batchGet",
                params=params
            )
        except:
            logging.exception("Error executing API request")
        return response.json()
