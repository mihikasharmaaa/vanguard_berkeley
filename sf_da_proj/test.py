from calendar import month
from gc import collect
from urls import month_urls
import requests
from bs4 import BeautifulSoup
from newspaper import Config
from newspaper import Article

all_urls = []
def collect_urls(month_urls):
    for url in month_urls: #for each news page in list
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        urls_on_page = [] #initializes list of all urls on that page
        x = soup.find_all('a')
        urls_on_page = [str(link.get('href')) for link in x if 'article' in str(link.get('href'))]
        for u in range(len(urls_on_page)):
            old_u = urls_on_page[u]
            if old_u[0:4] == '/web':
                new_u = 'https://web.archive.org' + old_u
                urls_on_page[u] = new_u
        all_urls.append(urls_on_page) #add list to list of all urls total for the month
collect_urls(month_urls)

def analyze_day(day_urls):
    crime = False
    Sf = False
    Oak = False
    Da = False
    San_DA = 0
    Oak_DA = 0
    for u in day_urls:
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36'
        config = Config()
        config.browser_user_agent = user_agent
        config.request_timeout = 15
        article = Article(u, config=config)
        article.download()
        article.parse()
        full_article = article.text
        full_article = str(full_article).lower().replace('san francisco chronicle', '')
        if(full_article.find('crime') != -1 or full_article.find('police') != -1):
            crime = True
        if(full_article.find('san francisco') != -1):
            Sf = True
        if(full_article.find('oakland') != -1):
            Oak = True
        if(full_article.find('district attorney') != -1 or full_article.find('d.a.') != -1):
            Da = True
        if(Sf and crime and Da):
            San_DA += 1
        if(Oak and crime and Da):
            Oak_DA +=1
    return San_DA, Oak_DA

print(analyze_day(month_urls[0]))
##results = map(analyze_day, all_urls)
##print(list(results))
