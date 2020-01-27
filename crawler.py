import requests
from bs4 import BeautifulSoup
import re

class IndiaMart():
    def __init__(self):
        self.agent = requests.session()
        self.home_url = 'https://www.indiamart.com/'
        self.search_url = 'https://dir.indiamart.com/search.mp?ss={}?page_no={}'

    def get_home(self,query, page_no):
        search_url = self.search_url.format('+'.join(query.split(' ')), page_no)
        print(search_url)
        resp = self.agent.get(search_url)
        if resp.status_code == 200:
            content = resp.content
            self.parser(content)

    def parser(self, content):
        soup = BeautifulSoup(content, 'lxml')
        ul = soup.find('ul',{'class':'wlm'})
        record = dict()
        for shop in ul.find_all('li',{'id':re.compile('LST\d+|lst\d+')}):
            desc_description = shop.find('div',{'class':'desc des_p'})
            for ii in desc_description.find_all('p'):
                ii = ii.text.strip()
                key = ii.split(':')[0].strip()
                value = ii.split(':')[1].strip()
                record[key] = value
            phone = shop.find('span',{'data-click':"MobileNo"}).text.replace('Call +91-','').strip()
            record['phone'] = phone
            raw = shop.find('div',{'class':"r-cl b-gry"})
            record['website'] = raw.a.get('href')
            company_name = raw.find('h4',{'data-click':'CompanyName'})
            record['company_name'] = company_name.text.strip()

            address = shop.find('p',{'data-rlocation':re.compile('([A-Za-z]+)')})
            record['address'] = address.text.strip()
            pprice = shop.find('span',{'class':"prc cur"})
            price = ''
            if pprice:
                price = pprice.text.strip()
            record['price'] = price.replace('Get Latest Price','').replace('Latest Price','').replace('\xa0',' ')

            raw_truested = shop.find('span',{'data-click':"TrustSEAL"})
            truested = ''
            if raw_truested:
                truested = raw_truested.text.strip()
            record['truested'] = truested
            print(record)
            print('')

    def pages(self):
        mininum = 0
        maximum = 100
        query = 'caustic soda'
        for page_no in range(mininum, maximum):
            self.get_home(query,page_no)

obj = IndiaMart()
obj.pages()
