import logging
from typing import Dict, List


class Config:
    def __init__(self, config: dict):
        self._config = config

    @property
    def spreadsheet_id(self) -> str:
        return self._get_required_property(self._config, "spreadsheet_id")

    @property
    def columns(self) -> List[str]:
        return self._get_required_property(self._config, "columns")

    @property
    def target(self) -> str:
        return self._get_required_property(self._config, "target")

    @property
    def type(self) -> str:
        return self._get_optional_property(self._config, "type")

    @property
    def keys(self) -> List[str]:
        return self._get_optional_property(self._config, "keys")

    @property
    def column_name_map(self) -> Dict[str, str]:
        return self._get_optional_property(self._config, "column_name_map")

    @property
    def column_dtype_map(self) -> Dict[str, str]:
        return self._get_optional_property(self._config, "column_dtype_map")

    @property
    def custom_values(self) -> Dict[str, str]:
        return self._get_optional_property(self._config, "custom_values")

    @property
    def validate(self) -> List[str]:
        return self._get_optional_property(self._config, "validate")

    @property
    def validate_target(self) -> str:
        return self._get_optional_property(self._config, "validate_target")

    @property
    def validate_fields(self) -> List[str]:
        return self._get_optional_property(self._config, "validate_fields")

    def _get_required_property(self, obj: dict, prop: str) -> str:
        try:
            result = obj.get(prop)
            if not result:
                raise KeyError()
        except KeyError:
            logging.exception(f"Config was missing {prop}")
        return result

    def _get_optional_property(self, obj: dict, prop: str) -> str:
        return obj.get(prop)
