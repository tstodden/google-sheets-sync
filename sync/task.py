import pickle
import uuid
from typing import List

from aiosqlite import Connection

from sync.models import Task

MUTABLE_FIELDS = [
    "spreadsheet_id",
    "target",
    "columns",
    "keys",
    "column_name_map",
    "column_dtype_map",
]


class TaskController:
    def __init__(self, connection: Connection):
        self.connection = connection

    async def create_task(self, req: dict) -> Task:
        task = Task(
            uuid=str(uuid.uuid4()),
            spreadsheet_id=req["spreadsheet_id"],
            target=req["target"],
            columns=req["columns"],
            keys=req.get("keys"),
            column_name_map=req.get("column_name_map"),
            column_dtype_map=req.get("column_dtype_map"),
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

    async def get_task(self, id_) -> Task:
        async with self.connection.execute(
            "SELECT uuid, task FROM tasks WHERE uuid = ?;", (id_,)
        ) as curs:
            row = await curs.fetchone()

        if not row:
            raise NameError("task not found")

        _, task = row
        return pickle.loads(task)

    async def update_task(self, id_: str, req: dict) -> Task:
        if (task := await self.get_task(id_)) is None:
            raise NameError("key not found")

        for key, data in req.items():
            if key in MUTABLE_FIELDS:
                task[key] = data
            else:
                raise KeyError(f"{key} is not valid")

        blob = pickle.dumps(task)
        try:
            await self.connection.execute(
                "UPDATE tasks SET task = ? WHERE uuid = ?;", (blob, id_)
            )
        except:
            await self.connection.rollback()
        else:
            await self.connection.commit()
        return task

    async def delete_task(self, id_) -> None:
        try:
            await self.connection.execute("DELETE FROM tasks WHERE uuid = ?;", (id_,))
        except:
            await self.connection.rollback()
        else:
            await self.connection.commit()

    async def get_all_tasks(self) -> List[Task]:
        all_tasks = []
        async with self.connection.execute("SELECT uuid, task FROM tasks;") as curs:
            row_list = await curs.fetchall()

        if not row_list:
            return all_tasks

        for row in row_list:
            _, task = row
            all_tasks.append(pickle.loads(task))
        return all_tasks

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
