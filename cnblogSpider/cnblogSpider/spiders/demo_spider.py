import scrapy


class ArticleSpider(scrapy.Spider):
    name = 'article'  # 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字

    def start_requests(self):
        urls = [
            'https://www.cnblogs.com/yinminbo/p/12020198.html',            # 1.2、Answer：web crawler question 2
            'https://www.cnblogs.com/yinminbo/p/12050239.html',            # 单步调试调试leetcode代码
            'https://www.cnblogs.com/yinminbo/p/12034265.html']
        return [scrapy.Request(url=url, callback=self.parse)
                for url in urls]

    def parse(self, response):
        url = response.url
        title = response.css('title').extract()
        print('url is : {}'.format(url))
        print('title is {}'.format(title))
