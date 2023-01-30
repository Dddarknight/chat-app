import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from chat_app.routers import users as users_routers
from chat_app.routers import login as login_routers
from chat_app.routers import messages as messages_routers
from chat_app import dependencies
from chat_app.database import database, engine
from chat_app.users import models as users_models
from chat_app.messages import models as messages_models
from chat_app.sio_server import sio_app
from chat_app.utils import templates
from chat_app.logger import setup_logger


setup_logger()

app = FastAPI()

app.include_router(users_routers.router)
app.include_router(login_routers.router)
app.include_router(messages_routers.router)


@app.on_event('startup')
async def startup():
    await database.connect()
    users_models.Base.metadata.create_all(bind=engine)
    messages_models.Base.metadata.create_all(bind=engine)


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get('/', response_class=HTMLResponse)
async def index(request: Request,
                db: Session = Depends(dependencies.get_db)):
    user = dependencies.get_current_user(
        db, token=request.cookies.get('access_token'))
    response = templates.TemplateResponse(
        "chat.html",
        {"request": request, "user": user.username})
    return response


app.mount("/", sio_app)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
