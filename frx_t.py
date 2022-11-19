import environ
import base64
from pprint import pprint
from shablony import BaseMy, Templates
from base_things import Extensions

env = environ.Env()
environ.Env.read_env('.env')
TOKEN = env('TOKEN')
PROS = env('PROS')


def converter()
with open('lol.frx', 'rb') as f:
    temp = base64.b64encode(f.read()).decode('utf-8')
    # print(temp)


id = b._get_root_folder().get('id')
# print(id)
# print(b.create_file('zxc_ghoul_1000-7', content=temp))
# print(b.prepare_file('zxc_ghoul_1000-7', file_prepare_name='zxc_ghoul_1000-7'))
file = b.export_file(file_name='zxc_ghoul_1000-7', format=Extensions.docx)
# print(file)
b.download_file(file_name='zxc_ghoul_1000-7.docx')
# print(b.download_file('bely_paren_v_belom_platye_vyglyazhu_kak_sheykh'))
# print(id)
