# -*- coding: utf-8 -*-
import base64

import fastreport_cloud_sdk
from requests import get, post, delete, put
import urllib3
import environ
from base_things import Extensions

env = environ.Env()
environ.Env.read_env('.env')
TOKEN = env('TOKEN')
PROS = env('PROS')


class Base:
    def __init__(self, username, token, sub_id):
        self._username = username
        self._token = token
        self._sub_id = sub_id

    def _config(self):
        auth = urllib3.util.make_headers(
            basic_auth=self._username + ':' + self._token
        ).get('authorization')

        headers = {
            'accept': 'application/json',
            'Authorization': auth,
            'Content-Type': 'application/json-patch+json'
        }
        return headers, f'?subscriptionId={self._sub_id}'


class Reports(Base):
    def __init__(self, username, token, sub_id):
        super().__init__(username, token, sub_id)
        self.headers, self.sub_id = self._config()
        self.domen = 'https://fastreport.cloud'

    def get_root_dir(self):
        response = get(f'{self.domen}/api/rp/v1/Reports/Root{self.sub_id}', headers=self.headers)
        return response.json()['id']

    def delite_file(self, id_file):
        response = delete(f'{self.domen}/api/rp/v1/Reports/File/{id_file}{self.sub_id}', headers=self.headers)
        return response.status_code

    def delite_folder(self, id_folder):
        response = delete(f'{self.domen}/api/rp/v1/Reports/Folder/{id_folder}{self.sub_id}', headers=self.headers)
        return response.status_code

    def get_all_file_and_folder(self, id_file):
        response = get(f'{self.domen}/api/rp/v1/Reports/Folder/{id_file}/ListFolderAndFiles{self.sub_id}',
                       headers=self.headers)
        return response.json()['files']

    def create_file(self, file_name: str, content='null'):
        headers, sub_id = self._config()
        folder = self.get_root_dir()
        json = {
            "name": file_name,
            "content": content
        }
        file = post(f'{self.domen}/api/rp/v1/Reports/Folder/{folder}/File', headers=headers,
                             json=json)

        return file.json()

    def get_file(self, id_file):
        response = get(f'{self.domen}/api/rp/v1/Reports/File/{id_file}{self.sub_id}', headers=self.headers)
        return response.json()

    def download_file(self, id_file):
        name = self.get_file(id_file)["name"]
        response = get(f'{self.domen}/download/r/{id_file}{self.sub_id}', headers=self.headers)
        with open(f'{name}', 'wb') as f:
            f.write(response.content)
        return name

    def export_file(self, id_file: str, format: str, export_name: str = None):
        json = {
            "fileName": export_name,
            "pagesCount": 2147483647,
            "format": format
        }
        # file = self._get_file_rep(file_name, folder_name=folder_name)
        # print(file_id)
        file = post(f'{self.domen}/api/rp/v1/Reports/File/{id_file}/Export', headers=self.headers,
                    json=json)
        return self.domen + '/download/e/' + file.json()['id']


rep = Reports('apikey', TOKEN, PROS)
id_root = rep.get_root_dir()
# print(rep.export_file('6378b6725f620ebfce9a212d', format=Extensions.docx))
print(id_root)
with open('file.fpx', 'rb') as f:
    temp = base64.b64encode(f.read()).decode('utf-8')
    print(temp)
# print(type(str(Extensions.pdf)))
# print(rep.download_file('6378f9215f620ebfce9a297f'))
print(rep.create_file('lol123', temp))
# print(rep.delite_file('637811b05f620ebfce9a10c8'))
#