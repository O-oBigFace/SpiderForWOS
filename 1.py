import openpyxl
import os
import json

column = {
    "expert": "A",
    "affiliation": "B",
    "interests": "C",
    "email": "D",
    "phone": "E",
    "address": "F",
    "country": "G",
    "language": "H",
    "position": "I",
    "name": "J",
    "citedby": "K",
    "hindex": "L",
    "hindex5y": "M",
    "i10index": "N",
    "i10index5y": "O",
    "url_picture": "P",
}
path_worksheet = os.path.join(os.getcwd(), 'result.xlsx')

wb = openpyxl.load_workbook(path_worksheet)
st = wb.active

with open('result1', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        item = json.loads(line.strip())
        st[column["name"] + item[0]] = item[1]
        st[column["citedby"] + item[0]] = item[2]
        st[column["hindex"] + item[0]] = item[3]
        st[column["hindex5y"] + item[0]] = item[4]
        st[column["i10index"] + item[0]] = item[5]
        st[column["i10index5y"] + item[0]] = item[6]
        st[column["url_picture"] + item[0]] = item[7]
        st[column["affiliation"] + item[0]] = item[8]

wb.save(path_worksheet)