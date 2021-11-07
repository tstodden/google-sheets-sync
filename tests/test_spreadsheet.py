import pytest

from google.oauth2._service_account_async import Credentials
from google.auth.transport._aiohttp_requests import AuthorizedSession

from sync.models import Sheet
from sync.spreadsheet import (
    SpreadsheetController,
    Spreadsheet,
    SpreadsheetMetadata,
    SpreadsheetContent,
    OAUTH_SCOPES,
)

TEST_SPREADSHEET_ID = "1o8l4RA3d4LEchi81mJP6wUDZI6HatT9MKRQ2wyTeNa4"


@pytest.fixture
async def spreadsheet_controller():
    credentials = Credentials.from_service_account_file(
        "service-account.json", scopes=OAUTH_SCOPES
    )
    session = AuthorizedSession(credentials)
    spreadsheet_controller = SpreadsheetController(session)
    yield spreadsheet_controller
    await spreadsheet_controller.close()


class TestSpreadsheetController:
    @pytest.mark.asyncio
    async def test_get_spreadsheet_modified_time(self, spreadsheet_controller):
        got = await spreadsheet_controller.get_spreadsheet_modified_time(
            TEST_SPREADSHEET_ID
        )

        want = "2021-11-07T18:38:18.162Z"
        assert got == want

    @pytest.mark.asyncio
    async def test_get_spreadsheet(self, spreadsheet_controller):
        metadata = SpreadsheetMetadata(
            {
                "properties": {"title": "Integration Test [Do Not Modify]"},
                "sheets": [{"properties": {"title": "Sheet1"}}],
            }
        )
        content = SpreadsheetContent(
            {
                "valueRanges": [
                    {
                        "range": "Sheet1!A1:Z1000",
                        "values": [
                            ["col1", "col2", "col3"],
                            ["a", "b", "c"],
                            ["d", "e", "f"],
                        ],
                    }
                ]
            }
        )

        got = await spreadsheet_controller.get_spreadsheet(TEST_SPREADSHEET_ID)

        want = Spreadsheet(metadata, content)
        assert got == want


class TestSpreadsheetMetadata:
    def test_get_sheet_title_list(self):
        metadata = {
            "properties": {"title": "Animal Facts"},
            "sheets": [
                {"properties": {"title": "Sheet1"}},
                {"properties": {"title": "Sheet2"}},
            ],
        }
        sut = SpreadsheetMetadata(metadata)

        got = sut.get_sheet_title_list()

        want = ["Sheet1", "Sheet2"]
        assert got == want


class TestSpreadsheetContent:
    def test_get_sheet_list(self):
        content = {
            "valueRanges": [
                {
                    "range": "Sheet1!A1:Z999",
                    "values": [["animal", "description"], ["koala", "fuzzy, smol"]],
                },
                {
                    "range": "Sheet2!A1:Z999",
                    "values": [
                        ["animal", "description"],
                        ["elephant", "big nose, jumbo"],
                    ],
                },
            ]
        }
        sut = SpreadsheetContent(content)

        got = sut.get_sheet_list()

        expected_sheet_1 = Sheet(
            title="Sheet1", data=[["animal", "description"], ["koala", "fuzzy, smol"]]
        )
        expected_sheet_2 = Sheet(
            title="Sheet2",
            data=[["animal", "description"], ["elephant", "big nose, jumbo"]],
        )
        want = [expected_sheet_1, expected_sheet_2]
        assert got == want
