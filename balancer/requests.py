from fastapi import Response
from fastapi.responses import JSONResponse

from balancer.logger import logger


async def get(session, url, request):
    async with session.get(url) as response:
        content_type = response.content_type
        logger.info(f'{content_type}')
        if content_type == 'application/json':
            data = await response.json()
            return JSONResponse(data)
        return Response('')


async def post(session, url, request):
    request_data = await request.json()
    async with session.post(url, json=request_data) as response:
        content_type = response.content_type
        logger.info(f'{content_type}')
        if content_type == 'application/json':
            data = await response.json()
            return JSONResponse(data)
        return Response('')


async def put(session, url, request):
    request_data = await request.json()
    headers = {'authorization': request.headers.get('authorization')}
    async with session.put(
            url, json=request_data, headers=headers) as response:
        content_type = response.content_type
        logger.info(f'{content_type}')
        if content_type == 'application/json':
            data = await response.json()
            return JSONResponse(data)
        return Response('')


async def delete(session, url, request):
    headers = {'authorization': request.headers.get('authorization')}
    async with session.delete(
            url, headers=headers) as response:
        content_type = response.content_type
        logger.info(f'{content_type}')
        if content_type == 'application/json':
            data = await response.json()
            return JSONResponse(data)
        return Response('')


types = {
    'GET': get,
    'POST': post,
    'PUT': put,
    'DELETE': delete
}
