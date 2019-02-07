import typing
import re


Union = typing.Union
Dict = typing.Dict
List = typing.List


class RegParser:
    ADDRESS_REGEX = r'^(?:[A-Z][a-z]*, )?(?:[A-Z][a-z]*(?: [Cc]ity)?, )?' \
                   r'[\w -]+(?: str\.)?, [0-9]+[ ]*[\\|/,-]?[ ]*[0-9]+$'
    CONTACT_REGEX = r'^(?:(?:name=(?P<name>[\w -]*)|surname=(?P<surname>[\w -]*)|age=(?P<age>[\w -]*)|' \
                    r'city=(?P<city>[\w -]*))(?:;|$)){1,4}(?<!;)$'
    PRICE_REGEX = r'[0-9]+(?:[\.,]?[0-9]+)?(?=[ ]*BYN)|(?<=[\$€] )[0-9]+(?:[\.,][0-9]+)?'

    @classmethod
    def find(cls, string: str, pattern_num: int) \
            -> List[Union[str, Dict[str, str], Union[int, float]]]:

        result = list()

        if pattern_num == 1:
            return re.findall(cls.ADDRESS_REGEX, string, re.MULTILINE)

        elif pattern_num == 2:
            splitted_string = string.split(sep='\n')
            for line in splitted_string:
                matched_data = re.match(cls.CONTACT_REGEX, line)
                if matched_data is not None:
                    result.insert(0, dict())
                    for key in ['age', 'name', 'surname', 'city']:
                        data = matched_data.group(key)
                        if data is not None:
                            result[0][key] = data
            result.reverse()
            return result

        elif pattern_num == 3:
            string_prices = re.findall(cls.PRICE_REGEX, string)
            for string_price in string_prices:
                if '.' in string_price or ',' in string_price:
                    string_price = string_price.replace(',', '.')
                    result.append(float(string_price))
                else:
                    result.append(int(string_price))

            return result

        else:
            raise ValueError
