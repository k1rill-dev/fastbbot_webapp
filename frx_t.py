import requests
import urllib3
import environ
import base64
from pprint import pprint
from shablony import BaseMy, Templates
from base_things import Extensions

env = environ.Env()
environ.Env.read_env('.env')
TOKEN = env('TOKEN')
PROS = env('PROS')

b = Templates('apikey', TOKEN, PROS, 'https://fastreport.cloud')

headers, sub_id = b._config()

with open('lol.frx', 'rb') as f:
    temp = base64.b64encode(f.read()).decode('utf-8')
    # print(temp)


id = b._get_root_folder().get('id')
# print(id)
print(b.create_file('lol', content=temp))
print(b.prepare_file('lol', file_prepare_name='lol'))
file = b.export_file(file_name='lol', format=Extensions.svg)
print(file)
b.download_file(file_name='lol')
# print(b.download_file('bely_paren_v_belom_platye_vyglyazhu_kak_sheykh'))
# print(id)
