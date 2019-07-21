import scrapy
from ..items import Item
import datetime
import dateparser


class TunivisionSpider(scrapy.Spider):


    name = "Tunivision"
    p_number=2
    start_urls = [
'https://tunivisions.net/category/politique/page/1/'    ]

    def parse(self,response):

        next_page = 'https://tunivisions.net/category/politique/page/'+str(TunivisionSpider.p_number)+'/'
        iteration = True
        all_news = response.css('.bd-col-md-4')

        for news in all_news :
            #extracting date
            chaine_date = news.css('.bdayh-date::text').get()
            splitted = chaine_date.split("/")
            date_article = datetime.datetime(int(splitted[2]), int(splitted[1]), int(splitted[0]))
            today = datetime.datetime.now()

            #calculating delta of article
            delta = (today-date_article).days

            if delta <= 1:
                lien=news.css('.bd-col-md-4 .entry-title a').xpath('@href').get()
                yield scrapy.Request(lien, callback=self.parse_article,meta={'date':chaine_date,'lien':lien})
            else:
                iteration=False
                break

        if iteration:
            TunivisionSpider.p_number+=1
            yield response.follow(next_page,callback=self.parse)

    def parse_article(self,response):
        item = Item()
        item['title'] = response.css('#content .entry-title span ::text').get()
        item['date'] = response.meta.get('date')
        item['lien'] = response.meta.get('lien')

        chaine = response.css('.bdaia-post-content p ::text').getall()

        item['article']=chaine
        yield item

