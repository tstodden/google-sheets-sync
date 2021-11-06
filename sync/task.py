import pickle
import uuid
from typing import List

from aiosqlite import Connection

from sync.models import Task


class TaskController:
    def __init__(self, connection: Connection):
        self.connection = connection

    async def create_task(self, json: dict) -> Task:
        task = Task(
            uuid=str(uuid.uuid4()),
            spreadsheet_id=json["spreadsheet_id"],
            target=json["target"],
            columns=json["columns"],
            keys=json.get("keys"),
            column_name_map=json.get("column_name_map"),
            column_dtype_map=json.get("column_dtype_map"),
        )
        blob = pickle.dumps(task)
        try:
            await self.connection.execute(
                "INSERT INTO tasks (uuid, task) VALUES (?, ?);",
                (
                    task.uuid,
                    blob,
                ),
            )
        except:
            await self.connection.rollback()
        else:
            await self.connection.commit()
        return task

    async def get_task(self, id_) -> Task | None:
        async with self.connection.execute(
            "SELECT uuid, task FROM tasks WHERE uuid = ?;", (id_,)
        ) as curs:
            row = await curs.fetchone()
            if row:
                return pickle.loads(row[1])
        return None

    async def update_task(self, id_) -> Task:
        pass

    async def delete_task(self, id_) -> None:
        pass

    async def get_all_tasks(self) -> List[Task]:
        pass

    async def initialize_database(self) -> None:
        await self.connection.execute(query)
        await self.connection.commit()


query = """
CREATE TABLE IF NOT EXISTS tasks
(
    uuid          TEXT PRIMARY KEY,
    task          BLOB,
    last_modified TEXT
);
"""
