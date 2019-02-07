class Department:

    class BudgetError(ValueError):
        pass

    def __init__(self, name: str, employees: dict, budget: int):
        self.name = name
        self.budget = budget
        self.employees = employees
        self.budget = budget

    def get_budget_plan(self) -> int:
        to_return = self.budget
        for salary in self.employees.values():
            to_return -= salary

        if to_return < 0:
            raise self.BudgetError

        return to_return

    @property
    def average_salary(self):
        salary = sum(self.employees.values()) / len(self.employees)
        return round(salary, 2)

    @classmethod
    def merge_departments(cls, *args, **kwargs):

        departments = [*args]
        for item in kwargs.values():
            departments.append(item)

        departments.sort()

        for i in range(len(departments)):
            if not i:
                temp_dep = departments[0]
            else:
                temp_dep = cls.__adding(departments[i], temp_dep)

        temp_dep.get_budget_plan()
        return temp_dep

    def __gt__(self, other):
        self_greater = True
        if self.average_salary < other.average_salary:
            self_greater = False
        elif self.average_salary == other.average_salary:
            if self.name > other.name:
                self_greater = False

        return self_greater

    @staticmethod
    def __adding(this, other) -> 'Department':

        new_budget = this.budget + other.budget
        new_employees = {**this.employees, **other.employees}

        if this > other:
            new_name = this.name + ' - ' + other.name
        else:
            new_name = other.name + ' - ' + this.name

        return Department(new_name, new_employees, new_budget)

    def __add__(self, other: 'Department'):
        to_return = self.__adding(self, other)
        to_return.get_budget_plan()
        return to_return

    def __repr__(self):
        return f'{self.name} ({len(self.employees)} - {self.average_salary}, {self.budget})'

    def __or__(self, other: 'Department'):
        self_plan = self.get_budget_plan()
        other_plan = other.get_budget_plan()

        if self_plan < other_plan:
            return other
        else:
            return self
