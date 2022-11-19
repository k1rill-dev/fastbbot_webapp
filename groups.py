from __future__ import print_function
import shutil
import time
import fastreport_cloud_sdk
import requests
from fastreport_cloud_sdk.rest import ApiException
from pprint import pprint
import environ
from base_things import BaseMy


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


def create_group(name: str):
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.GroupsApi(api_client)
        create_group_vm = fastreport_cloud_sdk.CreateGroupVM(name=name, subscription_id=PROS)

        try:
            api_response = api_instance.groups_create_group(create_group_vm=create_group_vm)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_create_group: %s\n" % e)


def _get_group(name: str = None) -> str:
    """Возвращает id группы с именем name"""
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.GroupsApi(api_client)
        skip = 0
        take = 10

        try:
            api_response = api_instance.groups_get_group_list(skip=skip, take=take)
            id = [i.id for i in api_response.groups if i.name == name]
            # print(api_response)
            return id
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_get_group_list: %s\n" % e)

def delete_group(group_id):
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        api_instance = fastreport_cloud_sdk.GroupsApi(api_client)
        try:
            api_instance.groups_delete_group(group_id)
        except ApiException as e:
            print("Exception when calling GroupsApi->groups_delete_group: %s\n" % e)
def get_user_groups():
    b = BaseMy('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()

    response = requests.get(f'{b._host}/api/manage/v1/Groups?take=100', headers=headers)
    return response.json().get('groups')


def update_name_group(new_name, group_id):
    b = BaseMy('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()
    json = {
        'name': new_name
    }
    response = requests.put(f'{b._host}/api/manage/v1/Groups/{group_id}/rename', headers=headers, json=json)

    return response.json()


def all_users_in_current_group(group_id):
    b = BaseMy('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()
    response = requests.get(f'{b._host}/api/manage/v1/Groups/{group_id}/Users?take=100', headers=headers)

    print(response.json())

def add_user_to_group(user_id, group_id):
    b = BaseMy('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()
    response = requests.put(f'{b._host}/api/manage/v1/Groups/{group_id}/Users/{user_id}', headers=headers)

    print(response.status_code)

def remove_user_from_group(user_id, group_id):
    b = BaseMy('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()
    response = requests.delete(f'{b._host}/api/manage/v1/Groups/{group_id}/Users/{user_id}', headers=headers)

    print(response.status_code)

def leave_from_group(group_id):
    b = BaseMy('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()
    response = requests.delete(f'{b._host}/api/manage/v1/Groups/{group_id}/leave', headers=headers)

    print(response.status_code)


# all_users_in_current_group('6377abc85f620ebfce9a09e0')

# add_user_to_group('84e40176-296e-47cd-a4ae-7165056c0417', '6377abc85f620ebfce9a09e0')
# remove_user_from_group('84e40176-296e-47cd-a4ae-7165056c0417', '6377abc85f620ebfce9a09e0')
# leave_from_group('6377db505f620ebfce9a0c4a')
# create_group('tomas_shelby')
# id = _get_group('tomas_shelby')
# print(id)
# update_name_group(new_name='aboba', group_id='')
# delete_group('')