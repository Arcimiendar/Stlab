import typing
import functools


def analyze_students(d: typing.Dict[str, typing.Dict[str, typing.List[int]]]) -> typing.Set[typing.Tuple]:
    return {(s, u, functools.reduce(lambda a, x: a*x, d[s][u])) for s in d for u in d[s] if u != '1C'}  # it fits!


def validate_data(data: typing.Dict) -> bool:
    for student in data:
        if not isinstance(student, str):
            raise TypeError

        for subject in data[student]:
            if not isinstance(subject, str):
                raise TypeError

            for note in data[student][subject]:
                if not (isinstance(note, int) and not isinstance(note, bool)):
                    raise TypeError

    for student in data:
        for letter in student:
            if not (ord('0') <= ord(letter) <= ord('9') or
                    ord('a') <= ord(letter.lower()) <= ord('z')):
                raise ValueError

        for subject in data[student]:
            for letter in subject:
                if not (ord('0') <= ord(letter) <= ord('9') or
                        ord('a') <= ord(letter.lower()) <= ord('z')):
                    raise ValueError

            for note in data[student][subject]:
                if note < 1 or note > 10:
                    raise ValueError

    return True
