import scrapy
from ..items import Item
import datetime
import dateparser



class tunisienumeriqueSpider(scrapy.Spider):

    def __init__(self,nb):
        self.nbj = int(nb)

    name = "tn"
    p_number=2
    iteration=True
    start_urls = [
'https://www.tunisienumerique.com/actualite-tunisie/politique/page/1/' ]


    def parse(self,response):

        next_page = 'https://www.tunisienumerique.com/actualite-tunisie/politique/page/'+str(tunisienumeriqueSpider.p_number)+'/'
        all_news =response.css('.infinite-post')

        for news in all_news:

            #extracting lien
            lien=str(news.css('a').xpath('@href')[0].get())
            yield scrapy.Request(lien, callback=self.parse_article, meta={'lien': lien})


        if tunisienumeriqueSpider.iteration:

            tunisienumeriqueSpider.p_number+=1
            yield response.follow(next_page,callback=self.parse)

    def parse_article(self,response):

        # extracting date
        chaine_date = response.css('time').xpath('@datetime').get()
        date_article = dateparser.parse(str(chaine_date))
        today = datetime.datetime.now()
        # calculating delta of article
        delta = (today - date_article).days

        if delta <= self.nbj:
            chaine =  response.css('#content-main p::text').getall()
            item = Item()
            item['title'] = response.css('.post-title.entry-title::text').get()
            item['date'] = chaine_date
            item['lien'] = response.meta.get('lien')
            item['article']=chaine
            yield item

        else:
            tunisienumeriqueSpider.iteration = False