from gc import collect
from urls import month_urls
import requests
from bs4 import BeautifulSoup

all_urls = []
def collect_urls(month_urls):
    for i in range(len(month_urls)): #for each news page in list
        url = month_urls[i] #gets the page url for that date
        page = requests.get(url)
        html = page.text #turns it into its html
        soup = BeautifulSoup(html, 'html.parser')
        urls_on_page = [] #initializes list of all urls on that page
        for link in soup.find_all('a'): #for each link on the page
            curr_url = link.get('href') #get the url
            str_url = str(curr_url)
            if 'article' in str_url: #filtering noise, if it is a link to an article
                if str_url[0:4] == '/web':
                    str_url = 'https://web.archive.org' + str_url
                urls_on_page.append(str_url) #add to list of all urls on the page
        all_urls.append(urls_on_page) #add list to list of all urls total for the month

collect_urls(month_urls)

def analyze_text(all_urls):
    crime = False
    Sf = False
    Oak = False
    Da = False
    San_DA = 0
    Oak_DA = 0
    for i in range(len(all_urls)):
        day_urls = all_urls[i] # operating on one day at a time
        for i in range(len(day_urls)): #operating on one url at a time
            url = day_urls[i]
            page = requests.get(url)
            html = page.text #turns it into its source code
            soup = BeautifulSoup(html, 'html.parser')
            for p in soup.find_all('p'): #each paragraph in article
                if('crime' in p):
                    crime = True
                if('San Francisco' in p):
                    Sf = True
                if('Oakland' in p):
                    Oak = True
                if('District Attorney' in p):
                    Da = True
            if(Sf and crime and Da):
                San_DA += 1
            if(Oak and crime and Da):
                Oak_DA +=1
    return San_DA, Oak_DA
                
print(analyze_text(all_urls))


