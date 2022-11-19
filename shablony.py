
import requests
import urllib3
import environ

env = environ.Env()
environ.Env.read_env('.env')
TOKEN = env('TOKEN')
PROS = env('PROS')


class Base:
    def __init__(self, username: str, token: str, sub_id: str, host: str):
        self._username = username
        self._token = token
        self._sub_id = sub_id
        self._host = host

    def _config(self):
        auth = urllib3.util.make_headers(
            basic_auth=self._username + ':' + self._token
        ).get('authorization')

        headers = {
            'accept': 'application/json',
            'Authorization': auth
        }
        return headers, self._sub_id


class Templates(Base):
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

    def create_file(self, file_name: str, folder_name: str = 'root'):
        headers, sub_id = self._config()
        folder = self._get_root_folder() if folder_name == 'root' else self.get_folder(folder_name)
        json = {
            "name": file_name
        }
        file = requests.post(f'{self._host}/api/rp/v1/Templates/Folder/{folder.get("id")}/File', headers=headers,
                             json=json)

        print(file.json())

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
        response = requests.get(f'{self._host}/api/rp/v1/Reports/Folder/6377865f5f620ebfce9a07cc/ListFiles',
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
        file = self._get_file_rep(file_name, folder_name=folder_name)
        # print(file_id)
        file = requests.post(f'{self._host}/api/rp/v1/Templates/File/{file.get("templateId")}/Export', headers=headers,
                             json=json)
        return file.json()

    def download_file(self, file_name: str):
        headers, sub_id = self._config()
        root_id = requests.get(f'{self._host}/api/rp/v1/Exports/Root', headers=headers).json().get('id')
        files = requests.get(f'{self._host}/api/rp/v1/Exports/Folder/{root_id}/ListFiles', headers=headers).json()
        file = [i for i in files.get('files') if i.get('name') == file_name][0]
        response = requests.get(f'{self._host}/download/e/{file.get("id")}', headers=headers)
        wer = requests.get(response.url, headers=headers)
        print(wer.content)

        with open(f'{file_name}', 'wb') as f:
            f.write(wer.content)


b = Templates('apikey', TOKEN, PROS, 'https://fastreport.cloud')
# print(b.create_file('loli_hentai'))
# print(b._get_root_folder())
# b.create_folder(folder_name='qwerty')
# print(b.get_folder('qwerty'))
# 6378a7125f620ebfce9a1ffa
# pprint(b.delete_folder('qwerty'))
# import base64
# with open('lolka_s_chlenom-femboy.frx', 'r') as xml:
#     content = base64.b64encode(xml.read().encode('utf-8'))
#     print(content)
# b.create_file(file_name='lol123')
# b.prepare_file(file_name='lol123', file_prepare_name='lol123')
# print(b._get_file_by_name('loli_hentai'))
# print(b._get_files_list())#6378a7fa5f620ebfce9a2037
# print(b.export_file('lol123.fpx', format='pdf'))
# print(b.prepare_file(file_name='lol123', file_prepare_name='lol123'))
# print(b._get_file_rep('lol123'))
# print(b.export_file('lol123', format='pdf'))
# print(b.download_file('lol123.pdf'))