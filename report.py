from pymongo import MongoClient
from pandas.io.json import json_normalize

mongo = MongoClient('127.0.0.1',27017)
db = mongo['india_mart']
con = db['caustic_soda']
def create():
    report_arr = []
    id_no = 1
    for data in con.find({}):
        phone = data.get('phone','')
        company_name = data.get('company_name','')
        price = data.get('price','')
        truested = data.get('truested','').replace('TrustSEAL','').strip()
        address = data.get('address','')
        products = data.get('products','')
        website = data.get('website','')
        packing_size = data.get('Packing Size','')
        product_type = data.get('Type','')
        application = data.get('Application','')

        record = dict()
        record['id'] = id_no
        record['company'] = company_name
        record['phone'] = phone
        record['packing'] = packing_size
        record['type'] = product_type
        record['price'] = price
        record['products'] = products
        record['application'] = application
        record['trusted'] = truested
        report_arr.append(record)
        id_no += 1

    dts = json_normalize(report_arr)
    dts.to_excel('report.xlsx')

create()
