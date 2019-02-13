import csv
import json
import openpyxl
import typing


File = typing.TextIO


def merge_students_data(csv_file: File, xlsx_workbook, json_file: File) \
        -> typing.NoReturn:
    workbook = xlsx_workbook
    students_csv = csv.DictReader(csv_file)
    sheet = workbook[workbook.sheetnames[0]]

    further_json = dict()

    for number_of_row in range(len(sheet['A'])):
        further_json[sheet[f'A{number_of_row + 1}'].value] = \
            {'marks': [mark.value for mark in sheet[str(number_of_row + 1)] if
                       isinstance(mark.value, int) and not isinstance(mark.value, bool)]}  # if value is int

    for student in students_csv:
        name = student['first_name'] + ' ' + student['last_name']

        further_json[name]['age'] = int(student['age'])

    json.dump(further_json, json_file)
