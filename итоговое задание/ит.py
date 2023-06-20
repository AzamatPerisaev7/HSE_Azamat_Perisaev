import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


class ParserCBRF:

    def __init__(self, url):
        self.url = url

    def start(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'data'})
        rows = table.find_all('tr')[1:]

        data = {}
        for row in rows:
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            iso_date = datetime.strptime(cols[0], '%d.%m.%Y').date().isoformat()
            cols[0] = iso_date
            data[iso_date] = cols[1]

        with open('data_1.json', 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=2, ensure_ascii=False)

        print("Data written to data_1.json file.")


parser = ParserCBRF("http://cbr.ru/hd_base/mb_nd/mb_nd_weekly/")
parser.start()


class MonetaryData:

    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r', encoding='utf-8') as infile:
            self.data = json.load(infile)

    def monetary_base_by_date(self, date):
        return self.data.get(date, "Data not found for selected date")

    def monetary_base_last(self):
        last_date = max(self.data.keys())
        return self.data[last_date]

    def range_dates(self, from_date, to_date):
        filtered_data = {}
        for key, value in self.data.items():
            date_obj = datetime.strptime(key, '%Y-%m-%d').date()
            if from_date <= date_obj <= to_date:
                filtered_data[key] = value
        sorted_data = sorted(filtered_data.items())
        return sorted_data


monetary_data = MonetaryData('data_1.json')
print("Данные за определенную дату: " + monetary_data.monetary_base_by_date('2022-08-19'))  # введите дату для проверки

monetary_data = MonetaryData('data_1.json')
print("Данные за последнюю доступную дату: " + monetary_data.monetary_base_last())

monetary_data = MonetaryData('data_1.json')
range_data = monetary_data.range_dates(datetime(2022, 8, 5).date(),
                                       datetime(2023, 3, 22).date())  # выберите диапазон дат
print("Данные за определенный период:")
for data in range_data:
    print(data)