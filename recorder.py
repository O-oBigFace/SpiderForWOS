import json
import os

path_record = os.path.join(os.getcwd(), 'record')
path_result = os.path.join(os.getcwd(), 'result')

record = {}
for i in range(2, 46012 + 1):
    record[str(i)] = False

with open(path_result, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        item = json.loads(line)
        record[item[0]] = True

with open(path_record, 'w', encoding='utf-8') as o:
    o.write(json.dumps(record))

