from sync.converter import Converter
from sync.models import DataType

from . import data


class TestConverter:
    def test_single_sheet_conversion(self):
        sheets = [data.BASIC_SHEET]
        sut = Converter(data.BASIC_TASK)

        got = sut.convert(sheets)

        want = [data.BASIC_RESULT]
        assert got == want

    def test_conversion_with_missing_key(self):
        sheets = [data.MISSING_KEY_SHEET]
        sut = Converter(data.BASIC_TASK)

        got = sut.convert(sheets)

        want = [data.MISSING_KEY_RESULT]
        assert got == want

    def test_conversion_with_duplicate_row(self):
        sheets = [data.DUPLICATE_SHEET]
        sut = Converter(data.BASIC_TASK)

        got = sut.convert(sheets)

        want = [data.DUPLICATE_RESULT]
        assert got == want

    def test_conversion_with_missing_value(self):
        sheets = [data.MISSING_VALUE_SHEET]
        sut = Converter(data.MISSING_TASK)

        got = sut.convert(sheets)

        want = [data.MISSING_VALUE_RESULT]
        assert got == want

    def test_conversion_with_column_def(self):
        sheets = [data.DATATYPE_MAP_SHEET]
        sut = Converter(data.DATATYPE_TASK)

        got = sut.convert(sheets)

        want = [data.DATATYPE_MAP_RESULT]
        assert got == want

    def test_conversion_with_column_rename_map(self):
        sheets = [data.RENAME_SHEET]
        sut = Converter(data.RENAME_TASK)

        got = sut.convert(sheets)

        want = [data.RENAME_RESULT]
        assert got == want
