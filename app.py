'''
Scraping the scraping extensions of the chrome
'''

import requests
import json
import random
from lxml import html
import datetime
import re
from multiprocessing import Pool
import logging


logging.basicConfig(level=logging.DEBUG, filename='chrome_extentions_scraping.log',
format='%(asctime)s %(levelname)s:%(message)s')

USER_AGENT_LIST = '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9
Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4
Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240
Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko
Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/8.0.7 Safari/600.7.12
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36
Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/7.1.8 Safari/537.85.17
Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4
Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F69 Safari/600.1.4'''

def get_response(url):
    headers = {'User-Agent':random.choice(USER_AGENT_LIST.split())}
    try:
        res = requests.get(url,headers=headers)
    except Exception as e:
        logging.debug("Raised and error while requesting %s of url",url)
        res = None
    if res:
        if res.status_code == 200:
            return res
        else:
            return None
def scrape_extension(extension_):
    '''It Scrapes all the extensions
    '''
    url = extension_['url']
    print('Scraping::',url)
    logging.debug("this file has %s words", url)
    res = get_response(url)
    extenstion_details = {}

    if res:
        page = html.fromstring(res.content.decode('utf-8'))
        try:
            name = page.xpath("//h1/text()")[0].strip()
        except:
            name = None
        try:
            website = page.xpath('//a[@class="e-f-y"]/@href')[0].strip()
        except:
            website = None
        try:
            offered_by = page.xpath('//a[@class="e-f-y"]/text()')[0].strip()

        except:
            offered_by = None

        try:
            img_url = page.xpath('//img/@src')[0].strip()
        except:
            img_url = None
        try:
            rating_sentence = page.xpath('//span[contains(@aria-label,"rating")]/@aria-label')[0].strip()
        except:
            rating_sentence = 'Not Found the rating'
        ratings, rating_count = parse_ratings_sentence(rating_sentence)
       
        try:
            users = page.xpath(
                '//span[@class="e-f-ih"]/text()')[0].replace('users', '').strip()
        except:
            users = None

        # updated_date = page.xpath('//span[@class="C-b-p-D-Xe h-C-b-p-D-xh-hh"]/text()')
        # size = page.xpath('//span[@class="C-b-p-D-Xe h-C-b-p-D-za"]/text()')
        try:
            update_date = page.xpath(
                '//span[text()="Updated:"]/following-sibling::span/text()')[0].strip()
        except:
            update_date = None
        try:
            size = page.xpath(
                '//span[text()="Size:"]/following-sibling::span/text()')[0].strip()
        except:
            size = None
        try:
            languages = page.xpath(
                '//span[text()="Languages:"]/following-sibling::span/text()')[0].replace('See all', '')
        except:
            languages = None
        try:
            developer_address = page.xpath(
                '//div[text()="Developer"]/following-sibling::div/a/@href')[0].strip()
        except:
            developer_address = None
        if developer_address:
            if developer_address.startswith('mailto:'):
                developer_address = developer_address.replace('mailto:', '')

        description = page.xpath(
            '//div[@itemprop="description"]/following-sibling::pre/text()')
        description = ' '.join(description)
        details = {
            'name':name,
            'website':website,
            'offered_by':offered_by,
            'image_url':img_url,
            'ratings':ratings,
            'users':users,
            'rating_count':rating_count,
            'update_data':update_date,
            'size':size,
            'languages':languages,
            'developer_address':developer_address,
            'description':description,
            'updated_date':datetime.date.today().strftime('%Y-%m-%d')
        }
        extension_['details'] = details
        logging.debug("Done sraping %s",url)
        return extension_

    else:
        logging.debug("No details were found for %s", url)
def parse_ratings_sentence(text_file):
    '''This is for parsing the rating of this type of pattern
    ---Average rating 4.4 out of 5.  43,424 users rated this item.--
    '''
    rating_file = re.compile('rating (.*) out of')
    try:
        rating_number = rating_file.findall(text_file)[0]
    except:
        rating_number = None
    rating_users_c = re.compile('5.(.*) users')
    try:
        rating_users = rating_users_c.findall(text_file)[0]
    except:
        rating_users = None
    return rating_number, rating_users


def main(INPUT_FILE,start_end, end_place):
    '''
    '''
    list_of_url = read_json(INPUT_FILE)
    extenstion_details = []
    list_of_url = list_of_url[start_end:end_place]
    with Pool(15) as p:
        sed = p.map(scrape_extension,list_of_url)
        extenstion_details.append(sed)
    with open(f'sample_chrome_extension_2022_12_08-{start_end}-{end_place}.json','w') as swp:
        json.dump(extenstion_details,swp, indent=2, ensure_ascii=True)
def read_json(INPUT_FILE):
    '''Returns the list of extensions
    '''
    with open(INPUT_FILE) as fp:
        json_file = json.load(fp)

    return json_file

   
if __name__ == "__main__":
    print("Main file started!!!")
    INPUT_FILE = 'extensions_2021.json'
    main(INPUT_FILE,100000,1000000)