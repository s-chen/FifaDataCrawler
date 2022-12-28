import scrapy
import json
import logging
from scrapy.utils.log import configure_logging 

class FifaPlayerStatsSpider(scrapy.Spider):
    name = "fifa_player_stats"

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='data/log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.ERROR
    )

    def __init__(self):
            f = open('./data/fifa_player_urls_dev.json')
            self.players = json.load(f)

    def start_requests(self):
        for player in self.players:
            url = 'https://sofifa.com' + player['playerUrl']
            yield scrapy.Request(url=url, callback=self.parse)

    
    #def get_player_name():
    #    return short_name, full_name

    def parse(self, response):
        
        content = response.css('div.info')

        player_id = response.css('a.bp3-tab::attr(href)')[0].get().split('/')[2]
        player_nationality = response.css('div.info > div > a::attr(title)').get()
        player_full_name = content[0].css('h1::text').get()
        player_short_name = response.css('meta::attr(content)')[2].get().split('(')[0].strip()
        player_position = response.css('div.card > ul.ellipsis.pl > li:nth-child(2) > span::text').get() #response.css('div.meta.ellipsis > span::text').getall()

        player_bio = response.css('div.meta.ellipsis').get().split('y.o.')
        player_age = player_bio[0][-2:]
        player_dob_month = player_bio[1].split(' ')[1].replace('(', '')
        player_dob_day = player_bio[1].split(' ')[2].replace(',', '')
        player_dob_year = player_bio[1].split(' ')[3].replace(')', '')
        player_height = player_bio[1].split(' ')[4].replace('cm', '')
        player_weight = player_bio[1].split(' ')[5].split('</div>')[0].replace('kg', '')

        player_overall_rating = response.css('div.block-quarter')[0].css('span::text').get()
        player_potential_rating = response.css('div.block-quarter')[1].css('span::text').get()
        player_value = response.css('div.block-quarter')[2].css('div::text').get()
        player_wage = response.css('div.block-quarter')[3].css('div::text').get()

        player_preferred_foot = response.css('div.card > ul.pl > li::text')[0].get()
        player_weak_foot = response.css('div.card > ul.pl > li::text')[1].get().strip()
        player_skill_moves = response.css('div.card > ul.pl > li').css('::text')[5].get().strip()
        player_international_reputation = response.css('div.card > ul.pl > li').css('::text')[8].get().strip()
        player_attacking_work_rate = response.css('div.card > ul.pl > li').css('::text')[12].get().split('/')[0].strip()
        player_defensive_work_rate = response.css('div.card > ul.pl > li').css('::text')[12].get().split('/')[1].strip()
        player_body_type = response.css('div.card > ul.pl > li').css('::text')[14].get()
        player_real_face = response.css('div.card > ul.pl > li').css('::text')[16].get()
        player_release_clause = response.css('div.card > ul.pl > li').css('::text')[18].get()
        club = response.css('div.card > h5 > a::text').get().strip()
        kit_number = response.css('div.card > ul.ellipsis.pl > li:nth-child(3)::text').get()

        player_profile = {
            'preferredFoot': player_preferred_foot,
            'weakFoot': player_weak_foot,
            'skillMoves': player_skill_moves,
            'internationalReputation': player_international_reputation,
            'attackWorkRate': player_attacking_work_rate,
            'defenseWorkRate': player_defensive_work_rate,
            'bodyType': player_body_type,
            'realFace': player_real_face,
            'releaseClause': player_release_clause,
            'club': club,
            'kitNumber': kit_number
        }

        player_info_dictionary = {
            'id': player_id,
            'nationality': player_nationality,
            'name': player_short_name,
            'fullName': player_full_name,
            'positions': player_position,
            'dateOfBirth': player_dob_day + ' ' + player_dob_month + ' ' + player_dob_year,
            'height': player_height,
            'weight': player_weight,
            'overallRating': player_overall_rating,
            'potential': player_potential_rating,
            'value': player_value,
            'wage': player_wage,
            'profile': player_profile
        }

        yield player_info_dictionary