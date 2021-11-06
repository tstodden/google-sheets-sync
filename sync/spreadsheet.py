import logging
from typing import List

from google.auth.credentials import Credentials as OAuthCredentials
from google.auth.transport._aiohttp_requests import AuthorizedSession

from sync.response import SpreadsheetResponse


class SpreadsheetController:
    def __init__(self, creds: OAuthCredentials):
        self.creds = creds
        self._session = AuthorizedSession(creds)

    async def close(self):
        await self._session.close()

    async def get_spreadsheet(self, id_: str) -> SpreadsheetResponse:
        metadata = await self._get_spreadsheet_metadata(id_)
        response = SpreadsheetResponse(metadata=metadata)
        contents = await self._get_spreadsheet_contents(
            id_=id_, sheets=response.get_sheet_titles()
        )
        response.set_contents(contents)
        return response

    async def _get_spreadsheet_metadata(self, id_: str) -> dict:
        params = {"fields": "properties.title,sheets.properties.title"}
        try:
            async with self._session.get(
                f"https://sheets.googleapis.com/v4/spreadsheets/{id_}", params=params
            ) as resp:
                assert resp.status == 200
                response = await resp.json()
        except:
            raise
        else:
            return response.json()

    async def _get_spreadsheet_contents(self, id_: str, sheets: List[str]) -> dict:
        params = {"fields": "valueRanges(range,values)", "ranges": sheets}
        try:

            async with self._session.get(
                f"https://sheets.googleapis.com/v4/spreadsheets/{id_}/values:batchGet",
                params=params,
            ) as resp:
                assert resp.status == 200
                response = await resp.json()
        except:
            raise
        else:
            return response.json()
