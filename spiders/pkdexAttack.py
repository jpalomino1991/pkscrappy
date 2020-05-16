# -*- coding: utf-8 -*-
import scrapy
import json
from w3lib.html import remove_tags


class PkdexAttackSpider(scrapy.Spider):

    name = 'pkdexAttack'
    allowed_domains = []
    start_urls = ['https://pokemondb.net/pokedex/bulbasaur']

    def parse(self, response):
        print("processing: " + response.url)

        pok_name = response.xpath(
            "//main[@class='main-content grid-container']/h1/text()").extract_first()

        loop = 0
        level_up = response.xpath(
            "(//h3[contains(.,'Moves learnt by level up')])[1]/following-sibling::div[1]/table[1]/tbody/tr/td").extract()

        if len(level_up) > 0:
            level_up_cat = response.xpath(
                "(//h3[contains(.,'Moves learnt by level up')])[1]/following-sibling::div[1]/table[1]/tbody/tr/td[@class='cell-icon']/span/@data-src").extract()

            list1 = list(map(remove_tags, level_up))

            for i in range(len(level_up_cat)):
                scrapped_info = {
                    'Name': pok_name,
                    'Lv': list1[i + loop],
                    'Move': list1[i + 1 + loop],
                    'Type': list1[i + 2 + loop],
                    'Category': level_up_cat[i],
                    'Power': list1[i + 4 + loop],
                    'Accuracy': list1[i + 5 + loop],
                    'TM': '',
                    'TR': '',
                }
                loop += 5
                yield scrapped_info

        egg_moves = response.xpath(
            "(//h3[contains(.,'Egg moves')])[1]/following-sibling::div[1]/table[1]/tbody/tr/td").extract()

        if len(egg_moves) > 0:
            egg_moves_cat = response.xpath(
                "(//h3[contains(.,'Egg moves')])[1]/following-sibling::div[1]/table[1]/tbody/tr/td[@class='cell-icon']/span/@data-src").extract()

            list2 = list(map(remove_tags, egg_moves))
            loop = 0
            for i in range(len(egg_moves_cat)):
                scrapped_info = {
                    'Name': pok_name,
                    'Lv': '',
                    'Move': list2[i + loop],
                    'Type': list2[i + 1 + loop],
                    'Category': egg_moves_cat[i],
                    'Power': list2[i + 3 + loop],
                    'Accuracy': list2[i + 4 + loop],
                    'TM': '',
                    'TR': '',
                }
                loop += 4
                yield scrapped_info

        tm = response.xpath(
            "(//h3[contains(.,'Moves learnt by TM')])[1]/following-sibling::div[1]/table[1]/tbody/tr/td").extract()

        if len(tm) > 0:
            tm_cat = response.xpath(
                "(//h3[contains(.,'Moves learnt by TM')])[1]/following-sibling::div[1]/table[1]/tbody/tr/td[@class='cell-icon']/span/@data-src").extract()

            list3 = list(map(remove_tags, tm))
            loop = 0
            for i in range(len(tm_cat)):
                scrapped_info = {
                    'Name': pok_name,
                    'Lv': '',
                    'Move': list3[i + 1 + loop],
                    'Type': list3[i + 2 + loop],
                    'Category': tm_cat[i],
                    'Power': list3[i + 4 + loop],
                    'Accuracy': list3[i + 5 + loop],
                    'TM': list3[i + loop],
                    'TR': '',
                }
                loop += 5
                yield scrapped_info

        tr = response.xpath(
            "(//h3[contains(.,'Moves learnt by TR')])[1]/following-sibling::div[1]/table[1]/tbody/tr/td").extract()

        if len(tr) > 0:
            tr_cat = response.xpath(
                "(//h3[contains(.,'Moves learnt by TR')])[1]/following-sibling::div[1]/table[1]/tbody/tr/td[@class='cell-icon']/span/@data-src").extract()

            list4 = list(map(remove_tags, tr))
            loop = 0
            for i in range(len(tr_cat)):
                scrapped_info = {
                    'Name': pok_name,
                    'Lv': '',
                    'Move': list4[i + 1 + loop],
                    'Type': list4[i + 2 + loop],
                    'Category': tr_cat[i],
                    'Power': list4[i + 4 + loop],
                    'Accuracy': list4[i + 5 + loop],
                    'TM': '',
                    'TR': list4[i + loop],
                }
                loop += 5
                yield scrapped_info

        next_page = response.xpath(
            "//a[@class='entity-nav-next']/@href").extract_first()

        if next_page:
            yield scrapy.Request(
                response.urljoin("https://pokemondb.net" + next_page),
                callback=self.parse)

        print(next_page)
