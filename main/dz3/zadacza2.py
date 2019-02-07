import csv
import json
import openpyxl
import typing


File = typing.TextIO


def merge_students_data(csv_file: File, xlsx_workbook, json_file: File) \
        -> typing.NoReturn:
    wb = xlsx_workbook
    students_csv = csv.DictReader(csv_file)
    sheet = wb[wb.sheetnames[0]]

    res_dict = dict()

    for name_row in range(len(sheet['A'])):
        res_dict[sheet[f'A{name_row + 1}'].value] = \
            {'marks': [mark.value for mark in sheet[str(name_row + 1)] if
                       isinstance(mark.value, int) and not isinstance(mark.value, bool)]}  # if value is int

    for student in students_csv:
        name = student['first_name'] + ' ' + student['last_name']

        res_dict[name]['age'] = int(student['age'])

    json.dump(res_dict, json_file)
