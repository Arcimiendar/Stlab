import json
import typing
import openpyxl


File = typing.TextIO


def xlsx_workbook(xlsx_workbook, json_file: File):

    wb = xlsx_workbook
    sheet = wb[wb.sheetnames[0]]
    res = dict()

    key = sheet['A1'].value
    res[key] = dict()

    for row in sheet.rows:
        if row[0].value is not None:
            key = row[0].value
            res[key] = dict()
        res[key][row[1].value] = row[2].value

    json.dump(res, json_file)
