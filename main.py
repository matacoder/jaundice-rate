import aiohttp
import asyncio

import pymorphy2
from loguru import logger

from adapters import SANITIZERS
from bs4 import BeautifulSoup

from adapters.html_tools import remove_all_tags, remove_buzz_tags
from text_tools import split_by_words


async def fetch(session, url):
    async with session.get(url) as response:
        response.raise_for_status()

        return await response.text(), response.host


async def main():
    async with aiohttp.ClientSession() as session:
        html, host = await fetch(
            session, "https://inosmi.ru/politic/20210816/250319691.html"
        )
        # print(html)
        try:
            sanitized_text = SANITIZERS[host](html)
        except KeyError:
            logger.debug(f"{host} is not supported yet.")
            raise
        soap = BeautifulSoup(sanitized_text, "html.parser")
        cleaned_text = remove_all_tags(soap)
        morph = pymorphy2.MorphAnalyzer()

        words = split_by_words(morph, cleaned_text.text)

        logger.debug(words)


asyncio.run(main())
