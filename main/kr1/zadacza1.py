import collections
import types
import typing


namedtuple = collections.namedtuple


def log_dec(func: typing.Callable, name_func: str):
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
        res_dct = dict()
        res_dct["LogItem"] = namedtuple('LogItem', ['name', 'args', 'kwargs', 'result'],
                                        defaults=[str(), list(), dict()])
        res_dct["log"] = list()
        res_dct['last_log'] = last_log

        for name_attr in dct:
            if name_attr[0] != '_' and isinstance(dct[name_attr], types.FunctionType):
                res_dct[name_attr] = log_dec(dct[name_attr], name_attr)
            else:
                res_dct[name_attr] = dct[name_attr]

        return res_dct

    def __new__(mcs, name, bases, dct):
        return super().__new__(mcs, name, bases, mcs.get_new_attr(dct))
