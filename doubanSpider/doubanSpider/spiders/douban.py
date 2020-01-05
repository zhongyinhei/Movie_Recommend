import scrapy
from doubanSpider.items import DoubanspiderItem


class DoubanSpider(scrapy.Spider):
    name = 'Douban'  # 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字

    allowed_domains=['movie.douban.com']

    start = 0

    url = 'https://movie.douban.com/top250?start='

    end = '&filter'

    start_urls = [url + str(start) + end]

    def parse(self, response):

        item = DoubanspiderItem()

        movies = response.xpath("//div[@class=\'info\']")

        for movie in movies:

            name = movie.xpath('div[@class="hd"]/a/span/text()').extract()

            message = movie.xpath('div[@class="bd"]/p/text()').extract()

            star = movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()

            number = movie.xpath('div[@class="bd"]/div[@class="star"]/span/text()').extract()

            quote = movie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()

            if quote:
                quote = quote[0]
            else:
                quote = ''

            item['title'] = ''.join(name)
            item['info'] = quote
            item['score'] = star[0]
            item['content'] = ';'.join(message).replace(' ', '').replace('\n', '')
            item['number'] = number[1].split('人')[0]

            # 提交item
            yield item

        if self.start <= 225:
            self.start += 25
            yield scrapy.Request(self.url + str(self.start) + self.end, callback=self.parse)