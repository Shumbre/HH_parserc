import csv
from bs4 import BeautifulSoup as bs
import requests


headers1 = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
base_url = 'https://hh.ru/search/vacancy?area=1&search_period=3&text=python&page=0'

def hh_parse(base_url, headers):
    jobs = []
    urls = [base_url]
    session = requests.Session()
    request = session.get(base_url, headers=headers1)

    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count_pages = int(pagination[-1].text)
            for i in range(count_pages):
                url = f'https://hh.ru/search/vacancy?area=1&search_period=3&text=python&page={i}'
                if url not in urls:
                    urls.append(url)
        except:
            pass

    for url in urls:
        request = session.get(url, headers=headers1)
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
        for div in divs:
            try:
                title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                description1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                description2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                description = description1 + description2
                jobs.append({
                    'title': title,
                    'href': href,
                    'company': company,
                    'description': description,
                })
            except:
                pass
    return jobs



if __name__ == '__main__':
    jobs = hh_parse(base_url, headers1)

