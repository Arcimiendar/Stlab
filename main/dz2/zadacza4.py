import types


def get_new_attr(old_attrs):
    new_class_attr = {}

    for name, old_attr in old_attrs.items():
        if isinstance(old_attr, types.FunctionType):
            if name.startswith('__'):
                new_class_attr[name] = old_attr
            else:
                new_class_attr[name.lower()] = old_attr
        elif isinstance(old_attr[name], type):
            splitted = name.split('_')
            new_name = ''
            for word in splitted:
                new_name += word.title()

            new_class_attr[new_name] = old_attr
        else:
            new_class_attr[name.upper()] = old_attr

    return new_class_attr


def pep8_warrior(class_name, class_parents, class_attr):
    return type(class_name, class_parents, get_new_attr(class_attr))


class Pep8Warrior(type):
    def __new__(mcs, name, bases, dct):
        return super().__new__(mcs, name, bases, get_new_attr(dct))
