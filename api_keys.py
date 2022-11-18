import datetime
import time

import fastreport_cloud_sdk
from fastreport_cloud_sdk.rest import ApiException
from pprint import pprint
import environ

env = environ.Env()
environ.Env.read_env('.env')
TOKEN = env('TOKEN')
PROS = env('PROS')


def _config_api(token: str) -> fastreport_cloud_sdk.configuration.Configuration:
    configuration = fastreport_cloud_sdk.Configuration(
        host="https://fastreport.cloud",
        username='apikey',
        password=token,
    )
    return configuration


def get_subscription() -> fastreport_cloud_sdk.models.subscription_vm.SubscriptionVM:
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        a = fastreport_cloud_sdk.SubscriptionsApi(api_client)
        try:
            return a.subscriptions_get_subscription(id=PROS)
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_create_group: %s\n" % e)

def get_api_keys():
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.ApiKeysApi(api_client)

        try:
            api_response = api_instance.api_keys_get_api_keys()
            # pprint(api_response)
            return api_response.api_keys
        except ApiException as e:
            print("Exception when calling ApiKeysApi->api_keys_get_api_keys: %s\n" % e)

def create_api_key(description:str=None, expired:datetime.date=None):
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.ApiKeysApi(api_client)
        create_api_key_vm = fastreport_cloud_sdk.CreateApiKeyVM(description, expired)

        try:
            api_response = api_instance.api_keys_create_api_key(create_api_key_vm)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling ApiKeysApi->api_keys_create_api_key: %s\n" % e)

print(get_api_keys())
date_time_str = '20/11/22'

date = datetime.datetime.strptime(date_time_str, '%d/%m/%y')
# print(date)
# create_api_key('test', date)