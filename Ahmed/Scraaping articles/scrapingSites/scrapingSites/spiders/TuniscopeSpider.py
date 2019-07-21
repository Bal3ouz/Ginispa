import scrapy
from ..items import Item
import datetime



class TuniscopeSpider(scrapy.Spider):

    def __init__(self, nb):
        self.nbj = int(nb)

    name = "Tuniscope"
    p_number=2
    iteration=True
    start_urls = [
'https://www.tuniscope.com/categorie?id_category=102&step=1' ]


    def parse(self,response):

        next_page = 'https://www.tuniscope.com/categorie?id_category=102&step='+str(TuniscopeSpider.p_number)+''
        all_news = response.css('.blog-cate')

        for news in all_news:

            #extracting lien
            lien=str(news.css('.blog-cate-title a').xpath('@href')[0].get())
            yield scrapy.Request(lien, callback=self.parse_article, meta={'lien': lien})


        if TuniscopeSpider.iteration:

            TuniscopeSpider.p_number+=1
            yield response.follow(next_page,callback=self.parse)

    def parse_article(self,response):

        # extracting date
        chaine_date = response.css('#inner-headline p::text').get().split(' ')[2]
        splitted = chaine_date.split('-')
        date_article = datetime.datetime(int(splitted[2]), int(splitted[1]), int(splitted[0]))
        today = datetime.datetime.now()
        # calculating delta of article
        delta = (today - date_article).days

        if delta <= self.nbj:
            chaine = response.css('#detail_article p::text').getall()
            item = Item()
            item['title'] = response.css('h2::text').get()
            item['date'] = chaine_date
            item['lien'] = response.meta.get('lien')
            item['article']=chaine
            yield item

        else:
            TuniscopeSpider.iteration = False


