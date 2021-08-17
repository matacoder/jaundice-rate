import aiohttp
import asyncio
from loguru import logger

from adapters import SANITIZERS
from bs4 import BeautifulSoup

from adapters.html_tools import remove_all_tags, remove_buzz_tags


async def fetch(session, url):
    async with session.get(url) as response:
        response.raise_for_status()

        html = await response.text()
        try:
            sanitized_text = SANITIZERS[response.host](html)
        except KeyError:
            logger.debug(f"{response.host} is not supported yet.")
            raise
        soap = BeautifulSoup(sanitized_text, "html.parser")
        cleaned_text = remove_all_tags(soap)
        return cleaned_text


async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, "https://inosmi.ru/politic/20210816/250319691.html")
        print(html)


asyncio.run(main())
