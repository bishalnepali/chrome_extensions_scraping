'''
Importing extensions.json
'''

import requests
import json

extensions_url = 'https://raw.githubusercontent.com/DebugBear/chrome-extension-list/master/extensions.json'

res = requests.get(extensions_url)
JSON_FILE = './input_file/extensions.json'

json.dump(res.json(),open(JSON_FILE,'w'),ensure_ascii=True, indent=2)
