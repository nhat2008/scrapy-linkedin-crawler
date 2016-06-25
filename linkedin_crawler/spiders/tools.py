__author__ = 'nhat'
from pymongo import MongoClient


class Mongodb():
    client = None
    rel_coll = None

    def __init__(self, host='localhost', port=27017, db=None, col=None):
        self._client = MongoClient(host, port)
        self._db = self._client[db]
        self.name_col = col
        self.rel_coll = self._db[col]

    def refresh_collection(self):
        self.rel_coll.drop()
        self.rel_coll = self._db[self.name_col]


import pandas as pd
from fuzzywuzzy import fuzz
import math
pd_file = pd.read_csv('27Mar2015_investor_relation.csv', encoding='utf-8')
mongodb_linkedin = Mongodb(host='localhost', db='linkedin', col='search_people')
#
# pd_file.fillna(' ')
# for index, row in pd_file.iterrows():
#     condition = {'company_name': "Not Name", 'name': row['name']}
#     print condition
#     mongodb_linkedin.rel_coll.update(condition, {'$set': {'company_name': row['company_name']}},multi=True)


for row in mongodb_linkedin.rel_coll.find({'name_linkedin': {'$exists': True}}):
    mongodb_linkedin.rel_coll.update({'_id': row['_id']}, {'$set': {'status': ''}})
    name_fuzz = fuzz.ratio(row['name'].lower(), row['name_linkedin'].lower())
    first_condition = True if name_fuzz > 75 else False

    list_word = (row['company_name'].lower().replace('ltd','')).split(' ')
    list_word.append('investor')
    list_word.append('invest')
    list_word.append('relation')
    list_word.append('relating')
    list_word_new = [word for word in list_word if len(word) > 3]

    second_condition = False
    if row['title'] not in ['',' ','--']:
        second_condition = (any(word in row['title'].lower() for word in list_word_new))
    if 'investor relation' in row['skill'].lower():
        second_condition = True

    if first_condition and second_condition:
        mongodb_linkedin.rel_coll.update({'_id': row['_id']}, {'$set': {'status': 'good'}})


