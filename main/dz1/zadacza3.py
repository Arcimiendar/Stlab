class FibIterator:
    def __iter__(self):
        self._previous = 0
        self._current = 1
        self._calls = 0
        return self

    def __next__(self):
        if self._calls >= 100:
            raise StopIteration

        self._calls += 1

        if self._calls == 1:
            return 0

        self._current, self._previous = self._current + self._previous, self._current

        return self._previous


def fib_generator():
    previous = 0
    current = 1
    iteration = 0
    while iteration != 100:
        iteration += 1
        if iteration == 1:
            yield 0
        else:
            yield current
            current, previous = previous + current, current


def strange_decorator(func):
    def new_func(*args, **kwargs):
        if len(args) + len(kwargs) > 10:
            raise ValueError

        for argument in kwargs.items():
            if isinstance(argument, bool):
                raise TypeError

        value = func(args, kwargs)

        return value + 13 if isinstance(value, int) and not isinstance(value, bool) else value

    return new_func
