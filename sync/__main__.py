import aiosqlite
from aiohttp import web

from sync.task import TaskController


routes = web.RouteTableDef()


@routes.get("/task/{id_}")
async def get_task(request: web.Request) -> web.Response:
    task = await request.app["task"].get_task(request.match_info["id_"])
    if task:
        return web.json_response(task.__dict__)
    return web.json_response({"error": "no task found"})


@routes.post("/task")
async def create_task(request: web.Request) -> web.Response:
    json = await request.json()
    task = await request.app["task"].create_task(json)
    return web.json_response(task.__dict__)


@routes.delete("/task/{id_}")
async def delete_task(request: web.Request) -> web.Response:
    await request.app["task"].delete_task(request.match_info["id_"])
    return web.Response()


async def task_controller(app):
    connection = await aiosqlite.connect("tasks.db")
    app["task"] = TaskController(connection)
    await app["task"].initialize_database()
    yield
    await connection.close()


app = web.Application()
app.add_routes(routes)
app.cleanup_ctx.append(task_controller)
web.run_app(app)
