import re
import csv

with open("phonebook_raw.csv", encoding="utf8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

number_pattern = re.compile(
    r'(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})')
extension_pattern = re.compile(r'\s*\(*(доб.)\s*(\d+)\)*\s*')
text_pattern = re.compile(
    r'(\w+[А-яЁё])\s*\,*(\w+[А-яЁё])\s*\,*(\w+[А-яЁё])*\,*(\w+[А-яЁё])*\,*(\w+[А-яЁё]\w+[А-яЁё –]*'
    r'\–*\s*)*\,*(\+*\d\s*\(*\d+\)*\-*\s*\d+\-*\d+\-*\d+\s*\(*\w*\.*\s*\d*\)*)*\,*([a-zA-Z0-9_.+-]'
    r'+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)*')

temp_list = []
for c in range(len(contacts_list)):
    if c == 0:
        temp_list.append(contacts_list[c])
    else:
        line = ','.join(contacts_list[c])
        result = re.search(text_pattern, line)
        temp_list.append(list(result.groups()))
        if temp_list[c][5] is not None:
            temp_list[c][5] = number_pattern.sub(r'+7(\2)\3-\4-\5', temp_list[c][5])
            temp_list[c][5] = extension_pattern.sub(r' \1\2', temp_list[c][5])


result_list = []
for i in range(len(temp_list)):
    for s in range(len(temp_list)):
        if temp_list[i][0] == temp_list[s][0]:
            temp_list[i] = [x or y for x, y in zip(temp_list[i], temp_list[s])]
    if temp_list[i] not in result_list:
        result_list.append(temp_list[i])


with open("phonebook_result.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result_list)
