import pandas as pd
from sync.config import Config
from sync.models import DataSet, Sheet

BASIC_CONFIG = Config({
    "columns": ["animal", "description"],
    "keys": ["animal"]
})

BASIC_SHEET = Sheet(
    title="Sheet1",
    data=[
        ["animal", "description"],
        ["koala", "fuzzy, smol"],
        ["elephant", "big nose, jumbo"]
    ]
)

BASIC_RESULT = DataSet(
    name="Sheet1",
    dataframe=pd.DataFrame(
        columns=["animal", "description"],
        data=[
            ["koala", "fuzzy, smol"],
            ["elephant", "big nose, jumbo"]
        ])
)

MISSING_KEY_SHEET = Sheet(
    title="Sheet1",
    data=[
        ["animal", "description"],
        ["koala", "fuzzy, smol"],
        ["", "good at hiding"]
    ]
)

MISSING_KEY_RESULT = DataSet(
    name="Sheet1",
    dataframe=pd.DataFrame(
        columns=["animal", "description"],
        data=[
            ["koala", "fuzzy, smol"]
        ])
)

DUPLICATE_SHEET = Sheet(
    title="Sheet1",
    data=[
        ["animal", "description"],
        ["koala", "fuzzy, smol"],
        ["koala", "fuzzy, smol"]
    ]
)

DUPLICATE_RESULT = MISSING_KEY_RESULT

MISSING_CONFIG = Config({
    "columns": ["animal", "description", "friends"]
})

MISSING_VALUE_SHEET = Sheet(
    title="Sheet1",
    data=[
        ["animal", "description", "friends"],
        ["koala", "", "octopus"],
        ["elephant", "big nose, jumbo", "giraffe, zebra"]
    ]
)

MISSING_VALUE_RESULT = DataSet(
    name="Sheet1",
    dataframe=pd.DataFrame(
        columns=[
            "animal", "description", "friends"
        ],
        data=[
            ["koala", None, "octopus"],
            ["elephant", "big nose, jumbo", "giraffe, zebra"]
        ])
)

DATATYPE_CONFIG = Config({
    "columns": ["animal", "description", "last_seen", "lifespan"],
    "keys": ["animal"],
    "column_dtype_map": {"last_seen": "datetime64", "lifespan": "float"}
})

DATATYPE_MAP_SHEET = Sheet(
    title="Sheet1",
    data=[
        ["animal", "description", "last_seen", "lifespan"],
        ["koala", "fuzzy, smol", "1/8/2021", "#15.07"],
        ["elephant", "big nose, jumbo", "03/5/2020", "$65.74"]
    ]
)

DATATYPE_MAP_RESULT = DataSet(
    name="Sheet1",
    dataframe=pd.DataFrame(
        columns=["animal", "description", "last_seen", "lifespan"],
        data=[
            ["koala", "fuzzy, smol", "2021-01-08", "15.07"],
            ["elephant", "big nose, jumbo", "2020-03-05", "65.74"]
        ]
    ).astype(
        {"last_seen": "datetime64", "lifespan": "float"}
    ).astype(object)
)

CUSTOM_VALUE_CONFIG = Config({
    "columns": ["animal", "description"],
    "custom_values": {"description": "fav 💖"}
})

CUSTOM_VALUE_SHEET = Sheet(
    title="Sheet1",
    data=[
        ["animal"],
        ["koala"],
        ["elephant"]
    ]
)

CUSTOM_VALUE_RESULT = DataSet(
    name="Sheet1",
    dataframe=pd.DataFrame(
        columns=[
            "animal", "description"
        ],
        data=[
            ["koala", "fav 💖"],
            ["elephant", "fav 💖"]
        ])
)

RENAME_CONFIG = Config({
    "columns": ["animal", "description"],
    "column_name_map": {"Pokemon": "animal"}
})

RENAME_SHEET = Sheet(
    title="Sheet1",
    data=[
        ["Pokemon", "description"],
        ["koala", "fuzzy, smol"],
        ["elephant", "big nose, jumbo"]
    ]
)

RENAME_RESULT = DataSet(
    name="Sheet1",
    dataframe=pd.DataFrame(
        columns=[
            "animal", "description"
        ],
        data=[
            ["koala", "fuzzy, smol"],
            ["elephant", "big nose, jumbo"]
        ])
)

VALIDATE_CONFIG = Config({
    "columns": ["animal", "description"],
    "keys": ["animal"],
    "validate": ["animal"],
})

VALIDATE_SHEET = BASIC_SHEET

VALIDATE_RESULT = DataSet(
    name="Sheet1",
    dataframe=pd.DataFrame(
        columns=["animal", "description"],
        data=[
            ["koala", "fuzzy, smol"]
        ])
)
