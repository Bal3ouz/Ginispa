import scrapy
from ..items import Item
import re
import datetime


class KapitalisSpider(scrapy.Spider):
    def __init__(self, nb):
        self.nbj = int(nb)
    name = "Kapitalis"
    p_number=2
    start_urls = [
        'http://kapitalis.com/tunisie/category/politique/page/1/?fbclid=IwAR3SUFIb-Foo2xn9Hg9qRyjzX68Gr05kBIFcUfvBbww13ZJDiA11jtRew1A'

    ]

    def parse(self,response):

        next_page='http://kapitalis.com/tunisie/category/politique/page/'+str(KapitalisSpider.p_number)+'/?fbclid=IwAR3SUFIb-Foo2xn9Hg9qRyjzX68Gr05kBIFcUfvBbww13ZJDiA11jtRew1A'
        iteration=True

        for href in response.css('.post-news').css('.post_title h3 a').xpath('@href'):
            #extracting date
            chaine_date = re.findall('[0-9]{4}\/[0-9]{2}\/[0-9]{2}', str(href))[0]
            splitted=chaine_date.split("/")
            date_article  = datetime.datetime(int(splitted[0]),int(splitted[1]),int(splitted[2]))
            today = datetime.datetime.now()
            #calculating delta of article
            delta = (today-date_article).days
            lien=href.extract()

            if delta<= self.nbj:
                yield scrapy.Request(lien, callback=self.parse_article,meta={'date':chaine_date,'lien':lien})
            else:
                iteration=False
                break


        if(iteration):
            KapitalisSpider.p_number+=1
            yield response.follow(next_page,callback=self.parse)



    def parse_article(self,response):
        item=Item()
        item['title']=response.css('title ::text').get()
        item['date']=response.meta.get('date')
        item['lien']=response.meta.get('lien')

        all_p=response.css('span~ p, em')
        chaine=""
        for para in all_p:
            chaine+=re.sub("<[^>]*>","",para.get())

        item['article']=chaine
        yield item





