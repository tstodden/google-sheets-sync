import logging
import json
from typing import List, Dict

from google.auth.transport._aiohttp_requests import AuthorizedSession, _CombinedResponse

from sync.models import Sheet

SHEETS_URL = "https://sheets.googleapis.com/v4/spreadsheets"
DRIVE_URL = "https://www.googleapis.com/drive/v3/files"
OAUTH_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
]


class SpreadsheetMetadata:
    def __init__(self, metadata: dict):
        self.metadata = metadata

    def get_sheet_title_list(self) -> List[str]:
        sheet_list = self.metadata["sheets"]
        return [sheet["properties"]["title"] for sheet in sheet_list]

    def __eq__(self, other):
        if isinstance(other, SpreadsheetMetadata):
            return self.metadata == other.metadata
        return False

    def __repr__(self):
        return f"SpreadsheetMetadata<metadata={self.metadata}>"


class SpreadsheetContent:
    def __init__(self, content: dict):
        self.content = content

    def get_sheet_list(self) -> List[Sheet]:
        sheet_list = []
        value_range_list = self.content["valueRanges"]
        for range_ in value_range_list:
            title, _ = range_["range"].split("!")
            values = range_["values"]
            sheet_list.append(Sheet(title, values))
        return sheet_list

    def __eq__(self, other):
        if isinstance(other, SpreadsheetContent):
            return self.content == other.content
        return False

    def __repr__(self):
        return f"SpreadsheetContent<content={self.content}>"


class Spreadsheet:
    def __init__(self, metadata: SpreadsheetMetadata, content: SpreadsheetContent):
        self.metadata = metadata
        self.content = content

    def __eq__(self, other):
        if isinstance(other, Spreadsheet):
            return self.metadata == other.metadata and self.content == other.content
        return False

    def __repr__(self):
        return f"Spreadsheet<metadata={self.metadata}, content={self.content}>"


class SpreadsheetController:
    def __init__(self, session: AuthorizedSession):
        self.session = session

    async def close(self):
        await self.session.close()

    async def get_spreadsheet(self, id_: str) -> Spreadsheet:
        metadata = await self._get_spreadsheet_metadata(id_)
        content = await self._get_spreadsheet_contents(
            id_=id_, sheets=metadata.get_sheet_title_list()
        )
        return Spreadsheet(metadata, content)

    async def get_spreadsheet_modified_time(self, id_: str) -> str:
        url = DRIVE_URL + f"/{id_}"
        params = {"fields": "modifiedTime"}
        resp = await self._try_get(url, params)
        return resp["modifiedTime"]

    async def _get_spreadsheet_metadata(self, id_: str) -> SpreadsheetMetadata:
        url = SHEETS_URL + f"/{id_}"
        params = {"fields": "properties.title,sheets.properties.title"}
        resp = await self._try_get(url, params)
        return SpreadsheetMetadata(resp)

    async def _get_spreadsheet_contents(
        self, id_: str, sheets: List[str]
    ) -> SpreadsheetContent:
        url = SHEETS_URL + f"/{id_}/values:batchGet"
        params = {"fields": "valueRanges(range,values)", "ranges": sheets}
        resp = await self._try_get(url, params)
        return SpreadsheetContent(resp)

    async def _try_get(self, url: str, params: Dict[str, str]) -> dict:
        logging.info({"requesting": url, "fields": params})
        try:
            resp = await self.session.request("GET", url, params=params)
            # decompression is not done properly by google.auth
            resp = _CombinedResponse(resp)
            assert resp.status == 200
        except Exception:
            raise
        else:
            data = await resp.content()
            return json.loads(data.decode("utf-8"))
