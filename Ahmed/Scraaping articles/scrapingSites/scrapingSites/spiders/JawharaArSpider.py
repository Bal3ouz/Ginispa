
import scrapy
from ..items import Item
import re
import datetime
import dateparser


class JawharaArSpider(scrapy.Spider):
    def __init__(self, nb):
        self.nbj = int(nb)
    name = "JawharaAr"
    p_number=2
    iteration=True
    start_urls = [
'https://www.jawharafm.net/ar/articles/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1/%D8%B3%D9%8A%D8%A7%D8%B3%D8%A9/44/1'    ]

    def parse(self, response):
        next_page = 'https://www.jawharafm.net/ar/articles/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1/%D8%B3%D9%8A%D8%A7%D8%B3%D8%A9/44/' + str(JawharaArSpider.p_number) + ''
        iteration = True
        all_news = response.css('.elem_ev')
        for news in all_news:

            #extracting date
            chaine_date = news.css('.dat_ev::text').get()
            date_article = dateparser.parse(chaine_date)
            today = datetime.datetime.now()

            #calculating delta of article
            delta = (today-date_article).days

            if delta <= self.nbj:
                lien='https://www.jawharafm.net'+str(news.css('.titr_ev a').xpath('@href').get())
                yield scrapy.Request(lien, callback=self.parse_article,meta={'date':chaine_date,'lien':lien})
            else:
                iteration=False
                break

        if iteration:
            JawharaArSpider.p_number+=1
            yield response.follow(next_page,callback=self.parse)


    def parse_article(self, response):
        item = Item()
        item['title'] = response.css('.titr_page ::text').get()
        item['date'] = response.meta.get('date')
        item['lien'] = response.meta.get('lien')

        chaine_with_html=response.css('.article_text div , .article_text p ::text').getall()
        chaine = re.sub("<[^>]*>", "", str(chaine_with_html))
        item['article'] = chaine
        yield item




