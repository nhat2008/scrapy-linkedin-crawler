__author__ = 'nhat'

from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
from scrapy.selector import HtmlXPathSelector
from pymongo import MongoClient
from linkedin_crawler.parser.HtmlParser import HtmlParser
from bs4 import UnicodeDammit
import urllib
import time
from random import randrange, uniform


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


class AutoRobot_Prenium_Links(InitSpider):
    name = 'LinkedinSpider_prenium_links'
    allowed_domains = ['linkedin.com']
    start_urls = []
    login_page = 'https://www.linkedin.com/uas/login'
    DOWNLOAD_DELAY = 10

    def init_links(self):
        self.mongodb_linkedin = Mongodb(host='localhost', db='linkedin', col='investor')
        for row in self.mongodb_linkedin.rel_coll.find():
            self.start_urls.append(row['linkedin'])
            print row['linkedin']
        # self.start_urls.append('https://www.linkedin.com/profile/view?id=52869925&authType=NAME_SEARCH&authToken=2k1k&locale=en_US&trk=tyah&trkInfo=clickedVertical%3Amynetwork%2Cidx%3A1-1-1%2CtarId%3A1428725803627%2Ctas%3ADuy')

    def init_request(self):
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        print self.settings['LINKEDIN_ACCOUNT']
        return FormRequest.from_response(response,
                    formdata={'session_key': self.settings['LINKEDIN_ACCOUNT_PRENIUM'], 'session_password': self.settings['LINKEDIN_PASSWORD_PRENIUM']},
                    callback=self.check_login_response)

    def check_login_response(self, response):
        if "Sign Out" in response.body:
            self.log("\n\n\nSuccessfully logged in. Let's start crawling!\n\n\n")
            # Now the crawling can begin..

            return self.initialized() # ****THIS LINE FIXED THE LAST PROBLEM*****

        else:
            self.log("\n\n\nFailed, Bad times :(\n\n\n")
            # Something went wrong, we couldn't log in, so nothing happens.

    def __init__(self):
        self.mongodb_linkedin_links = Mongodb(host='localhost', db='linkedin', col='investor_links')
        self.init_links()
        pass

    def parse(self, response):
        """
        default parse method, rule is not useful now
        """
        time.sleep(uniform(1, 10))
        print response.url
        # response = response.replace(url=HtmlParser.remove_url_parameter(response.url))
        hxs = HtmlXPathSelector(response)
        try:
            new_link = hxs.select('//a[@class="browse-map-photo"]/@href').extract()[0]
            self.mongodb_linkedin_links.rel_coll.update({'linkedin':new_link}, {'$set':{'linkedin':new_link}}, upsert=True)
        except Exception as e:
            print e

    def determine_level(self, response):
        """
        determine the index level of current response, so we can decide wether to continue crawl or not.
        level 1: people/[a-z].html
        level 2: people/[A-Z][\d+].html
        level 3: people/[a-zA-Z0-9-]+.html
        level 4: search page, pub/dir/.+
        level 5: profile page
        """
        import re
        url = response.url
        if 'search=Search' in url:
            return 2
        elif 'profile' in url:
            return 2
        return 2
        return None

    @staticmethod
    def get_linkedin_id(url):
        find_index = url.find("www.linkedin.com/")
        if find_index >= 0:
            return url[find_index + 13:].replace('/', '-')
        return None

    @staticmethod
    def get_follow_links(level, hxs):
        if level in [1, 2, 3]:
            relative_urls = hxs.select("//ul[@class='column dual-column']/li/a/@href").extract()
            relative_urls = ["http://www.linkedin.com" + x for x in relative_urls if 'linkedin.com' not in x]
            return relative_urls
        elif level == 4:
            relative_urls = relative_urls = hxs.select("//ol[@id='result-set']/li/h2/strong/a/@href").extract()
            relative_urls = ["http://www.linkedin.com" + x for x in relative_urls]
            return relative_urls

    @staticmethod
    def get_top_profile(number_profiles, hxs):
        profile_links = hxs.select('//div[@id="results-container"]/ol/li/a/@href').extract()
        return profile_links[0:number_profiles]
