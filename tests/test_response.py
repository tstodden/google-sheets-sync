from sync.models import Sheet
from sync.response import SpreadsheetResponse

METADATA = {
    "properties": {"title": "Animal Facts"},
    "sheets": [
        {"properties": {"title": "Sheet1"}},
        {"properties": {"title": "Sheet2"}}
    ]
}

CONTENTS = {
    "valueRanges": [{
        "range": "Sheet1!A1:Z999",
        "values": [
            ["animal", "description"],
            ["koala", "fuzzy, smol"]
        ]
    }, {
        "range": "Sheet2!A1:Z999",
        "values": [
            ["animal", "description"],
            ["elephant", "big nose, jumbo"]
        ]
    }]
}

EXPECTED_SHEET_1 = Sheet(
    title="Sheet1",
    data=[
        ["animal", "description"],
        ["koala", "fuzzy, smol"]
    ]
)

EXPECTED_SHEET_2 = Sheet(
    title="Sheet2",
    data=[
        ["animal", "description"],
        ["elephant", "big nose, jumbo"]
    ]
)


class TestSpreadsheetResponse:
    def test_getting_sheet_titles(self):
        sut = SpreadsheetResponse(METADATA)

        got = sut.get_sheet_titles()

        want = ["Sheet1", "Sheet2"]
        assert got == want

    def test_setting_contents(self):
        sut = SpreadsheetResponse(METADATA)

        sut.set_contents(CONTENTS)

        assert sut.is_valid == True and sut.contents == CONTENTS

    def test_getting_sheets(self):
        sut = SpreadsheetResponse(METADATA)
        sut.set_contents(CONTENTS)

        got = sut.get_sheets()

        want = [EXPECTED_SHEET_1, EXPECTED_SHEET_2]
        assert got == want
