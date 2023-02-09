import os
import uvicorn
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse

from balancer.logger import logger
from balancer.utils import choose_server, is_healthy


load_dotenv()

APP_HOST = os.getenv('APP_HOST')

app = FastAPI()


@app.api_route("/{path_name:path}", methods=["GET", "POST", "DELETE"])
async def catch_all(request: Request, path_name: str):
    port = choose_server()
    healthy = await is_healthy(port)
    while not healthy:
        port = choose_server()
        healthy = await is_healthy(port)
        logger.info(f'checking {port}')

    url = f'http://{APP_HOST}:{port}/{path_name}'
    logger.info(f'Request to {url}')
    if request.method == 'GET':
        return RedirectResponse(url)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5003)
