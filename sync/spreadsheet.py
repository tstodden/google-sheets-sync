from dataclasses import dataclass
import logging
import json

from google.auth.transport._aiohttp_requests import AuthorizedSession, _CombinedResponse

from sync.models import Sheet

SHEETS_URL = "https://sheets.googleapis.com/v4/spreadsheets"
DRIVE_URL = "https://www.googleapis.com/drive/v3/files"
OAUTH_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.metadata.readonly",
]


@dataclass
class SpreadsheetMetadata:
    metadata: dict

    def get_sheet_title_list(self) -> list[str]:
        sheet_list = self.metadata["sheets"]
        return [sheet["properties"]["title"] for sheet in sheet_list]


@dataclass
class SpreadsheetContent:
    content: dict

    def get_sheet_list(self) -> list[Sheet]:
        sheet_list = []
        value_range_list = self.content["valueRanges"]
        for range_ in value_range_list:
            title, _ = range_["range"].split("!")
            values = range_["values"]
            sheet_list.append(Sheet(title, values))
        return sheet_list


@dataclass
class Spreadsheet:
    metadata: SpreadsheetMetadata
    content: SpreadsheetContent


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
        self, id_: str, sheets: list[str]
    ) -> SpreadsheetContent:
        url = SHEETS_URL + f"/{id_}/values:batchGet"
        params = {"fields": "valueRanges(range,values)", "ranges": sheets}
        resp = await self._try_get(url, params)
        return SpreadsheetContent(resp)

    async def _try_get(self, url: str, params: dict[str, str]) -> dict:
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
            if not data:
                raise ValueError("GET {url} response empty")
            return json.loads(data.decode("utf-8"))
