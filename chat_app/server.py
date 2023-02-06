import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from chat_app.routers import (
    users, auth, login, profiles, messages, sessions, rooms, likes
)
from chat_app import dependencies
from chat_app.database import database, engine, Base
# from chat_app.users import models as users_models
# from chat_app.messages import models as messages_models
from chat_app.sio_server import sio_app
from chat_app.utils import templates
from chat_app.logger import setup_logger


setup_logger()

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(login.router)
app.include_router(profiles.router)
app.include_router(messages.router)
app.include_router(sessions.router)
app.include_router(rooms.router)
app.include_router(likes.router)


@app.on_event('startup')
async def startup():
    await database.connect()
    Base.metadata.create_all(bind=engine)


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
