import requests
import urllib3
import environ
import base64
from pprint import pprint
from shablony import BaseMy, Templates

env = environ.Env()
environ.Env.read_env('.env')
TOKEN = env('TOKEN')
PROS = env('PROS')

b = Templates('apikey', TOKEN, PROS, 'https://fastreport.cloud')

headers, sub_id = b._config()

with open('lol.fpx', 'rb') as f:
    temp = base64.b64encode(f.read()).decode('utf-8')
    print(temp)


id = b._get_root_folder().get('id')
print(b.create_file('lolihunter', content=temp))
file = b.export_file('lolihunter', format='pdf', export_name='lolihunter')
# print(id)
