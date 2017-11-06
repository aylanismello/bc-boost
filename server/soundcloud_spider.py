import scrapy
import re
import os
from IPython import embed


# scrapy runspider ./scrapes/bossafy_scraper.py -a url=%s -a artist_name=%s -o %s
class SoundcloudSpider(scrapy.Spider):
    name = "soundcloud"

    def __init__(self):
        self.start_urls = ['https://soundcloud.com/burncartel']

    def get_value_from_key(self, key, html):
        # result = re.search(f'followers_count":\d+', html).group(0)
        result = re.search(f'{re.escape(key)}":\d+', html).group(0)
        result = re.search('\d+', result).group(0)
        return result

    def parse(self, response):
        with open(f'{os.getcwd()}/server/data/soundcloud.csv', 'w+') as f:
            # followers_count = re.search('followers_count":\d+', response.text).group(0)
            # followers_count = re.search('\d+', followers_count).group(0)
            followers_count = self.get_value_from_key('followers_count', response.text)
            track_count = self.get_value_from_key('track_count', response.text)
            f.write(response.text)

        # yield response.text
        # print(response.text)
        # x = 'yo'
        # print(f'{x}')
        # html = response.text
        # # print(value)
        # print(followers_count)


# SoundcloudSpider().start_requests()
