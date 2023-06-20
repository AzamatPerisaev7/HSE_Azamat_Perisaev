import json
import csv

with open('traders.txt', 'r', encoding='utf-8') as f:
    inn_list = [line.strip() for line in f]
    # print(inn_list)

with open('traders.json', 'r', encoding='utf-8') as g:
    data = json.load(g)

org_info_list = []
for item in data:
    if item['inn'] in inn_list:
        org_info_list.append(item)
        # print(org_info_list)


with open('traders.csv', 'w', newline='') as h:
    writer = csv.writer(h)
    writer.writerow(['ИНН', 'ОГРН', 'АДРЕСС'])
    for item in org_info_list:
        writer.writerow([item['inn'], item['ogrn'], item['address']])
        print(writer)
