# -*- coding: utf-8 -*-
import scrapy
from w3lib.html import remove_tags


class PkdexSpider(scrapy.Spider):
    name = 'attack'
    allowed_domains = ['https://pokemondb.net/']
    start_urls = ['https://pokemondb.net/move/all']

    def parse(self, response):
        print("processing: " + response.url)
        # pok = pokemon()

        attack_name = response.xpath(
            "//div[@class='resp-scroll']/table/tbody/tr/td[@class='cell-name']/a/text()").extract()

        attack_type = response.xpath(
            "//div[@class='resp-scroll']/table/tbody/tr/td[@class='cell-icon']/a/text()").extract()

        attack_cat = response.xpath(
            "//div[@class='resp-scroll']/table/tbody/tr/td[@class='cell-icon'][2]").extract()

        attack_cat_i = response.xpath(
            "//div[@class='resp-scroll']/table/tbody/tr/td[@class='cell-icon']/span/@data-src").extract()

        attack_power = response.xpath(
            "//div[@class='resp-scroll']/table/tbody/tr/td[@class='cell-num'][1]/text()").extract()

        attack_acc = response.xpath(
            "//div[@class='resp-scroll']/table/tbody/tr/td[@class='cell-num'][2]/text()").extract()

        attack_pp = response.xpath(
            "//div[@class='resp-scroll']/table/tbody/tr/td[@class='cell-num'][3]").extract()

        attack_tm = response.xpath(
            "//div[@class='resp-scroll']/table/tbody/tr/td[@class='cell-num'][4]").extract()

        attack_effect = response.xpath(
            "//div[@class='resp-scroll']/table/tbody/tr/td[@class='cell-long-text']").extract()

        attack_prob = response.xpath(
            "//div[@class='resp-scroll']/table/tbody/tr/td[@class='cell-num'][5]").extract()

        eff = list(map(remove_tags, attack_effect))
        cat = list(map(remove_tags, attack_cat))
        tm = list(map(remove_tags, attack_tm))
        pp = list(map(remove_tags, attack_pp))

        i = 0
        for idx, cat_i in enumerate(cat):
            if cat_i == '—':
                continue
            cat[idx] = attack_cat_i[i]
            i += 1

        print(cat)
        print(len(cat))

        row_data = zip(attack_name, attack_type, cat, attack_power,
                       attack_acc, pp, tm, eff)

        for item in row_data:
            scrapped_info = {
                'name': item[0],
                'type': item[1],
                'category': item[2],
                'power': item[3],
                'accuracy': item[4],
                'pp': item[5],
                'tm': item[6],
                'effect': item[7]
            }
            yield scrapped_info
