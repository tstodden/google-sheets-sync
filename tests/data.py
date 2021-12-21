import pandas as pd
from sync.models import DataSet, Sheet, Task, DataType

BASIC_TASK = Task.from_dict(
    {
        "spreadsheet_id": "1",
        "table": "test",
        "column_def": {"animal": DataType.STRING, "description": DataType.STRING},
        "key_list": ["animal"],
    }
)

BASIC_SHEET = Sheet(
    title="Sheet1",
    data=[
        ["animal", "description"],
        ["koala", "fuzzy, smol"],
        ["elephant", "big nose, jumbo"],
    ],
)

BASIC_RESULT = DataSet(
    name="Sheet1",
    dataframe=pd.DataFrame(
        columns=["animal", "description"],
        data=[["koala", "fuzzy, smol"], ["elephant", "big nose, jumbo"]],
    ),
)

MISSING_KEY_SHEET = Sheet(
    title="Sheet1",
    data=[["animal", "description"], ["koala", "fuzzy, smol"], ["", "good at hiding"]],
)

MISSING_KEY_RESULT = DataSet(
    name="Sheet1",
    dataframe=pd.DataFrame(
        columns=["animal", "description"], data=[["koala", "fuzzy, smol"]]
    ),
)

DUPLICATE_SHEET = Sheet(
    title="Sheet1",
    data=[
        ["animal", "description"],
        ["koala", "fuzzy, smol"],
        ["koala", "fuzzy, smol"],
    ],
)

DUPLICATE_RESULT = MISSING_KEY_RESULT

MISSING_TASK = Task.from_dict(
    {
        "spreadsheet_id": "1",
        "table": "test",
        "column_def": {
            "animal": DataType.STRING,
            "description": DataType.STRING,
            "friends": DataType.STRING,
        },
    }
)

MISSING_VALUE_SHEET = Sheet(
    title="Sheet1",
    data=[
        ["animal", "description", "friends"],
        ["koala", "", "octopus"],
        ["elephant", "big nose, jumbo", "giraffe, zebra"],
    ],
)

MISSING_VALUE_RESULT = DataSet(
    name="Sheet1",
    dataframe=pd.DataFrame(
        columns=["animal", "description", "friends"],
        data=[
            ["koala", None, "octopus"],
            ["elephant", "big nose, jumbo", "giraffe, zebra"],
        ],
    ),
)

DATATYPE_TASK = Task.from_dict(
    {
        "spreadsheet_id": "1",
        "table": "test",
        "column_def": {
            "animal": DataType.STRING,
            "description": DataType.STRING,
            "last_seen": DataType.DATETIME,
            "lifespan": DataType.FLOAT,
        },
        "key_list": ["animal"],
    }
)

DATATYPE_MAP_SHEET = Sheet(
    title="Sheet1",
    data=[
        ["animal", "description", "last_seen", "lifespan"],
        ["koala", "fuzzy, smol", "1/8/2021", "#15.07"],
        ["elephant", "big nose, jumbo", "03/5/2020", "$65.74"],
    ],
)

DATATYPE_MAP_RESULT = DataSet(
    name="Sheet1",
    dataframe=pd.DataFrame(
        columns=["animal", "description", "last_seen", "lifespan"],
        data=[
            ["koala", "fuzzy, smol", "2021-01-08T00:00:00+00:00", 15.07],
            ["elephant", "big nose, jumbo", "2020-03-05T00:00:00+00:00", 65.74],
        ],
    ).astype(object),
)

RENAME_TASK = Task.from_dict(
    {
        "spreadsheet_id": "1",
        "table": "test",
        "column_def": {"animal": DataType.STRING, "description": DataType.STRING},
        "column_rename_map": {"Pokemon": "animal"},
    }
)

RENAME_SHEET = Sheet(
    title="Sheet1",
    data=[
        ["Pokemon", "description"],
        ["koala", "fuzzy, smol"],
        ["elephant", "big nose, jumbo"],
    ],
)

RENAME_RESULT = DataSet(
    name="Sheet1",
    dataframe=pd.DataFrame(
        columns=["animal", "description"],
        data=[["koala", "fuzzy, smol"], ["elephant", "big nose, jumbo"]],
    ),
)
