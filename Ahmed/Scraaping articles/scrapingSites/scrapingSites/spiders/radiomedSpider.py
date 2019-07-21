import scrapy
from ..items import Item
import datetime
import dateparser



class radiomedSpider(scrapy.Spider):

    def __init__(self,nb):
        self.nbj = int(nb)

    name = "radiomed"
    p_number=2


    start_urls = [
'https://radiomedtunisie.com/fr/category/actualites-radiomed/actualites-politiques/page/1/'
    ]



    def parse(self, response):

        next_page = 'https://radiomedtunisie.com/fr/category/actualites-radiomed/actualites-politiques/page/'+str(radiomedSpider.p_number)+'/'
        iteration = True
        all_news = response.css('.post-item')

        for news in all_news :
            #extracting date
            date = news.css('.date span ::text').get()
            date_article = dateparser.parse(date)
            today = datetime.datetime.now()
            #calculating delta of article
            delta = (today-date_article).days
            #extracting lien
            lien=news.css('.post-title a').xpath('@href').get()

            if delta <= self.nbj:
                yield scrapy.Request(lien, callback=self.parse_article,meta={'date':date,'lien':lien})
            else:
                iteration=False
                break

        if iteration:
            radiomedSpider.p_number+=1
            yield response.follow(next_page,callback=self.parse)

    def parse_article(self,response):
        item = Item()
        item['title'] = response.css('.entry-title ::text').get()
        item['date'] = response.meta.get('date')
        item['lien'] = response.meta.get('lien')
        chaine = response.css('p ::text').get()
        item['article']=chaine
        yield item