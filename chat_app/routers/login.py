import aiohttp
import os

from fastapi import Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import APIRouter

from chat_app.utils import templates


router = APIRouter()


HOST = os.getenv('HOST')
API_PORT = os.getenv('API_PORT')
TOKEN_URL = f'http://{HOST}:{API_PORT}/token'
ACCESS_TOKEN_EXPIRE_SECONDS = 21600


@router.get('/login', response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html",
                                      {"request": request})


@router.post('/login', response_class=HTMLResponse)
async def login(username: str = Form(), password: str = Form()):
    data = {'username': username, 'password': password}
    async with aiohttp.ClientSession() as session:
        async with session.post(
                TOKEN_URL,
                data=data) as response:
            token_data = await response.json()
    token = token_data['access_token']
    redirect = RedirectResponse("/", status_code=303)
    redirect.set_cookie(
        key='access_token',
        value=token,
        expires=ACCESS_TOKEN_EXPIRE_SECONDS)
    return redirect
