import fractions
import decimal
import typing
import collections


def get_max_and_min(data: typing.Set[typing.Union[
    decimal.Decimal, fractions.Fraction, str
]])\
        -> typing.Tuple[
                typing.Union[fractions.Fraction, decimal.Decimal],
                typing.Union[fractions.Fraction, decimal.Decimal]]:
    list_to_search = []
    for i in data:
        if isinstance(i, str):
            if i.find('\\') != -1:
                list_to_search.append(
                    fractions.Fraction(i.replace('\\', '/'))
                )
            else:
                list_to_search.append(decimal.Decimal(i))
        else:
            list_to_search.append(i)

    maximal = max(list_to_search)
    minimal = min(list_to_search)

    to_return = collections.namedtuple('tuple', ['max_value', 'min_value'])(
        maximal, minimal
    )

    return to_return


print(get_max_and_min(
    {'10\\2'}
))
