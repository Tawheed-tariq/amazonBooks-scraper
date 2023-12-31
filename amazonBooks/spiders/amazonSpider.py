"""
Scraping amazon books and storing them into a json file (not all the books data just some few 15-20 pages)
The amazon will not allow simple user to scrape the data so we have to use user agent 
To use user agent we look into browser  `https://explore.whatismybrowser.com/useragents/explore/software_name/googlebot/` and 
check here which user agent is suitable for our operating system and browser.
OR
we can also use python library `scrapy-proxy-pool` to use another ip address to scrape the data in any website
"""
import scrapy
from ..items import AmazonbooksItem

class AmazonspiderSpider(scrapy.Spider):
    name = "amazonSpider"
    allowed_domains = ["amazon.in"]
    pageNumber = 2
    start_urls = [
        "https://www.amazon.in/s?k=books&rh=p_90%3A20912642031&dc&page=1&crid=1WYNHOQK5Y1E5&qid=1704005868&rnid=6741116031&sprefix=books%2Caps%2C249&ref=sr_pg_2"
                ]



    def parse(self, response):
        items = AmazonbooksItem()

        name = response.css('span.a-color-base.a-text-normal').css('::text').extract()
        author = response.css('.a-color-secondary .a-row .a-size-base+ .a-size-base , .a-color-secondary .a-size-base.s-link-style').css('::text').getall()
        price = response.css('.puis-price-instructions-style .a-price-whole').css('::text').extract()
        img = response.css('.s-image::attr(src)').extract()

        items['title'] = name
        items['author'] = author
        items['price'] = price
        items['img'] = img
        yield items

        nextPage = "https://www.amazon.in/s?k=books&rh=p_90%3A20912642031&dc&page=" +str(AmazonspiderSpider.pageNumber)+ "&crid=1WYNHOQK5Y1E5&qid=1704005868&rnid=6741116031&sprefix=books%2Caps%2C249&ref=sr_pg_2"
        if AmazonspiderSpider.pageNumber <= 20:
            AmazonspiderSpider.pageNumber += 1
            yield response.follow(nextPage, callback=self.parse)