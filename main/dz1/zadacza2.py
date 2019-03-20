import typing
import functools


def analyze_students(data: typing.Dict[str, typing.Dict[str, typing.List[int]]]) -> typing.Set[typing.Tuple]:
    return {(student, subject, functools.reduce(lambda accumulator, note: accumulator * note, data[student][subject])) for student in data for subject in data[student] if subject != '1C'}  # it doesn't fit yet!


def validate_data(data: typing.Dict) -> bool:

    raise_value_error = False

    for student, subjects in data.items():
        if not isinstance(student, str):
            raise TypeError

        for letter in student:
            if not (ord('0') <= ord(letter) <= ord('9') or
                    ord('a') <= ord(letter.lower()) <= ord('z')):
                raise_value_error = True

        for subject, notes in subjects.items():
            if not isinstance(subject, str):
                raise TypeError

            for letter in subject:
                if not (ord('0') <= ord(letter) <= ord('9') or
                        ord('a') <= ord(letter.lower()) <= ord('z')):
                    raise_value_error = True

            for note in notes:
                if not (isinstance(note, int) and not isinstance(note, bool)):
                    raise TypeError

                if note < 1 or note > 10:
                    raise_value_error = True

    if raise_value_error:
        raise ValueError

    return True
