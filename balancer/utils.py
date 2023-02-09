import os
import random
import aiohttp
import asyncio

from balancer.logger import logger


HEALTH_CHECK_HOST = os.getenv('HEALTH_CHECK_HOST')


ports = {
    1: 5000,
    -1: 5001
}


def choose_server(port=None):
    if not port:
        choice = random.choice([1, -1])
        port = ports.get(choice)
    else:
        for value in ports.values():
            if value != port:
                port = value
    return port


async def is_healthy(port):
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        check_health_url = f'http://{HEALTH_CHECK_HOST}:{port}/health-check'
        logger.info(f'Request to {check_health_url}')
        try:
            async with session.get(check_health_url) as response:
                data = await response.json()
                logger.info(data)
                if data.get('health') != 'ok':
                    return False
                return True
        except (
            aiohttp.client_exceptions.ClientConnectorError,
            asyncio.TimeoutError
        ):
            return False
