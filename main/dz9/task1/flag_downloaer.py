import datetime
import re
import os
import threading
from typing import List, NoReturn

import sys
from lxml import html
from requests import get


def download_image(url: str, file_path: str) -> NoReturn:
    with open(file_path, 'wb') as image_file:
        image_file.write(get(url).content)


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


def download_flags_in_multiple_threads():
    urls = get_flag_list()
    path = os.path.dirname(sys.argv[0]) + '/flags'
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

    pattern = r'(?<=io/)[A-Z]{2}(?=/flat)'

    threads = []

    for url in urls:
        threads.append(threading.Thread(
            target=download_image,
            args=(url, 'flags/' + re.search(pattern, url).group(0) + '.png')
        ))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def compare():
    print('single thread starts')
    start = datetime.datetime.now()
    download_flags_in_single_thread()
    print(f'single thread took {datetime.datetime.now() - start}')

    print('multiple threads start')
    start = datetime.datetime.now()
    download_flags_in_multiple_threads()
    print(f'multiple threads took {datetime.datetime.now() - start}')


if __name__ == '__main__':
    compare()
