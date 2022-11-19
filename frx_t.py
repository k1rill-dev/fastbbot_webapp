import environ
import base64
import requests
from dataclasses import dataclass
import urllib3

env = environ.Env()
environ.Env.read_env('.env')
TOKEN = env('TOKEN')
PROS = env('PROS')


@dataclass
class Extensions:
    fpx: str = 'fpx'
    pdf: str = 'pdf'
    xml: str = 'xml'
    html: str = 'html'
    docx: str = 'docx'
    pptx: str = 'pptx'
    xlsx: str = 'xlsx'
    rtf: str = 'rtf'
    odt: str = 'odt'
    ods: str = 'ods'
    odp: str = 'odp'
    png: str = 'png'
    jpg: str = 'jpg'
    jpeg: str = 'jpeg'
    svg: str = 'svg'


class BaseMy:
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
            'Authorization': auth,
            'Content-Type': 'application/json-patch+json'
        }
        return headers, f'?subscriptionId={self._sub_id}'
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

    def delete_file(self, name: str):
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


def converter(file: str, format: str):
    b = Templates('apikey', TOKEN, PROS, 'https://fastreport.cloud')
    with open(file, 'rb') as f:
        temp = base64.b64encode(f.read()).decode('utf-8')

    print(b.create_file('convert_file', content=temp))
    print(b.prepare_file('convert_file', file_prepare_name='convert_file'))
    b.export_file(file_name='convert_file', format=format)
    b.download_file(file_name=f'convert_file.{format}')

converter('lol.frx', Extensions.pdf)