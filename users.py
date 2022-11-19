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



def upd_current_user(name='null', username='null', email='null', pswd_new='null', pswd_new2='null'):
    b = BaseMy('apikey', TOKEN, PROS, 'https://fastreport.cloud')

    headers, sub_id = b._config()

    json = {
        "name": name,
        "username": username,

    }
    response = requests.put(f'{b._host}/api/manage/v1/UserProfile', headers=headers, json=json)
    print(response.json())


def get_my_profile():
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        # Create an instance of the API class
        api_instance = fastreport_cloud_sdk.UserProfileApi(api_client)

        try:
            # Return current profile of the current user
            api_response = api_instance.user_profile_get_my_profile()
            pprint(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling UserProfileApi->user_profile_get_my_profile: %s\n" % e)


def get_current_settings():
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        # Create an instance of the API class
        api_instance = fastreport_cloud_sdk.UserSettingsApi(api_client)
        try:
            # Return current user settings.
            api_response = api_instance.user_settings_get_current_user_settings()
            pprint(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling UserSettingsApi->user_settings_get_current_user_settings: %s\n" % e)


def update_profile_settings(profile_visibility: str = None, default_subscription: str = None,
                            show_hidden_files_and_folders: bool = None):
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        # Create an instance of the API class
        api_instance = fastreport_cloud_sdk.UserSettingsApi(api_client)
        update_user_settings_vm = fastreport_cloud_sdk.UpdateUserSettingsVM(profile_visibility, default_subscription,
                                                                            show_hidden_files_and_folders)
        try:
            # Return current user settings.
            api_response = api_instance.user_settings_update_my_settings(
                update_user_settings_vm=update_user_settings_vm)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling UserSettingsApi->user_settings_get_current_user_settings: %s\n" % e)

# get_my_profile()
# update_profile_settings(show_hidden_files_and_folders=True)
