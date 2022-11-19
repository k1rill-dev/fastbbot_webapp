from dataclasses import dataclass
from typing import NamedTuple
import urllib3

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