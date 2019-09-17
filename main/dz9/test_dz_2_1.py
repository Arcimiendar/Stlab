import unittest
from random import randint

from ..dz2.zadacza1 import Department


class DZ2Test(unittest.TestCase):

    def test_budget_plan(self):
        budget = randint(1000, 100000)
        employers = {str(i): randint(0, 10) for i in range(10)}
        dep = Department('str', employers, budget)
        self.assertEqual(budget - sum(employers.values()), dep.get_budget_plan())
        employers = {str(i): randint(10000, 100001) for i in range(10)}
        dep = Department('str', employers, budget)
        self.assertRaises(ValueError, dep.get_budget_plan)

    def test_average_salary(self):
        employers = {str(i): randint(0, 10) for i in range(10)}
        dep = Department('1', employers, 1000)
        self.assertEqual(sum(employers.values()) / len(employers), dep.average_salary)

    def test_merge(self):
        departments = (
            Department('a', {'1': 100}, 200),
            Department('c', {'2': 150}, 200),
            Department('b', {'2': 150}, 200),
        )
        merged = Department.merge_departments(*departments)
        self.assertEqual(merged.name, 'b - c - a')

        departments[0].employees['1'] = 2000
        self.assertRaises(Department.BudgetError, Department.merge_departments, *departments)

    def test_sum(self):
        departments = (
            Department('a', {'1': 100}, 200),
            Department('c', {'2': 150}, 200),
        )
        merged = departments[0] + departments[1]
        self.assertEqual(merged.name, 'c - a')

        departments[0].employees['1'] = 2000
        self.assertRaises(Department.BudgetError, departments[0].__add__, departments[1])

    def test_str_repr(self):
        name = randint(0, 10)
        budget = randint(1000, 100000)
        employers = {str(i): randint(0, 10) for i in range(10)}
        dep = Department(str(name), employers, budget)
        self.assertEqual(
            f'{name} ({len(employers)} - {dep.average_salary}, {budget})',
            dep.__repr__()
        )

    def test_or(self):
        name = randint(0, 10)
        budget = randint(1000, 100000)
        employers = {str(i): randint(0, 10) for i in range(10)}
        dep = Department(str(name), employers, budget)
        dep2 = Department(str(name + 1), employers, budget)
        self.assertEqual((dep | dep2).name, dep.name)

        dep3 = Department(str(name + 2), employers, budget + 200)
        self.assertEqual((dep | dep3).name, dep3.name)

        dep4 = Department(str(name + 3), employers, 0)
        self.assertRaises(Department.BudgetError, dep.__or__, dep4)
