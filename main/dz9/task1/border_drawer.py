import datetime
import os
from typing import NoReturn, List
import math
from multiprocessing import Process, Queue

from PIL import Image, ImageDraw


def draw_border_for_single_image(image_path: str, image_destiny: str) -> NoReturn:
    image: Image.Image = Image.open(image_path)

    drawer = ImageDraw.Draw(image)

    drawer.line((0, 0, 0, image.size[1] - 1), fill='black')
    drawer.line((0, image.size[1] - 1, image.size[0] - 1, image.size[1] - 1), fill='black')
    drawer.line((image.size[0] - 1, image.size[1] - 1, image.size[0] - 1, 0), fill='black')
    drawer.line((image.size[0] - 1, 0, 0, 0), fill='black')

    del drawer

    with open(image_destiny, 'wb') as destiny_file:
        image.save(destiny_file, "PNG")


def get_file_paths(directory: str) -> List[str]:
    return [file for file in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, file))]


def draw_border_for_array_files(folder_source: str, folder_destiny: str,
                                file_names: List[str], queue: Queue=None) -> NoReturn:
    try:
        os.mkdir(folder_destiny)
    except FileExistsError:
        pass
    for file_name in file_names:
        draw_border_for_single_image(
            os.path.join(folder_source, file_name),
            os.path.join(folder_destiny, file_name)
        )
        if queue is not None:
            queue.put((
                f'file name is {file_name}',
                f'old size = {os.path.getsize(os.path.join(folder_source, file_name))}',
                f'new size = {os.path.getsize(os.path.join(folder_destiny, file_name))}'
            ))


def draw_border_in_one_process(folder_source: str, folder_destiny: str) -> NoReturn:
    file_names = get_file_paths(folder_source)
    draw_border_for_array_files(folder_source, folder_destiny, file_names)


def draw_border_in_multiple_processes(folder_source: str, folder_destiny: str) -> NoReturn:
    file_names = get_file_paths(folder_source)

    files_per_process = math.ceil(len(file_names) / os.cpu_count())

    queue = Queue()

    processes: List[Process] = []

    for i in range(os.cpu_count()):
        processes.append(
            Process(
                target=draw_border_for_array_files,
                args=(
                    folder_source, folder_destiny,
                    file_names[i*files_per_process:i*(files_per_process + 1)],
                    queue
                )
            )
        )

    for process in processes:
        process.start()

    info = []
    for process in processes:
        process.join()
        info.append(queue.get())
    print(info)


def compare():
    source = 'flags/'
    destiny = 'flags_plus/'

    print('single process starts')
    start = datetime.datetime.now()
    draw_border_in_one_process(source, destiny)
    print(f'single process took {datetime.datetime.now() - start}')

    print('multiple processes start')
    start = datetime.datetime.now()
    draw_border_in_multiple_processes(source, destiny)
    print(f'multiple processes took {datetime.datetime.now() - start}')


if __name__ == '__main__':
    compare()


