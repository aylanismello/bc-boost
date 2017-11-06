import scrapy

# scrapy runspider ./scrapes/bossafy_scraper.py -a url=%s -a artist_name=%s -o %s
class InstagramSpider(scrapy.Spider):
    name = "instagram"

    def start_requests(self):
        urls = [
            'https://instagram.com/burncartel'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse:
        #
