import scrapy

# scrapy runspider ./scrapes/bossafy_scraper.py -a url=%s -a artist_name=%s -o %s
class FacebookSpider(scrapy.Spider):
    name = "facebook"

    def start_requests(self):
        urls = [
            'https://www.facebook.com/burncartel'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse:
        #
