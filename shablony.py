import base64
from pprint import pprint

import requests
import urllib3
import environ
from requests import Response

from base_things import Extensions, BaseMy

env = environ.Env()
environ.Env.read_env('.env')
TOKEN = env('TOKEN')
PROS = env('PROS')


class Templates(BaseMy):
    def __init__(self, username: str, token: str, sub_id: str, host: str):
        super().__init__(username, token, sub_id, host)

    def _get_root_folder(self):
        headers, sub_id = self._config()
        response = requests.get(f'{self._host}/api/rp/v1/Templates/Root?subscriptionId={PROS}', headers=headers).json()
        return response

    def get_folder(self, name: str):
        headers, sub_id = self._config()
        root = self._get_root_folder()
        print(root.get('id'))
        folder_and_files = requests.get(f'{self._host}/api/rp/v1/Templates/Folder/{root.get("id")}/ListFolderAndFiles',
                                        headers=headers).json()

        return [i for i in folder_and_files.get('files') if i.get('name') == name][0]

    def _get_list_folders(self, name: str = 'root'):
        headers, sub_id = self._config()
        folder = self._get_root_folder() if name == 'root' else self.get_folder(name)
        list_folder = requests.get(f'{self._host}/api/rp/v1/Templates/Folder/{folder.get("id")}/ListFolders',
                                   headers=headers).json()
        return (list_folder.get('files'))

    def _get_list_files_folder(self, name: str = 'root'):
        headers, sub_id = self._config()
        folder = self._get_root_folder() if name == 'root' else self.get_folder(name)
        list_folder = requests.get(f'{self._host}/api/rp/v1/Templates/Folder/{folder.get("id")}/ListFolderAndFiles',
                                   headers=headers).json()
        return list_folder.get('files')

    def create_folder(self, parent_name: str = 'root', folder_name: str = None):
        headers, sub_id = self._config()
        folder = self._get_root_folder() if parent_name == 'root' else self.get_folder(parent_name)
        json_folder = {
            "name": folder_name,
            "tags": [
                'null'
            ],
            "icon": 'null'
        }
        new_folder = requests.post(f'{self._host}/api/rp/v1/Templates/Folder/{folder.get("id")}/Folder',
                                   headers=headers, json=json_folder).json()
        return new_folder

    def delete_folder(self, name: str):
        headers, sub_id = self._config()
        folder = self.get_folder(name)
        del_folder = requests.delete(f'{self._host}/api/rp/v1/Templates/Folder/{folder.get("id")}/ToBin',
                                     headers=headers)
        return del_folder

    def delete_file(self, name: str) -> Response:
        headers, sub_id = self._config()
        file = self._get_file_by_name(name)
        print(file)
        del_folder = requests.delete(f'{self._host}/api/rp/v1/Templates/File/{file.get("id")}/ToBin',
                                     headers=headers)
        return del_folder

    def create_file(self, file_name: str, folder_name: str = 'root', content='null'):
        headers, sub_id = self._config()
        folder = self._get_root_folder() if folder_name == 'root' else self.get_folder(folder_name)
        json = {
            "name": file_name,
            'content': content
        }
        file = requests.post(f'{self._host}/api/rp/v1/Templates/Folder/{folder.get("id")}/File', headers=headers,
                             json=json)

        return file.json()

    def _get_file_by_name(self, name: str, folder_name: str = 'root'):
        headers, sub_id = self._config()
        folder = self._get_root_folder() if folder_name == 'root' else self.get_folder(folder_name)
        response = requests.get(f'{self._host}/api/rp/v1/Templates/Folder/{folder.get("id")}/ListFiles?take=100',
                                headers=headers).json()
        return [i for i in response.get('files') if i.get('name') == f'{name}.frx'][0]

    def prepare_file(self, file_name: str, folder_name: str = 'root', file_prepare_name: str = None):
        headers, sub_id = self._config()
        file = self._get_file_by_name(file_name, folder_name)
        json = {
            "name": file_prepare_name,
            "pagesCount": 2147483647
        }
        lol = requests.post(f'{self._host}/api/rp/v1/Templates/File/{file.get("id")}/Prepare', headers=headers,
                            json=json)
        print(lol.json())

    def _get_root_reports_dir(self):
        headers, sub_id = self._config()
        response = requests.get(f'{self._host}/api/rp/v1/Reports/Root', headers=headers)
        return response.json()

    def _get_files_list_rep(self, folder_name: str = 'root'):
        headers, sub_id = self._config()
        folder = self._get_root_reports_dir() if folder_name == 'root' else self.get_folder(folder_name)
        response = requests.get(f'{self._host}/api/rp/v1/Reports/Folder/6377865f5f620ebfce9a07cc/ListFiles?take=100',
                                headers=headers)
        return response.json()

    def _get_file_rep(self, name: str, folder_name: str = 'root'):
        headers, sub_id = self._config()
        files = self._get_files_list_rep(folder_name=folder_name)
        file = [i for i in files.get('files') if i.get("name") == f'{name}.fpx'][0]
        response = requests.get(f'{self._host}/api/rp/v1/Reports/File/{file.get("id")}', headers=headers)
        return response.json()

    def export_file(self, file_name: str, format: str, folder_name: str = 'root', export_name: str = None):
        headers, sub_id = self._config()
        json = {
            "fileName": export_name,
            "pagesCount": 2147483647,
            "format": format
        }
        fileq = self._get_file_rep(file_name, folder_name=folder_name)
        file = requests.post(f'{self._host}/api/rp/v1/Templates/File/{fileq.get("templateId")}/Export', headers=headers,
                             json=json)
        return file.json()

    def download_file(self, file_name: str):
        headers, sub_id = self._config()
        root_id = requests.get(f'{self._host}/api/rp/v1/Exports/Root', headers=headers).json().get('id')
        files = requests.get(f'{self._host}/api/rp/v1/Exports/Folder/{root_id}/ListFiles?take=100', headers=headers).json()
        f = file_name.split('.')[0]
        # print(f)
        file = [i for i in files.get('files') if i.get('name').split('.')[0] == f'{f}'][0]
        response = requests.get(f'{self._host}/download/e/{file.get("id")}', headers=headers)
        wer = requests.get(response.url, headers=headers)

        with open(f'{file_name}', 'wb') as f:
            f.write(wer.content)


# b = Templates('apikey', TOKEN, PROS, 'https://fastreport.cloud')

# with open('lol.frx', 'rb') as f:
#     temp = base64.b64encode(f.read()).decode('utf-8')
#     print(temp)

# print(b.create_file('bely_paren_v_belom_platye_vyglyazhu_kak_sheykh', content=temp))
# print(b._get_root_folder())
# b.create_folder(folder_name='qwerty')
# print(b.get_folder('qwerty'))
# 6378a7125f620ebfce9a1ffa
# pprint(b.delete_folder('qwerty'))
# import base64
# with open('lol.fpx', 'r') as xml:
#     content = base64.b64encode(xml.read().encode('utf-8'))
#     print(content)
# b.create_file(file_name='lol123')
# b.prepare_file(file_name='lol123', file_prepare_name='lol123')
# id = b._get_file_by_name('bely_paren_v_belom_platye_vyglyazhu_kak_sheykh').get('id')
# print(b._get_file_by_name('bely_paren_v_belom_platye_vyglyazhu_kak_sheykh').get('id'))


# print(b._get_files_list())#6378a7fa5f620ebfce9a2037
# print(b.export_file('lol123.fpx', format='pdf'))
# print(b.prepare_file(file_name='bely_paren_v_belom_platye_vyglyazhu_kak_sheykh',
#                      file_prepare_name='bely_paren_v_belom_platye_vyglyazhu_kak_sheykh'))
# print(b._get_file_rep('lol123'))
# print(b.export_file('bely_paren_v_belom_platye_vyglyazhu_kak_sheykh', format=Extensions.pdf))
# print(b.download_file('lol123.pdf'))
# print(b.delete_file('Frog'))
# print()
