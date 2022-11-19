import environ
from shablony import Base

env = environ.Env()
environ.Env.read_env('.env')
TOKEN = env('TOKEN')
PROS = env('PROS')

class DataSources(Base):
    def __init__(self, username: str, token: str, sub_id: str, host: str):
        super().__init__(username, token, sub_id, host)





b = DataSources('apikey', TOKEN, PROS, 'https://fastreport.cloud')