'''
Importing extensions.json
'''

import requests
import json

extensions_url = 'https://raw.githubusercontent.com/DebugBear/chrome-extension-list/master/extensions-2021.json'

res = requests.get(extensions_url)
JSON_FILE = 'extensions_2021.json'

json.dump(res.json(),open(JSON_FILE,'w'),ensure_ascii=True, indent=2)

