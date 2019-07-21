import scrapy
from ..items import Item
import datetime
import dateparser


class ifmSpider(scrapy.Spider):

    def __init__(self, nb):
        self.nbj = int(nb)

    name = "ifm"
    p_number=2
    iteration=True
    start_urls = [
'https://www.ifm.tn/ar/actualite/5/%D8%B3%D9%8A%D8%A7%D8%B3%D8%A9?page=1' ]

    def parse(self, response):
        next_page = 'https://www.ifm.tn/ar/actualite/5/%D8%B3%D9%8A%D8%A7%D8%B3%D8%A9?page=' + str(ifmSpider.p_number) + ''
        iteration = True
        all_news = response.css('.actu-wrapper')
        for news in all_news:
            #extract lien
            lien=str(news.css('.actu-title a').xpath('@href').get())
            yield scrapy.Request(lien, callback=self.parse_article,meta={'lien':lien})


        if ifmSpider.iteration:
            ifmSpider.p_number+=1
            yield response.follow(next_page,callback=self.parse)


    def parse_article(self, response):

        chaine_date =  response.css('.article_date span ::text')[1].get()
        date_article = dateparser.parse(chaine_date)
        today = datetime.datetime.now()
        # calculating delta of article
        delta = (today - date_article).days

        if delta <= self.nbj:
            item = Item()
            item['title'] = response.css('h1 ::text').get()
            item['lien'] = response.meta.get('lien')
            item['date']= chaine_date
            chaine = response.css('.actu-desc p ::text').getall()
            item['article'] = chaine
            yield item
        else:
            ifmSpider.iteration = False




