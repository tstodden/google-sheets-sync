class ApplicationService:
    def __init__(self, creds: Credential):
        self.spreadsheet_controller = SpreadsheetController(creds.oath)
        self.postgres_controller = PostgresController(creds.postgres)
