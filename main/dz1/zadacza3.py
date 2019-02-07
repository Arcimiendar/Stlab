class FibIterator:
    def __iter__(self):
        self._prev = 0
        self._curr = 1
        self._calls = 0
        return self

    def __next__(self):
        if self._calls >= 100:
            raise StopIteration

        self._calls += 1

        if self._calls == 1:
            return 0

        to_return = self._curr
        self._curr += self._prev
        self._prev = to_return

        return to_return


def fib_generator():
    prev = 1
    prevprev = 0
    curr = 1
    iteration = 0
    while iteration != 100:
        iteration += 1
        if iteration == 1:
            yield 0
        else:
            yield curr
            curr = prev + prevprev
            prevprev = prev
            prev = curr


def strange_decorator(func):
    def new_func(*args, **kwargs):
        if len(args) + len(kwargs) > 10:
            raise ValueError

        for key in kwargs:
            if isinstance(kwargs[key], bool):
                raise TypeError

        to_return = func(args, kwargs)

        return to_return + 13 if isinstance(to_return, int) and not isinstance(to_return, bool) else to_return

    return new_func
