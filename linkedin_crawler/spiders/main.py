__author__ = 'nhat'

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.utils.project import get_project_settings
from linkedin_crawling_prenium_account import AutoRobot_Prenium as AutoRobot_Prenium
import pandas as pd
from pymongo import MongoClient

class ReactorControl:
    def __init__(self):
        self.crawlers_running = 0

    def add_crawler(self):
        self.crawlers_running += 1

    def remove_crawler(self):
        self.crawlers_running -= 1
        if self.crawlers_running == 0:
            reactor.stop()


def setup_crawler():
    crawler = Crawler(settings)
    crawler.configure()
    crawler.signals.connect(reactor_control.remove_crawler, signal=signals.spider_closed)
    spider = AutoRobot_Prenium()
    crawler.crawl(spider)
    reactor_control.add_crawler()
    crawler.start()


if __name__ == "__main__":
    print '========================================'
    print 'Running all spiders to get data in BW'
    # Scrapy spiders script...

    reactor_control = ReactorControl()

    settings = get_project_settings()
    crawler = Crawler(settings)
    # Create crawler
    setup_crawler()
    reactor.run()

    print 'Finishing all spiders to get data in BW'
    print '========================================'

