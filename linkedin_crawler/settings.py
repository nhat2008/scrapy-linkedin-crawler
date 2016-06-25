# -*- coding: utf-8 -*-

# Scrapy settings for linkedin_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'linkedin_crawler'

SPIDER_MODULES = ['linkedin_crawler.spiders']
NEWSPIDER_MODULE = 'linkedin_crawler.spiders'

DOWNLOADER_MIDDLEWARES = {
    'linkedin_crawler.middleware.CustomHttpProxyMiddleware': 543,
    'linkedin_crawler.middleware.CustomUserAgentMiddleware': 545,
}


LINKEDIN_ACCOUNT = 'nhatpandas@gmail.com'
LINKEDIN_PASSWORD = ''


LINKEDIN_ACCOUNT_PRENIUM = ''
LINKEDIN_PASSWORD_PRENIUM = ''
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'linkedin_crawler (+http://www.yourdomain.com)'
