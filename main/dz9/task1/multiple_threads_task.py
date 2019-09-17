from threading import Thread, Lock, BoundedSemaphore, Event, Barrier, Condition, BrokenBarrierError
from typing import NoReturn
import time


class ClientThread(Thread):
    __CLIENT_LOCK = Lock()
    __id = 0

    def __init__(self):
        super().__init__()
        self._current_id = ClientThread.__id
        ClientThread.__id += 1
        self.start()

    def run(self) -> NoReturn:
        while True:
            self.client()
            time.sleep(0.01)

    def client(self):
        self.__CLIENT_LOCK.acquire()

        for char in f'client id is {self._current_id}':
            print(char, end="", flush=True)
            time.sleep(0.1)
        print('', flush=True)

        self.__CLIENT_LOCK.release()


def client_task():
    for i in range(3):
        ClientThread()


class TouristBorderGuard(Thread):
    _current_id = 0
    __CONDITION = Condition()

    def __init__(self, is_guard=None):
        super().__init__()
        self.__current_id = TouristBorderGuard._current_id
        TouristBorderGuard._current_id += 1
        self.__is_guard = is_guard if is_guard is not None else False
        self.start()

    def run(self) -> NoReturn:
        if self.__is_guard:
            for i in range(3):
                with self.__CONDITION:
                    self.__CONDITION.notify()
                time.sleep(1)
            with self.__CONDITION:
                self.__CONDITION.notify_all()
        else:
            self.__CONDITION.acquire()
            self.__CONDITION.wait()
            print(f'my id is {self.__current_id}')
            self.__CONDITION.release()


def tourist_guarder_task():
    for i in range(6):
        TouristBorderGuard()
    time.sleep(3)

    TouristBorderGuard(is_guard=True)


class Client2Thread(Thread):
    __BOUND_SEMAPHORE = BoundedSemaphore(3)
    __id = 0

    def __init__(self):
        super().__init__()
        self._current_id = Client2Thread.__id
        Client2Thread.__id += 1
        self.start()

    def run(self) -> NoReturn:
        self.__BOUND_SEMAPHORE.acquire()
        time.sleep(self._current_id / 2)
        for char in f'my id is {self._current_id}':
            print(char, end="", flush=True)
        print("", flush=True)

        self.__BOUND_SEMAPHORE.release()
        print(f"semaphore after value {self.__BOUND_SEMAPHORE._value}", flush=True)


def client_2_task():
    for i in range(9):
        Client2Thread()


class TouristBorderGuard2(Thread):
    __OPENING_EVENT = Event()
    __id = 0
    __PRINT_LOCK = Lock()

    def __init__(self, is_guard=None):
        super().__init__()
        self.__is_guard = is_guard if is_guard is not None else False
        self._current_id = TouristBorderGuard2.__id
        TouristBorderGuard2.__id += 1
        self.start()

    def run(self) -> NoReturn:
        if self.__is_guard:
            time.sleep(4)
            with self.__PRINT_LOCK:
                print("border opened")
            self.__OPENING_EVENT.set()
            time.sleep(2)
            with self.__PRINT_LOCK:
                print("border closed")
            self.__OPENING_EVENT.clear()
            time.sleep(4)
            with self.__PRINT_LOCK:
                print("border is opened again")
            self.__OPENING_EVENT.set()
        else:
            self.__OPENING_EVENT.wait()
            with self.__PRINT_LOCK:
                print(f'my id is {self._current_id}')


def tourist_guard_2_task():
    TouristBorderGuard2(is_guard=True)
    for i in range(9):
        TouristBorderGuard2()
        time.sleep(1)


class RollerCoaster(Thread):
    __PRINT_LOCK = Lock()
    __BARRIER = Barrier(5, timeout=4)
    __id = 0

    def __init__(self):
        super().__init__()
        self._current_id = RollerCoaster.__id
        RollerCoaster.__id += 1
        with self.__PRINT_LOCK:
            print(f'roller coaster {self._current_id} starts')
        self.start()

    def run(self) -> NoReturn:
        try:
            self.__BARRIER.wait()
        except BrokenBarrierError:
            self.__BARRIER.reset()
        with self.__PRINT_LOCK:
            print(f'my id is {self._current_id}')


def roller_coaster_task():
    for i in range(20):
        RollerCoaster()
        time.sleep(0.5)

    for i in range(10):
        RollerCoaster()
        time.sleep(1)

    for i in range(5):
        RollerCoaster()
        time.sleep(2)


if __name__ == '__main__':
    choice = input("""
    \r1) client
    \r2) tourist - border guard
    \r3) client 2
    \r4) tourist - border guard 2
    \r5) roller coaster
    \r""")

    if choice == '1':
        client_task()
    elif choice == '2':
        tourist_guarder_task()
    elif choice == '3':
        client_2_task()
    elif choice == '4':
        tourist_guard_2_task()
    elif choice == '5':
        roller_coaster_task()
