import logging
from typing import List

from .models import Sheet


class SpreadsheetResponse:
    def __init__(self, metadata: dict):
        self.metadata = metadata
        self.contents = dict()
        self.is_valid = False

    def set_contents(self, contents: dict):
        self.contents = contents
        self.is_valid = True

    def get_sheet_titles(self) -> List[str]:
        sheets = self._get_property(self.metadata, "sheets")
        return [self._get_title(element) for element in sheets]

    def get_sheets(self) -> List[Sheet]:
        sheets: List[Sheet] = []
        value_ranges = self._get_property(self.contents, "valueRanges")
        for rng in value_ranges:
            new_rng = Sheet(
                title=self._get_range_title(rng), data=self._get_values(rng)
            )
            sheets.append(new_rng)
        return sheets

    def _get_title(self, response: dict) -> str:
        properties = self._get_property(response, "properties")
        title = self._get_property(properties, "title")
        return title

    def _get_range_title(self, element: dict):
        range_name = self._get_property(element, "range")
        return range_name.split("!")[0]

    def _get_values(self, element: dict):
        return self._get_property(element, "values")

    def _get_property(self, obj: dict, property: str) -> str:
        try:
            result = obj.get(property)
            if not result:
                raise KeyError()
        except KeyError:
            logging.exception(f"SpreadsheetResponse is missing {property}")
        return result
