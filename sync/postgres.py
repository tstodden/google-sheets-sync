import logging
from typing import List

import pandas as pd
import psycopg2
from psycopg2 import extras
from psycopg2.pool import ThreadedConnectionPool

from .auth import PostgresCredentials
from .config import Config
from .models import DataSet
from .validator import Validator


class PostgresController:
    def __init__(self, creds: PostgresCredentials):
        self._creds = creds
        self._dbpool = self._initialize_pool()

    def update(self, target: str, datasets: List[DataSet]):
        try:
            conn = self._dbpool.getconn()
        except:
            logging.exception("Error connecting to database")
        for ds in datasets:
            self._update_dataset(conn, target, ds)
        self._dbpool.putconn(conn)

    def get_validator(self, config: Config) -> Validator:
        try:
            conn = self._dbpool.getconn()
            curs = conn.cursor()
            fields = ','.join(config.validate_fields)
            curs.execute(
                f"SELECT DISTINCT {fields} FROM {config.validate_target};"
            )
            values = curs.fetchall()
            conn.commit()
        except:
            logging.exception("Error creating validator")
            conn.rollback()
        self._dbpool.putconn(conn)
        return Validator(config, set(values))

    def _update_dataset(self, conn, target: str, dataset: DataSet):
        title, df = dataset
        curs = conn.cursor()
        try:
            self._delete_data_from_target(curs, target)
            self._insert_dataframe_into_target(curs, target, df)
            conn.commit()
        except psycopg2.Error:
            logging.exception("Error updating database")
            conn.rollback()
        curs.close()

    def _insert_dataframe_into_target(self, curs, target: str, df: pd.DataFrame) -> str:
        tuples = df.itertuples(index=False, name=None)
        cols = ','.join(list(df.columns))
        query = f"INSERT INTO {target} ({cols}) VALUES %s"
        extras.execute_values(curs, query, tuples, page_size=800)

    def _delete_data_from_target(self, curs, target: str):
        curs.execute(self._delete(target))

    def _delete(self, tablename: str) -> str:
        return f"DELETE FROM {tablename};"

    def _initialize_pool(self) -> ThreadedConnectionPool:
        return ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host=self._creds.host,
            dbname=self._creds.dbname,
            user=self._creds.user,
            password=self._creds.password,
        )
