import json
import typing
import openpyxl


File = typing.TextIO


def xlsx_to_json(xlsx_workbook, json_file: File):

    workbook = xlsx_workbook
    sheet = workbook[workbook.sheetnames[0]]
    further_json = dict()

    key = sheet['A1'].value
    further_json[key] = dict()

    for row in sheet.rows:
        if row[0].value is not None:
            key = row[0].value
            further_json[key] = dict()
        further_json[key][row[1].value] = row[2].value

    json.dump(further_json, json_file)
