import scrapy

from common_data_spiders.items import AreaItem


class AreaSpider(scrapy.spiders.Spider):
    name = "area"
    allowed_domains = ["stats.gov.cn"]

    # based = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/"

    def start_requests(self):
        urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/index.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        self.log("###省份###")
        request_url = response.request.url

        based = request_url[0:request_url.rindex("/") + 1]

        # print(based)
        order = 0
        for sel in response.xpath('//tr[@class="provincetr"]'):

            urls = sel.xpath('td/a/@href').extract()
            names = sel.xpath('td/a/text()').extract()

            for index in range(len(names)):
                item = AreaItem()
                url = urls[index]
                item['code'] = url[0:url.rindex(".")].ljust(12, '0')
                item['name'] = names[index]
                item['p_code'] = None
                item['level'] = 1
                item['order'] = order
                yield item

                order = order + 1
                yield scrapy.Request(url=based + url, callback=self.parse_city, meta={'p_code': item['code']})

            # self.log("###城市###")
            # for url in urls:
            #     yield scrapy.Request(url=based + url, callback=self.parse_city)

    def parse_city(self, response):
        # self.log("###城市###")
        request_url = response.request.url
        based = request_url[0:request_url.rindex("/") + 1]
        p_code = response.meta['p_code']
        # print(based)
        order = 0
        for sel in response.xpath('//tr[@class="citytr"]'):
            url = sel.xpath('td[1]/a/@href').extract_first()
            code = sel.xpath('td[1]/a/text()').extract_first()
            name = sel.xpath('td[2]/a/text()').extract_first()

            item = AreaItem()

            item['p_code'] = p_code
            item['code'] = code
            item['name'] = name
            item['level'] = 2
            item['order'] = order

            yield item
            self.log("###区县###")
            yield scrapy.Request(url=based + url, callback=self.parse_country, meta={'p_code': item['code']})

            order = order + 1

    def parse_country(self, response):

        request_url = response.request.url
        based = request_url[0:request_url.rindex("/") + 1]
        p_code = response.meta['p_code']

        order = 0
        for sel in response.xpath('//tr[@class="countytr"]'):

            code = sel.xpath('td[1]/text()').extract_first()
            name = sel.xpath('td[2]/text()').extract_first()
            url = None
            if sel.xpath('td[1]/a'):
                url = sel.xpath('td[1]/a/@href').extract_first()
                code = sel.xpath('td[1]/a/text()').extract_first()
                name = sel.xpath('td[2]/a/text()').extract_first()

            item = AreaItem()
            item['p_code'] = p_code
            item['code'] = code
            item['name'] = name
            item['level'] = 3
            item['order'] = order

            yield item

            if url is not None:
                self.log("###乡镇###" + based + url)
                yield scrapy.Request(url=based + url, callback=self.parse_town, meta={'p_code': item['code']})

            order = order + 1

    def parse_town(self, response):

        request_url = response.request.url
        based = request_url[0:request_url.rindex("/") + 1]
        p_code = response.meta['p_code']

        order = 0
        for sel in response.xpath('//tr[@class="towntr"]'):

            code = sel.xpath('td[1]/text()').extract_first()
            name = sel.xpath('td[2]/text()').extract_first()
            url = None

            if sel.xpath('td[1]/a'):
                url = sel.xpath('td[1]/a/@href').extract_first()
                code = sel.xpath('td[1]/a/text()').extract_first()
                name = sel.xpath('td[2]/a/text()').extract_first()

            item = AreaItem()
            item['p_code'] = p_code
            item['code'] = code
            item['name'] = name
            item['level'] = 4
            item['order'] = order

            yield item

            if url is not None:
                self.log("###村镇###" + based + url + " " + item['name'])
                yield scrapy.Request(url=based + url, callback=self.parse_village, meta={'p_code': item['code']})

            order = order + 1

    def parse_village(self, response):

        p_code = response.meta['p_code']
        order = 0

        for sel in response.xpath('//tr[@class="villagetr"]'):
            code = sel.xpath('td[1]/text()').extract_first()
            name = sel.xpath('td[3]/text()').extract_first()

            item = AreaItem()
            item['p_code'] = p_code
            item['code'] = code
            item['name'] = name
            item['level'] = 5
            item['order'] = order
            yield item

            order = order + 1
