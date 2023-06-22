import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
import json


def get_headers():
    headers = Headers(browser="firefox", os='win')
    return headers.generate()


def hhparsingrubbles():
    HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    responsevacancies = requests.get(HOST, headers=get_headers()).text
    soup = BeautifulSoup(responsevacancies, features='lxml')
    vacancieslist = soup.find("main", {"class": "vacancy-serp-content"})
    vacancies = vacancieslist.find_all('div', {'class': 'serp-item'})
    parsed = []
    for vacancy in vacancies:

        title = vacancy.find('a', class_='serp-item__title')
        link = title['href']
        vacancy_name = title.text

        response = requests.get(link, headers=get_headers())
        vacancy_article = BeautifulSoup(response.text, features='lxml')
        vacancy_description = vacancy_article.find('div', {'data-qa': 'vacancy-description'}).text
        if ('django' in vacancy_description.lower()) or ('flask' in vacancy_description.lower()):
            fork = vacancy.find('span', class_='bloko-header-section-3')
            if fork is not None:
                fork = fork.text.strip()
                fork = fork.replace("\u202f", " ")
            else:
                fork = 'з/п не указана'
            company = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text
            city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
            #  attrs={'data-qa': 'vacancy-serp__vacancy-address'}
            item = {
                'Название должности': vacancy_name,
                'Ссылка': link,
                'Вилка зп': fork,
                'Компания': company,
                'Город': city
            }
            parsed.append(item)
    return parsed


if __name__ == '__main__':
    parsedrub = hhparsingrubbles()
    with open('vacancies.json', 'w', encoding='UTF-8') as file:
        json.dump(parsedrub, file, indent=5, ensure_ascii=False)
