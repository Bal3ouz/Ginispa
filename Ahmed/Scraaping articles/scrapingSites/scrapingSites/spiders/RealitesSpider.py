import scrapy
from ..items import Item
import datetime
import dateparser



class RealitesSpider(scrapy.Spider):
    def __init__(self, nb):
        self.nbj = int(nb)

    name = "Realites"
    p_number=2
    iteration=True
    start_urls = [
'https://www.realites.com.tn/category/politique/page/1/' ]


    def parse(self,response):

        next_page = 'https://www.realites.com.tn/category/politique/page/'+str(RealitesSpider.p_number)+'/'
        all_news =response.css('.content-main-wrap .main-term-5')

        for news in all_news:

            #extracting lien
            lien=str(news.css('.title a').xpath('@href')[0].get())
            yield scrapy.Request(lien, callback=self.parse_article, meta={'lien': lien})


        if RealitesSpider.iteration:

            RealitesSpider.p_number+=1
            yield response.follow(next_page,callback=self.parse)

    def parse_article(self,response):

        # extracting date
        chaine_date = response.css('.time b::text').get()
        date_article = dateparser.parse(chaine_date)
        today = datetime.datetime.now()
        # calculating delta of article
        delta = (today - date_article).days

        if delta <= self.nbj:
            chaine =  response.css('.single-post-content p::text').getall()
            item = Item()
            item['title'] = response.css('.single-post-title .post-title::text').getall()
            item['date'] = chaine_date
            item['lien'] = response.meta.get('lien')
            item['article']=chaine
            yield item

        else:
            RealitesSpider.iteration = False