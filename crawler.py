import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient

class IndiaMart():
    def __init__(self):
        self.agent = requests.session()
        self.home_url = 'https://www.indiamart.com/'
        self.search_url = 'https://dir.indiamart.com/search.mp?ss={}?page_no={}'
        mongo = MongoClient('127.0.0.1',27017)
        db = mongo['india_mart']
        self.con = db['caustic_soda']

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
        for shop in ul.find_all('li',{'id':re.compile('LST\d+|lst\d+')}):
            record = dict()
            desc_description = shop.find('div',{'class':'desc des_p'})
            if desc_description:
                for ii in desc_description.find_all('p'):
                    ii = ii.text.strip()
                    key = ii.split(':')[0].replace('.','').strip()
                    value = ii.split(':')[1].strip()
                    record[key] = value

            phone = shop.find('span',{'data-click':"MobileNo"}).text.replace('Call +91-','').strip()
            record['phone'] = phone
            raw = shop.find('div',{'class':"r-cl b-gry"})
            record['website'] = raw.a.get('href')
            company_name = raw.find('h4',{'data-click':'CompanyName'})
            record['company_name'] = company_name.text.strip()

            raw_address = shop.find('p',{'data-rlocation':re.compile('([A-Za-z]+)')})
            address = ''
            if raw_address:
                address = raw_address.text.strip()

            record['address'] = address
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

            product_name_raw = soup.find('span',{'data-click':"Prod0Name"})
            product_name = ''
            if product_name_raw:
                product_name = product_name_raw.text.strip()
            record['products'] = product_name            
            if re.findall(r'caustic soda|Caustic Soda', product_name):
                self.con.insert_one(record)
                del record['_id']

    def pages(self):
        mininum = 0
        maximum = 100000
        query = 'caustic soda'
        for page_no in range(mininum, maximum):
            self.get_home(query,page_no)

obj = IndiaMart()
obj.pages()
