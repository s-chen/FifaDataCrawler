import scrapy

class FifaPlayerUrlsSpider(scrapy.Spider):
    name = "fifa_player_urls"

    def start_requests(self):
        urls = [
            'https://sofifa.com/players?col=oa&sort=desc&offset=0'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    
    def parse(self, response):
        for playerUrl in response.css('td.col-name a.tooltip::attr(href)'):
            link = playerUrl.get()
            yield {
                'playerUrl': link + '?attr=fut'
            }

        offset = response.url[51:]
        endOffset = 19260

        if int(offset) <= endOffset:
            nextPageLink = 'https://sofifa.com/players?col=oa&sort=desc&offset=' + str(int(offset) + 60)
            request = scrapy.Request(url=nextPageLink)
            yield request