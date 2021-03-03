'''
Scraping the scraping extensions of the chrome
'''

import requests
import json
import random

USER_AGENT_LIST = ''

INPUT_FILE = './input_file/extensions.json'

def get_response(url):
    headers = {'User-Agent':random.choice(USER_AGENT_LIST)}
    res = requests.get(url,headers=headers)
def main():
    '''
    '''
    print("Main file started!!!")
if __name__ == "__main__":
    main()