import typing
import dataclasses


@dataclasses.dataclass(order=True)
class Student:
    name: str = dataclasses.field(compare=False)
    average_mark: float
    age: int = dataclasses.field(default=18, compare=False, repr=False)
    subjects: typing.List[str] = dataclasses.field(default_factory=list, compare=False, repr=False)

    def __post_init__(self):
        self.first_letter = self.name[0] if len(self.name) > 0 else None
