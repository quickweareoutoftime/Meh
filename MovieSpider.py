import scrapy
from Example.items import MovieItem

class MovieSpider(scrapy.Spider):
    name = "MovieSpider"
    allowed_domains = ["imdb.com"]
    start_urls = (
        'http://www.imdb.com/chart/top',
    )

    def parse(self, response):
        links = response.xpath('//tbody[@class="lister-list"]/tr/td[@class="titleColumn"]/a/@href').extract()
        i = 1
        for link in links[:5]:
            abs_url = response.urljoin(link)
            url_next =  '//*[@id="main"]/div/span/div/div/div[2]/table/tbody/tr['+str(i)+']/td[3]/strong/text()'
            rating = response.xpath(url_next).extract()
            if ( i <= len(links)):
                i += 1
            yield scrapy.Request(abs_url, callback = self.parse_indetail, meta={'rating' : rating})

    def parse_indetail(self, response):
        item = MovieItem()
        item['title'] = response.xpath('//div[@class="title_wrapper"]/h1/text()').extract()[0][:-1]
        # item['directors'] = response.xpath('//div[@class="credit_summary_item"]/span[@itemprop="director"]/a/span/text()').extract()
        item['directors'] = response.xpath('//div[@class="credit_summary_item"][1]/a/text()').extract()

        # item['writers'] = response.xpath('//div[@class="credit_summary_item"]/span[@itemprop="creator"]/a/span/text()').extract()
        tmp = response.xpath('//div[@class="credit_summary_item"][2]/a/text()').extract()
        if "more credit" in tmp[-1]:
            del tmp[-1]
        item['writers'] = tmp

        # item['stars'] = response.xpath('//div[@class="credit_summary_item"]/span[@itemprop="actors"]/a/span/text()').extract()
        tmp = response.xpath('//div[@class="credit_summary_item"][3]/a/text()').extract()
        del tmp[-1]
        item['stars'] = tmp

        item['popularity'] = response.xpath('//div[@class="titleReviewBarSubItem"]/div/span/text()').extract()[2][21:-8]

        return item


