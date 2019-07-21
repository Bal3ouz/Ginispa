import scrapy
from ..items import Item
import datetime
import dateparser



class babnetSpider(scrapy.Spider):

    def __init__(self, nb):
        self.nbj = int(nb)

    name = "babnet"
    p_number=2


    start_urls = [
'https://www.babnet.net/politique.php?p=1'
    ]



    def parse(self, response):

        next_page = 'https://www.babnet.net/politique.php?p='+str(babnetSpider.p_number)+''
        iteration = True
        all_news = response.css('.arabi')

        for news in all_news :
            #extracting date
            date_french = news.css('.art-datte ::text').get()
            date_article = dateparser.parse(date_french)
            today = datetime.datetime.now()
            #calculating delta of article
            delta = (today-date_article).days
            #extracting lien
            lien ='https://www.babnet.net/'+news.css('a').xpath('@href').get()

            if delta <= self.nbj:
                yield scrapy.Request(lien, callback=self.parse_article,meta={'date':date_french,'lien':lien})
            else:
                iteration=False
                break

        if iteration:
            babnetSpider.p_number+=30
            yield response.follow(next_page,callback=self.parse)

    def parse_article(self,response):
        item = Item()
        item['title'] = response.css('.titrexx ::text').get()
        item['date'] = response.meta.get('date')
        item['lien'] = response.meta.get('lien')

        #la chaien d article manque d etre plus propre
        chaine = response.css('.article_ct ::text').getall()
        item['article']=chaine
        yield item