# Google Sheets Sync
An appliation for syncing Google Sheets content to a database table.
### Configuration
Configure jobs in `config.yml`:
```
# Example config.yml
Job Name:
  target: public.table_name (required)
  spreadsheet_id: unique Google Sheet identifier (required)
  columns: (required)
    - column_1
    - column_2
  keys:
    - column_1
  column_name_map:
    Column 1: column_1
    Column 2: column_2
  column_dtype_map:
    column_2: (int, float, datetime64)
  custom_values:
    column_3: Test Row
  validate:
    - column_1
  validate_target: public.validate_table
  validate_fields:
    - other_column
```
Set the following environment variables for a PostgreSQL database:
* `SYNC_DB_HOST`
* `SYNC_DB_NAME`
* `SYNC_DB_USER`
* `SYNC_DB_PASSWORD`
