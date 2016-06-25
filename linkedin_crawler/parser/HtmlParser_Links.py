from linkedin_crawler.items import PersonProfileItem
from bs4 import UnicodeDammit
from w3lib.url import url_query_cleaner
import random
import LinkedinParser


class HtmlParser_Links:
    @staticmethod
    def extract_person_profile(hxs):
        personProfile = PersonProfileItem()

        # id = HtmlParser.get_linkedin_id()
        name = hxs.select("//span[@class='full-name']//text()").extract()
        title = hxs.select('//div[@id="headline"]//text()').extract()
        location = hxs.select('//span[@class="locality"]/a//text()').extract()
        industry = hxs.select('//dd[@class="industry"]/a//text()').extract()

        overview_summary_current = hxs.select('//tr[@id="overview-summary-current"]/td//text()').extract()
        overview_summary_past = hxs.select('//tr[@id="overview-summary-past"]/td//text()').extract()
        overview_sumary_education = hxs.select('//tr[@id="overview-summary-education"]/td//text()').extract()

        linkedin_link = hxs.select('//div[@id="contact-public-url-view"]//text()').extract()
        linkedin_link2 = hxs.select('//dd[@class="view-public-profile"]/a/@href').extract()
        linkedin_link3 = hxs.select('//a[@class="view-public-profile"]/@href').extract()

        big_summary = hxs.select('//div[@class="summary"]//text()').extract()
        number_connection = hxs.select('//div[@class="member-connections"]/strong//text()').extract()

        email = hxs.select('//div[@id="relationship-emails-view"]/li/a//text()').extract()
        birthday = hxs.select('//div[@id="relationship-birthday-view"]//text()').extract()
        phone = hxs.select('//div[@id="relationship-phone-numbers-view"]/li//text()').extract()

        website = hxs.select('//div[@id="relationship-sites-view"]/li/a/@href').extract()

        span_skill = hxs.select('//span[@class="endorse-item-name"]//text()').extract()
        span_past_experience = hxs.select('//div[@class="editable-item section-item past-position"]/div/header//text()').extract()

        image = hxs.select('//div[@class="profile-picture"]/a/img/@src').extract()

        twitter = hxs.select('//div[@id="twitter-view"]/li/a/@href').extract()

        personProfile['twitter'] = ';'.join(twitter)
        personProfile['name_linkedin'] = ' '.join(name)
        personProfile['title'] = ' '.join(title)
        personProfile['location'] = ';'.join(location)
        personProfile['industry'] = ';'.join(industry)
        personProfile['current_company'] = ';'.join(overview_summary_current)
        personProfile['past_company'] = ';'.join(overview_summary_past)
        personProfile['education'] = ';'.join(overview_sumary_education)
        personProfile['url'] = ';'.join([linkedin_link[0] if len(linkedin_link) > 0 else '',
                                         linkedin_link2[0] if len(linkedin_link2) > 0 else '',
                                         linkedin_link3[0] if len(linkedin_link3) > 0 else ''])

        personProfile['summary'] = ' '.join(big_summary)
        personProfile['connection'] = number_connection[0] if len(number_connection) > 0 else ''
        personProfile['email'] = ';'.join(email)
        personProfile['website'] = ';'.join(website)
        personProfile['birthday'] = ';'.join(birthday)
        personProfile['phone'] = ';'.join(phone)

        personProfile['skill'] = ';'.join(span_skill)
        personProfile['experience'] = ';'.join(span_past_experience)
        personProfile['image'] = image[0] if len(image) > 0 else ''

        return personProfile

    @staticmethod
    def get_also_view_item(dirtyUrl):
        item = {}
        url = HtmlParser.remove_url_parameter(dirtyUrl)
        item['linkedin_id'] = url 
        item['url'] = HtmlParser.get_linkedin_id(url)
        return item
        
    @staticmethod
    def remove_url_parameter(url):
        return url_query_cleaner(url)
    
    @staticmethod
    def get_linkedin_id(url):
        find_index = url.find("linkedin.com/")
        if find_index >= 0:
            return url[find_index + 13:].replace('/', '-')
        return None
