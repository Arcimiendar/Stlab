import asyncio
import datetime
import re
import os
from typing import List, NoReturn
import aiohttp

import sys
from lxml import html
from requests import get


def download_image(url: str, file_path: str) -> NoReturn:
    with open(file_path, 'wb') as image_file:
        image_file.write(get(url).content)


async def download_image_asynchronously(url: str, file_path: str) -> NoReturn:
    with open(file_path, 'wb') as image_file:
        async with aiohttp.ClientSession() as session:
            data = await session.get(url)
            image_file.write(await data.content.read())


def get_flag_list() -> List[str]:
    image_tags = html.fromstring(get('https://www.countryflags.io').text).\
        xpath('//img[@class="theme-flat"]')

    return list(map(lambda image_tag: 'https://www.countryflags.io' + image_tag.attrib['src'], image_tags))


def download_flags_in_single_thread():
    urls = get_flag_list()
    path = os.path.dirname(sys.argv[0]) + '/flags'
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    pattern = r'(?<=io/)[A-Z]{2}(?=/flat)'

    for url in urls:
        download_image(url, 'flags/' + re.search(pattern, url).group(0) + '.png')


def download_flags_asynchronously():
    urls = get_flag_list()
    path = os.path.dirname(sys.argv[0]) + '/flags'
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    pattern = r'(?<=io/)[A-Z]{2}(?=/flat)'

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(
        [
            download_image_asynchronously(
                url, 'flags/' + re.search(pattern, url).group(0) + '.png'
            ) for url in urls
        ]
    ))


def compare():
    print('not async starts')
    start = datetime.datetime.now()
    download_flags_in_single_thread()
    print(f'not async took {datetime.datetime.now() - start}')

    print('async starts')
    start = datetime.datetime.now()
    download_flags_asynchronously()
    print(f'async took {datetime.datetime.now() - start}')


if __name__ == '__main__':
    compare()
