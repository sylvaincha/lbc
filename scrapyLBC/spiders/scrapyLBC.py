#!/usr/bin/env python3

"""Title : scrapyLBC
Author : Sigri44 (sigri44.github.io)
Description : scrapyLBC is a spider which collect data from www.leboncoin.fr.
"""

import scrapy

class LeboncoinSpider(scrapy.Spider):
    """Crawl all the pagination links to scrap the data of every ads.
    """
    name = "leboncoin"
    start_urls = [
        'https://www.leboncoin.fr/recherche/?category=9&locations=Vitry-sur-Seine_94400,Villejuif_94800,Ivry-sur-Seine_94200,Clamart_92140,Montrouge_92120,Montreuil_93100,Paris,Le%20Kremlin-Bic%C3%AAtre,Gentilly_94250,Bagneux_92220&real_estate_type=1,3',
    ]
    custom_settings = {
        'COOKIES_ENABLED': False,
        'DOWNLOAD_DELAY': 2.1,
        'DEFAULT_REQUEST_HEADERS': {
            'Referer': 'https://images.google.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
        }
    }

    def parse(self, response_list):
        """Scrap and parse the page containing the ads and pagination.
        """
        # follow links to advertissement pages
        for ad_link in response_list.css('a.list_item'):
            description_page = ad_link.css('a::attr("href")').extract_first()
            yield response_list.follow(description_page, self.parse_description)

        # follow pagination link
        next_list = response_list.css('li.next a::attr("href")').extract_first()
        if next_list is not None:
            yield response_list.follow(next_list, self.parse)

    def parse_description(self, response):
        """Scrap and parse the content of the ads page.
        """
        # check if the phone button exist then return phone number
        phone_button = response.css('button.button-orange.large.phoneNumber.trackable')\
                             .extract_first()
        if phone_button is not None:
            phone = 'Oui'
        else:
            phone = 'Non'

        # export data
        return {
            'Url': response.url,
            'Titre': response.css("h1::text").extract_first().strip(),
            'Prix': response.css("h2.item_price.clearfix > span.value::text")\
                               .extract_first().strip(),
            'Surface': response.xpath('//div[9]/h2/span[2]/text()')\
                                  .extract_first().strip('m').strip(),
            'GES': response.xpath('//div[10]/h2/span[2]/a/text()')\
                              .extract_first(),
            'Classe énergie': response.xpath('//div[11]/h2/span[2]/a/text()')\
                                         .extract_first(),
            'Auteur': response.css('a[data-info*="pseudo_annonceur"]::text')\
                                 .extract_first().strip(),
            'Téléphone': phone,
            'Remarques': ''
        }
