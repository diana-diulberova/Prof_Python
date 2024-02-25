import requests
import bs4
import re
from fake_headers import Headers
import json
from tqdm import tqdm

headers = Headers(browser="chrome", os="win")

header_data = headers.generate()
vacancies = []

# ограничила количество просмотренных страниц, чтобы сократить время выполнения программы
for page in tqdm(range(0, 2), desc='Поиск по страницам ...'):
    response = requests.get(
        f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={page}', headers=header_data)
    html_data = response.text
    soup = bs4.BeautifulSoup(html_data, 'lxml')
    tag = soup.find_all('div', class_='serp-item')

    for mask in tag:
        # сохраняем ссылку на вакансию
        lay = mask.find('a')
        link = lay['href']

        # смотрим зп
        salary = mask.find('span', class_="bloko-header-section-3")
        if salary is not None:
            gat = salary.text
            salary = re.sub(gat)
        else:
            salary = 'None'

        # смотрим вакансию
        job = mask.find(class_="bloko-header-section-3").text

        # смотрим название компании
        title = mask.find('div', class_='vacancy-serp-item__meta-info-company').text
        company = re.sub(r'\s+', ' ', title).strip()

        # смотрим город
        ci = mask.find('div', class_="vacancy-serp-item-company").text
        heh = re.findall(r'(?:Москва|Санкт-Петербург)', ci)
        city = heh[0]

        # словарь для хранения данных
        vacancy = {
            'link': link,
            'salary': salary,
            'company': company,
            'city': city,
            'job': job
        }

        # ищем "Django" и "Flask"
        response1 = requests.get(link, headers=header_data)
        html_data1 = response1.text
        soup1 = bs4.BeautifulSoup(html_data1, 'lxml')
        tag1 = soup1.find('div', class_='g-user-content')

        if tag1 is not None:
            if tag:
                text = tag1.text
                match = re.search(r'\b(Django|Flask)\b', text)
                if match:
                    match_word = match.group(0)
                    vacancies.append(vacancy)
                else:
                    continue
        else:
            continue

        # сохраняем полученные вакансии в файл
        file_with_vacancies = 'vacancies.json'

        with open(file_with_vacancies, 'w', encoding='utf-8') as file:
            json.dump(vacancies, file, indent=4, ensure_ascii=False)
