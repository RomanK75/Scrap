import requests
import bs4
from fake_headers import Headers
import time
import requests_html


url = r"https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

keywords = ["Django", "django", "Flask", "flask"]

### mian function / Moscow/St. Petersburg, Python, Django/Flask

headers = Headers(browser="firefox", os="win")
headers_data = headers.generate()

main_page_html = requests.get(url, headers=headers_data).text
main_page_soup = bs4.BeautifulSoup(main_page_html, "lxml")
tags = main_page_soup.find_all(
    "div", {"class": "vacancy-serp-item__layout"}
)  ### Main problem, parser finds only 20 div instead of 50

vacancy = []

for tag in tags:
    vacancy_name = tag.find("a", {"class": "serp-item__title"}).text
    for keyword in keywords:  ## Checking keyword in vacancy
        if keyword in vacancy_name:
            link = tag.find("a", {"class": "serp-item__title"})["href"]
            city = tag.find("div", {"data-qa": "vacancy-serp__vacancy-address"})
            company_name = tag.find("a", {"data-qa": "vacancy-serp__vacancy-employer"})
            vacancy_paycheck = tag.find(
                "span", {"data-qa": "vacancy-serp__vacancy-compensation"}
            )
            if city:  # if city not None
                city = city.text.replace("\xa0", " ")
            else:
                city = "None"
            if company_name:
                company_name = company_name.text
            else:
                company_name = "None"
            if vacancy_paycheck:  # if payment not None
                vacancy_paycheck = vacancy_paycheck.text
                vacancy_paycheck = vacancy_paycheck.replace("\u202f", " ")
                ls = [
                    vacancy_name,
                    {
                        "payment": vacancy_paycheck,
                        "link": link,
                        "company name": company_name,
                        "city": city,
                    },
                ]
            else:
                ls = [
                    vacancy_name,
                    {
                        "payment": "None",
                        "link": link,
                        "company name": company_name,
                        "city": city,
                    },
                ]
            vacancy.append(ls)

print(len(vacancy), vacancy)


### conver to json func (link, paycheck array, company, city)


### Secondary task - add only USD jobs.
