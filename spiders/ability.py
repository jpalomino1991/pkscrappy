# -*- coding: utf-8 -*-
import scrapy


class PkdexSpider(scrapy.Spider):
    name = 'ability'
    allowed_domains = ['https://pokemondb.net/']
    start_urls = ['https://pokemondb.net/ability']

    def parse(self, response):
        print("processing: " + response.url)

        ability_name = response.xpath(
            "//table[@id='abilities']/tbody/tr/td/a/text()").extract()

        ability_desc = response.xpath(
            "//table[@id='abilities']/tbody/tr/td[@class='cell-med-text']/text()").extract()

        print(ability_desc)

        row_data = zip(ability_name, ability_desc)

        for item in row_data:
            scrapped_info = {
                'name': item[0],
                'description': item[1],
            }
            yield scrapped_info
