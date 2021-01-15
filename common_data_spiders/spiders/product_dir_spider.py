import scrapy


class ProductDirSpider(scrapy.spiders.Spider):
    name = "productDir"
    allowed_domains = ["stats.gov.cn"]

    def start_requests(self):
        urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjypflml/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        request_url = response.request.url

        based = request_url[0:request_url.rindex("/") + 1]

        for sel in response.xpath('//ul[@class="center_list_contlist"]/li'):
            url = sel.xpath('a/@href').extract_first()
            name = sel.xpath('a/span/font[1]/text()').extract_first()

            print(url, name, based)
