import scrapy
from ..items import Item
import datetime
import dateparser



class LaPresseSpider(scrapy.Spider):

    def __init__(self,nb):
        self.nbj = int(nb)

    name = "LaPresse"
    p_number=2


    start_urls = [
'https://lapresse.tn/category/politique-nationale/page/1/'
    ]



    def parse(self, response):

        next_page = 'https://lapresse.tn/category/politique-nationale/page/'+str(LaPresseSpider.p_number)+'/'
        iteration = True
        all_news = response.css('.bd-col-md-6 article')

        for news in all_news :
            #extracting date
            date = news.css('.bdayh-date ::text').get()
            splitted = date.split("/")
            date_article = datetime.datetime(int(splitted[2]), int(splitted[1]), int(splitted[0]))
            today = datetime.datetime.now()
            #calculating delta of article
            delta = (today-date_article).days
            #extracting lien
            lien=news.css('.block-article-content-wrapper .entry-title a').xpath('@href').get()

            if delta <= self.nbj:
                yield scrapy.Request(lien, callback=self.parse_article,meta={'date':date,'lien':lien})
            else:
                iteration=False
                break

        if iteration:
            LaPresseSpider.p_number+=1
            yield response.follow(next_page,callback=self.parse)

    def parse_article(self,response):
        item = Item()
        item['title'] = response.css('.entry-title span ::text').get()
        item['date'] = response.meta.get('date')
        item['lien'] = response.meta.get('lien')
        if len(response.css('.p1'))==0:
            chaine = response.css('.bdaia-post-content p ::text').getall()
        else:
            chaine = response.css('.p1 ::text').getall()

        item['article']=chaine
        yield item