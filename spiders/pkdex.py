# -*- coding: utf-8 -*-
import scrapy
import json
from w3lib.html import remove_tags


class pokemon:
    def __init__(self):
        self.name = ""
        self.type1 = ""
        self.type2 = ""
        self.nationalNo = ""
        self.height = ""
        self.weight = ""
        self.ability1 = ""
        self.ability2 = ""
        self.hiddenAbility = ""
        self.Aability1 = ""
        self.Aability2 = ""
        self.AhiddenAbility = ""
        self.Gability1 = ""
        self.Gability2 = ""
        self.GhiddenAbility = ""
        self.location = ""
        self.species = ""
        self.SHDesc = ""
        self.SWDesc = ""
        self.attack = ""
        self.hp = ""
        self.spA = ""
        self.spD = ""
        self.spe = ""
        self.deff = ""

    def __str__(self):
        return "%s %s %s %s %s %s %s" % (self.name, self.AhiddenAbility, self.GhiddenAbility, self.hiddenAbility, self.ability1, self.Gability2, self.Aability2)


class PkdexSpider(scrapy.Spider):
    name = 'pkdex'
    allowed_domains = []
    start_urls = ['https://pokemondb.net/pokedex/bulbasaur']

    def getNAbility(self, pok, pok_abilities, pok_HA):
        pok.ability1 = pok_abilities[0]
        if len(pok_abilities) > 1:
            pok.ability2 = pok_abilities[1]
        if len(pok_HA) > 0:
            pok.hiddenAbility = pok_HA[0]

    def getAAbility(self, pok, pok_abilities, pok_HA, begin, flag):
        pok.Aability1 = pok_abilities[begin]
        if len(pok_abilities) - begin > 1:
            pok.Aability2 = pok_abilities[begin + 1]
        if len(pok_HA) > 2:
            if(flag):
                pok.AhiddenAbility = pok_HA[begin // 2]
            else:
                pok.AhiddenAbility = pok_HA[begin]

    def getGAbility(self, pok, pok_abilities, pok_HA, begin, flag):
        pok.Gability1 = pok_abilities[begin]
        if len(pok_abilities) - begin > 1:
            pok.Gability2 = pok_abilities[begin]
        if len(pok_HA) > 2:
            if(flag):
                pok.GhiddenAbility = pok_HA[begin // 2]
            else:
                pok.GhiddenAbility = pok_HA[begin]

    def parse(self, response):
        print("processing: " + response.url)

        pok = pokemon()

        pok.SWDesc = response.xpath(
            "//span[@class='igame sword']/../../td/text()").extract_first()

        pok.SHDesc = response.xpath(
            "//span[@class='igame shield']/../../td/text()").extract_first()

        pok.location = response.xpath(
            "//span[@class='igame shield']/../../td/small/text()").extract_first()

        pok_data = response.xpath(
            "//div[@class='grid-col span-md-6 span-lg-4']/table/tbody/tr/td/text()").extract()

        pok.nationalNo = response.xpath(
            "//div[@class='grid-col span-md-6 span-lg-4']/table/tbody/tr/td/strong/text()").extract_first()

        pok_types = response.xpath(
            "//div[@class='grid-col span-md-6 span-lg-4']/table/tbody/tr/td/a/text()").extract()

        pok_abilities = response.xpath(
            "//div[@class='grid-col span-md-6 span-lg-4']/table/tbody/tr/td/span/a/text()").extract()

        pok_HA = response.xpath(
            "//div[@class='grid-col span-md-6 span-lg-4']/table/tbody/tr/td/small/a/text()").extract()

        pok_forms = response.xpath(
            "//div[@class='tabset-basics tabs-wrapper ']/div/a/text()").extract()

        pok_basestat = response.xpath(
            "//div[@class='resp-scroll']/table[@class='vitals-table']/tbody/tr/td[@class='cell-num'][1]/text()").extract()

        pok_basestat1 = response.xpath(
            "//div[@class='resp-scroll']/table[@class='vitals-table']/tbody/tr/td[@class='cell-num'][2]/text()").extract()

        pok_basestat2 = response.xpath(
            "//div[@class='resp-scroll']/table[@class='vitals-table']/tbody/tr/td[@class='cell-num'][3]/text()").extract()

        pok.name = response.xpath(
            "//main[@class='main-content grid-container']/h1/text()").extract_first()

        pok_weakness = response.xpath(
            "//table[@class='type-table type-table-pokedex']/tr[2]/td").extract()

        if len(pok_forms) > 1 and "Mega" not in pok_forms[1] and "Alolan" not in pok_forms[1] and "Galar" in pok_forms[1]:
            if len(pok_forms) == 2:
                if "Alolan" in pok_forms[1]:
                    self.getAAbility(pok, pok_abilities,
                                     pok_HA, len(pok_abilities) // 2, False)
                else:
                    self.getGAbility(pok, pok_abilities,
                                     pok_HA, len(pok_abilities) // 2, False)
            elif len(pok_forms) == 3:
                self.getAAbility(pok, pok_abilities,
                                 pok_HA, len(pok_abilities) // 3, True)
                self.getGAbility(pok, pok_abilities,
                                 pok_HA, 4, True)

        self.getNAbility(pok, pok_abilities, pok_HA)

        pok.type1 = pok_types[0]
        if len(pok_types) > 1:
            pok.type2 = pok_types[1]

        pok.species = pok_data[3]
        pok.height = pok_data[4]
        pok.weight = pok_data[5]

        weakness = list(map(remove_tags, pok_weakness))

        scrapped_info = {
            'name': pok.name,
            'type1': pok.type1,
            'type2': pok.type2,
            'species': pok.species,
            'height': pok.height,
            'weight': pok.weight,
            'location': pok.location,
            'SW Desc': pok.SWDesc,
            'SH Desc': pok.SHDesc,
            'ability1': pok.ability1,
            'ability2': pok.ability2,
            'hiddenAbility': pok.hiddenAbility,
            'Galar Ability 1': pok.Gability1,
            'Galar Ability 2': pok.Gability2,
            'Galar Hidden Ability': pok.GhiddenAbility,
            'Alola Ability 1': pok.Aability1,
            'Alola Ability 2': pok.Aability2,
            'Alola Hidden Ability': pok.AhiddenAbility,
            'HP': pok_basestat[0],
            'Attack': pok_basestat[1],
            'Defense': pok_basestat[2],
            'Special Attack': pok_basestat[3],
            'Special Defense': pok_basestat[4],
            'Speed': pok_basestat[5],
            'HP Min': pok_basestat1[0],
            'Attack Min': pok_basestat1[1],
            'Defense Min': pok_basestat1[2],
            'Special Attack Min': pok_basestat1[3],
            'Special Defense Min': pok_basestat1[4],
            'Speed Min': pok_basestat1[5],
            'HP Max': pok_basestat2[0],
            'Attack Max': pok_basestat2[1],
            'Defense Max': pok_basestat2[2],
            'Special Attack Max': pok_basestat2[3],
            'Special Defense Max': pok_basestat2[4],
            'Speed Max': pok_basestat2[5],
            'Normal Weakness': weakness[0],
            'Fire Weakness': weakness[1],
            'Water Weakness': weakness[2],
            'Electric Weakness': weakness[3],
            'Grass Weakness': weakness[4],
            'Ice Weakness': weakness[5],
            'Fighting Weakness': weakness[6],
            'Poison Weakness': weakness[7],
            'Ground Weakness': weakness[8],
            'Flying Weakness': weakness[9],
            'Psychic Weakness': weakness[10],
            'Bug Weakness': weakness[11],
            'Rock Weakness': weakness[12],
            'Ghost Weakness': weakness[13],
            'Dragon Weakness': weakness[14],
            'Dark Weakness': weakness[15],
            'Steel Weakness': weakness[16],
            'Fairy Weakness': weakness[17],
        }

        yield scrapped_info

        next_page = response.xpath(
            "//a[@class='entity-nav-next']/@href").extract_first()

        if next_page:
            yield scrapy.Request(
                response.urljoin("https://pokemondb.net" + next_page),
                callback=self.parse)

        print(next_page)


'''
//a[@name = 'standardlevel']/../../../../..

    '''
