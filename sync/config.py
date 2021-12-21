class Config:
    def __init__(self, config: dict):
        self.config = config

    @property
    def spreadsheet_id(self) -> str:
        return self.config["spreadsheet_id"]

    @property
    def columns(self) -> list[str]:
        return self.config["columns"]

    @property
    def target(self) -> str:
        return self.config["target"]

    @property
    def type(self) -> str | None:
        return self.config.get("type")

    @property
    def keys(self) -> list[str] | None:
        return self.config.get("keys")

    @property
    def column_name_map(self) -> dict[str, str] | None:
        return self.config.get("column_name_map")

    @property
    def column_dtype_map(self) -> dict[str, str] | None:
        return self.config.get("column_dtype_map")

    @property
    def custom_values(self) -> dict[str, str] | None:
        return self.config.get("custom_values")
