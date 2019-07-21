import scrapy
from ..items import Item
import datetime
import dateparser



class MosaiqueSpider(scrapy.Spider):

    def __init__(self,nb):
        self.nbj = int(nb)

    name = "Mosaique"
    p_number=2


    start_urls = [
'https://www.mosaiquefm.net/fr/actualites/actualite-politique-tunisie/4/1'
    ]



    def parse(self, response):

        next_page = 'https://www.mosaiquefm.net/fr/actualites/actualite-politique-tunisie/4/'+str(MosaiqueSpider.p_number)+''
        iteration = True
        all_news = response.css('.news')

        for news in all_news :
            #extracting date
            date_french = news.css('.date::text').get()
            date_article = dateparser.parse(date_french)
            today = datetime.datetime.now()
            #calculating delta of article
            delta = (today-date_article).days
            #extracting lien
            lien = 'https://www.mosaiquefm.net'+news.css('.title a').xpath('@href')[0].get()

            if delta <= self.nbj:
                yield scrapy.Request(lien, callback=self.parse_article,meta={'date':date_french,'lien':lien})
            else:
                iteration=False
                break

        if iteration:
            MosaiqueSpider.p_number+=1
            yield response.follow(next_page,callback=self.parse)

    def parse_article(self,response):
        item = Item()
        item['title'] = response.css('h1 ::text').get()
        item['date'] = response.meta.get('date')
        item['lien'] = response.meta.get('lien')
        chaine = response.css('p[style="text-align: justify;"] ::text').getall()
        item['article']=chaine
        yield item