
import scrapy
from ..items import Item
import datetime
import dateparser


class tapinfoSpider(scrapy.Spider):

    def __init__(self, nb):
        self.nbj = int(nb)

    name = "tapinfo"
    p_number = 2

    start_urls = [
        'https://www.tap.info.tn/en/portal%20-%20politics?pg=1'
    ]

    def parse(self, response):

        next_page = 'https://www.tap.info.tn/en/portal%20-%20politics?pg=' + str(tapinfoSpider.p_number) + ''
        iteration = True
        all_news = response.css('#ctl09_ctl00_MAIN_TABLE td tr')

        for i in range(10):
            # extracting date
            date_french = all_news[1+i*5].css('td ::text').get().split(',')[0]
            date_article = dateparser.parse(date_french)
            today = datetime.datetime.now()
            # calculating delta of article
            delta = (today - date_article).days
            # extracting lien
            lien = all_news[i*5].css('td a').xpath('@href').get()

            if delta <= self.nbj:
                yield scrapy.Request(lien, callback=self.parse_article, meta={'date': date_french, 'lien': lien})
            else:
                iteration = False
                break

        if iteration:
            tapinfoSpider.p_number += 30
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        item = Item()
        item['title'] = response.css('.NewsItemHeadline ::text').get()
        item['date'] = response.meta.get('date')
        item['lien'] = response.meta.get('lien')

        # la chaien d article manque d etre plus propre
        chaine = response.css('p ::text').getall()
        item['article'] = chaine
        yield item