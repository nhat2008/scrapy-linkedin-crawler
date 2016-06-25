import time

__author__ = 'khoi'
from selenium import webdriver
from pymongo import MongoClient
import HTMLParser
from linkedin_crawler import settings
from pandas import read_csv as readcsv
import random
if __name__ == "__main__":

    MAIN_DB_HOST = 'localhost'
    MAIN_DB_PORT = 27017
    REL_DB = 'linkedin'
    REL_COLL = 'investor'

    client = MongoClient(MAIN_DB_HOST, MAIN_DB_PORT)
    rel_coll = client[REL_DB][REL_COLL]
    start_urls = []
    html_parser = HTMLParser.HTMLParser()

    start_urls.append("https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Fvsearch%2Fp%3Fkeywords%3DInvestor%2BRelations%26titleScope%3DCP%26title%3DInvestor%2BRelations%26sb%3DPeople%2Bwith%2BInvestor%2BRelations%2Btitles%26trkInfo%3DclickedVertical%253Asuggestion%252Cidx%253A1-2-2%252CtarId%253A1428488273653%252Ctas%253Ainvestor%2B%26trk%3Dtyah&fromSignIn=true&trk=uno-reg-join-sign-in")
    chromedriver = webdriver.Firefox()
    chromedriver.get(start_urls[0])

    username = chromedriver.find_element_by_id("session_key-login")
    password = chromedriver.find_element_by_id("session_password-login")
    username.send_keys(settings.LINKEDIN_ACCOUNT_PRENIUM)
    password.send_keys(settings.LINKEDIN_PASSWORD_PRENIUM)

    chromedriver.find_element_by_name("signin").click()

    time.sleep(2)

    while True:
        for i in range(1, 11):
            try:
                string_query = '//*[@class="search-results"]/li[' + str(i) + ']/a'
                profiles = chromedriver.find_element_by_xpath(string_query)
                linkedin = profiles.get_attribute('href')
                print linkedin
                # rel_coll.insert({'linkedin':linkedin})
            except Exception as e:
                print e

        try:
            string_query = '//*[@class="next"]/a'
            next = chromedriver.find_element_by_xpath(string_query)
            next.click()
        except Exception as e:
            print e

        time.sleep(random.uniform(5, 10))



    #
    # pd_file = readcsv('27Mar2015_investor_relation.csv')
    # count = 0
    # for index, row in pd_file.iterrows():
    #     count += 1
    #     if count == 20:
    #         time.sleep(10)
    #         count = 0
    #     sub_names = row['name'].split(' ')
    #     sub_names = [sub_name.replace(' ', '') for sub_name in sub_names if sub_name != '']
    #     name = " ".join(sub_names)
    #     try:
    #         search_inbox = chromedriver.find_element_by_name("keywords")
    #
    #         search_inbox.send_keys(name)
    #         chromedriver.find_element_by_name("search").click()
    #
    #         for i in range(2, 7):
    #             try:
    #                 string_query = '//*[@class="search-results"]/li[' + str(i) + ']/a'
    #                 profiles = chromedriver.find_element_by_xpath(string_query)
    #                 linkedin = profiles.get_attribute('href')
    #                 title = row['title_bloomberg'] if row['title_bloomberg'] not in ['', ' '] else row['title']
    #                 rel_coll.update({'linkedin': linkedin},
    #                                 {'$set': {'item_id': row['item_id'], 'o_title': title, 'name': name}}, upsert=True)
    #             except Exception as e:
    #                 continue
    #         chromedriver.find_element_by_name("keywords").clear()
    #     except Exception as e:
    #         print 'error at >>>>>>>>>>>>>>>', name

