import aiohttp
import os
import uvicorn
from fastapi import FastAPI, Request
from dotenv import load_dotenv

from balancer.logger import logger
from balancer.utils import choose_server, is_healthy
from balancer import requests


load_dotenv()

APP_HOST = os.getenv('APP_HOST')

app = FastAPI()


async def main_request(request: Request, path_name: str):
    port = choose_server()
    healthy = await is_healthy(port)
    while not healthy:
        port = choose_server()
        healthy = await is_healthy(port)
        logger.info(f'checking {port}')

    async with aiohttp.ClientSession() as session:
        url = f'http://{APP_HOST}:{port}/{path_name}'
        logger.info(f'Request to {url}')
        return await requests.types.get(request.method)(session, url, request)


@app.api_route("/{path_name:path}", methods=["GET", "DELETE", "POST", "PUT"])
async def catch_all_get_del(request: Request, path_name: str):
    return await main_request(request, path_name)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5004)
