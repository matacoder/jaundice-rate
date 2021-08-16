import aiohttp
import asyncio
from loguru import logger

from adapters import SANITIZERS


async def fetch(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        logger.debug(response.host)
        html = await response.text()
        sanitized_text = SANITIZERS[response.host](html)
        return sanitized_text


async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, "https://inosmi.ru/politic/20210816/250319691.html")
        print(html)


asyncio.run(main())
