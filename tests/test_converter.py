from sync.converter import create_converter
from sync.validator import Validator

from . import data


class TestConverter:
    def test_single_sheet_conversion(self):
        sheets = [data.BASIC_SHEET]
        sut = create_converter(data.BASIC_CONFIG)

        got = sut.convert(sheets)

        want = [data.BASIC_RESULT]
        assert got == want

    def test_conversion_with_missing_key(self):
        sheets = [data.MISSING_KEY_SHEET]
        sut = create_converter(data.BASIC_CONFIG)

        got = sut.convert(sheets)

        want = [data.MISSING_KEY_RESULT]
        assert got == want

    def test_conversion_with_duplicate_row(self):
        sheets = [data.DUPLICATE_SHEET]
        sut = create_converter(data.BASIC_CONFIG)

        got = sut.convert(sheets)

        want = [data.DUPLICATE_RESULT]
        assert got == want

    def test_conversion_with_missing_value(self):
        sheets = [data.MISSING_VALUE_SHEET]
        sut = create_converter(data.MISSING_CONFIG)

        got = sut.convert(sheets)

        want = [data.MISSING_VALUE_RESULT]
        assert got == want

    def test_conversion_with_dtype_map(self):
        sheets = [data.DATATYPE_MAP_SHEET]
        sut = create_converter(data.DATATYPE_CONFIG)

        got = sut.convert(sheets)

        want = [data.DATATYPE_MAP_RESULT]
        assert got == want

    def test_conversion_with_custom_values(self):
        sheets = [data.CUSTOM_VALUE_SHEET]
        sut = create_converter(data.CUSTOM_VALUE_CONFIG)

        got = sut.convert(sheets)

        want = [data.CUSTOM_VALUE_RESULT]
        assert got == want

    def test_conversion_with_column_name_map(self):
        sheets = [data.RENAME_SHEET]
        sut = create_converter(data.RENAME_CONFIG)

        got = sut.convert(sheets)

        want = [data.RENAME_RESULT]
        assert got == want

    def test_conversion_with_validation(self):
        sheets = [data.VALIDATE_SHEET]
        validator = Validator(data.VALIDATE_CONFIG, {("koala",)})
        sut = create_converter(data.VALIDATE_CONFIG)
        sut.set_validator(validator)

        got = sut.convert(sheets)

        want = [data.VALIDATE_RESULT]
        assert got == want
