import pickle
from typing import List

import aiosqlite

from sync.models import Task

MUTABLE_FIELDS = [
    "spreadsheet_id",
    "table",
    "column_def",
    "key_list",
    "column_rename_map",
]


class TaskController:
    def __init__(self, conn: aiosqlite.Connection):
        self.conn = conn

    @classmethod
    async def from_path(cls, path: str) -> "TaskController":
        conn = await aiosqlite.connect(path)
        controller = cls(conn)
        await controller._initialize_database()
        return controller

    async def close(self) -> None:
        await self.conn.close()

    async def create_task(self, json: dict) -> Task:
        task = Task.from_dict(json)
        try:
            await self._insert_new_task(task)
        except:
            await self.conn.rollback()
        else:
            await self.conn.commit()
        return task

    async def get_task(self, id_) -> Task:
        get_query = "SELECT uuid, task FROM tasks WHERE uuid = ?;"
        async with self.conn.execute(get_query, (id_,)) as curs:
            row = await curs.fetchone()
        if not row:
            raise NameError("task not found")

        _, task = row
        return pickle.loads(task)

    async def update_task(self, id_: str, json: dict) -> Task:
        if (task := await self.get_task(id_)) is None:
            raise NameError("key not found")
        task = self._update_mutable_fields(task, json)

        try:
            await self._update_task(task, id_)
        except:
            await self.conn.rollback()
        else:
            await self.conn.commit()
        return task

    async def delete_task(self, id_) -> None:
        delete_query = "DELETE FROM tasks WHERE uuid = ?;"
        try:
            await self.conn.execute(delete_query, (id_,))
        except:
            await self.conn.rollback()
        else:
            await self.conn.commit()

    async def get_all_tasks(self) -> List[Task]:
        get_all_query = "SELECT uuid, task FROM tasks;"
        all_tasks = []
        async with self.conn.execute(get_all_query) as curs:
            row_list = await curs.fetchall()

        if not row_list:
            return all_tasks

        for row in row_list:
            _, task = row
            all_tasks.append(pickle.loads(task))
        return all_tasks

    async def _initialize_database(self) -> None:
        initialization_query = """
        CREATE TABLE IF NOT EXISTS tasks
        (
            uuid          TEXT PRIMARY KEY,
            task          BLOB,
            last_modified TEXT
        );
        """
        await self.conn.execute(initialization_query)
        await self.conn.commit()

    async def _insert_new_task(self, task: Task) -> None:
        insert_query = "INSERT INTO tasks (uuid, task) VALUES (?, ?);"
        blob = pickle.dumps(task)
        await self.conn.execute(insert_query, (task.uuid, blob))

    async def _update_task(self, task: Task, id_: str) -> None:
        update_query = "UPDATE tasks SET task = ? WHERE uuid = ?;"
        blob = pickle.dumps(task)
        await self.conn.execute(update_query, (blob, id_))

    def _update_mutable_fields(self, task: Task, json: dict) -> Task:
        for key, data in json.items():
            if key in MUTABLE_FIELDS:
                task[key] = data
            else:
                raise KeyError(f"{key} is not valid")
        return task
