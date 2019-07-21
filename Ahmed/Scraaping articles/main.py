import sys
from scrapy.crawler import CrawlerProcess
from scrapingSites.scrapingSites.spiders.MosaiqueSpider import MosaiqueSpider
from scrapingSites.scrapingSites.spiders.ifmSpider import ifmSpider
from scrapingSites.scrapingSites.spiders.JawharaArSpider import JawharaArSpider
from scrapingSites.scrapingSites.spiders.RealitesSpider import RealitesSpider
from scrapingSites.scrapingSites.spiders.TuniscopeSpider import TuniscopeSpider
from scrapingSites.scrapingSites.spiders.tunisienumeriqueSpider import tunisienumeriqueSpider
from scrapingSites.scrapingSites.spiders.KapitalisSpider import KapitalisSpider
from scrapingSites.scrapingSites.spiders.TunivisionSpider import TunivisionSpider
from scrapingSites.scrapingSites.spiders.radiomedSpider import radiomedSpider
from scrapingSites.scrapingSites.spiders.babnetSpider import babnetSpider


def main():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 ',
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'data.csv'
    })

    process.crawl(MosaiqueSpider, sys.argv[1])
    #jawhara en arabe
    process.crawl(JawharaArSpider, sys.argv[1])
    process.crawl(RealitesSpider, sys.argv[1])
    process.crawl(TuniscopeSpider, sys.argv[1])
    process.crawl(tunisienumeriqueSpider, sys.argv[1])
    # ifm en arabe
    process.crawl(ifmSpider, sys.argv[1])
    process.crawl(KapitalisSpider, sys.argv[1])
    process.crawl(TunivisionSpider, sys.argv[1])
    process.crawl(radiomedSpider, sys.argv[1])
    #babnet en arabe 
    process.crawl(babnetSpider, sys.argv[1])
    process.start()


if __name__ == '__main__':
    main()

