curl -X POST http://localhost:8080/task \
    -H 'Content-Type: application/json' \
    -d '{"spreadsheet_id":"test","target":"target", "columns":["col1", "col2"]}'
