import scrapy

# scrapy runspider ./scrapes/bossafy_scraper.py -a url=%s -a artist_name=%s -o %s
class TwitterSpider(scrapy.Spider):
    name = "twitter"

    def start_requests(self):
        urls = [
            'https://twitter.com/burncartel'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse:
        #
