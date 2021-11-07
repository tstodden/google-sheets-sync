import aiosqlite
from aiohttp import web

from google.oauth2._service_account_async import Credentials
from google.auth.transport._aiohttp_requests import AuthorizedSession

from sync.spreadsheet import SpreadsheetController, OAUTH_SCOPES
from sync.task import TaskController


routes = web.RouteTableDef()


@routes.post("/task")
async def create_task(request: web.Request) -> web.Response:
    json = await request.json()
    try:
        task = await request.app["task"].create_task(json)
    except KeyError as e:
        return web.json_response({"error": str(e)})
    else:
        return web.json_response(task.__dict__)


@routes.get("/task/{id_}")
async def get_task(request: web.Request) -> web.Response:
    try:
        task = await request.app["task"].get_task(request.match_info["id_"])
    except NameError as e:
        return web.json_response({"error": str(e)})
    else:
        return web.json_response(task.__dict__)


@routes.patch("/task/{id_}")
async def update_task(request: web.Request) -> web.Response:
    json = await request.json()
    try:
        task = await request.app["task"].update_task(request.match_info["id_"], json)
    except Exception as e:
        return web.json_response({"error": str(e)})
    else:
        return web.json_response(task.__dict__)


@routes.delete("/task/{id_}")
async def delete_task(request: web.Request) -> web.Response:
    await request.app["task"].delete_task(request.match_info["id_"])
    return web.Response()


@routes.get("/all-tasks")
async def get_all_tasks(request: web.Request) -> web.Response:
    all_tasks = await request.app["task"].get_all_tasks()
    task_dicts = [task.__dict__ for task in all_tasks]
    return web.json_response(task_dicts)


async def task_controller(app):
    connection = await aiosqlite.connect("tasks.db")
    app["task"] = TaskController(connection)
    await app["task"].initialize_database()
    yield
    await connection.close()


async def spreadsheet_controller(app):
    credentials = Credentials.from_service_account_file(
        "service-account.json", scopes=OAUTH_SCOPES
    )
    session = AuthorizedSession(credentials)
    app["spreadsheet"] = SpreadsheetController(session)
    yield
    await app["spreadsheet"].close()


app = web.Application()
app.add_routes(routes)
app.cleanup_ctx.append(task_controller)
app.cleanup_ctx.append(spreadsheet_controller)
web.run_app(app)
