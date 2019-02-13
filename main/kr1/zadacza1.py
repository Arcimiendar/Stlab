import collections
import types
import typing


namedtuple = collections.namedtuple


def log_decorator(func: typing.Callable, name_func: str):
    def new_func(self, *args, **kwargs):
        
        result = func(self, *args, **kwargs)

        self.log.append(self.LogItem(name=name_func, args=list(args),
                                     kwargs=kwargs, result=result))

        return result

    return new_func


@property
def last_log(self):

    self.log.reverse()

    log = list()

    iteration = 0

    for event in self.log:
        if iteration == 3:
            break
        log.append(event)
        iteration += 1

    self.log.reverse()

    return log


class Logger(type):

    @staticmethod
    def get_new_attr(dct: typing.Dict[str, typing.Any]):
        new_dct = dict()
        new_dct["LogItem"] = namedtuple('LogItem', ['name', 'args', 'kwargs', 'result'],
                                        defaults=[str(), list(), dict()])
        new_dct["log"] = list()
        new_dct['last_log'] = last_log

        for name_of_attribute in dct:
            if name_of_attribute[0] != '_' and isinstance(dct[name_of_attribute], types.FunctionType):
                new_dct[name_of_attribute] = log_decorator(dct[name_of_attribute], name_of_attribute)
            else:
                new_dct[name_of_attribute] = dct[name_of_attribute]

        return new_dct

    def __new__(mcs, name, bases, dct):
        return super().__new__(mcs, name, bases, mcs.get_new_attr(dct))
