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


def update_me(name: str = None, username: str = None, email: str = None, password_new: str = None,
              password_new2: str = None):
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        # Create an instance of the API class
        api_instance = fastreport_cloud_sdk.UserProfileApi(api_client)
        update_user_profile_vm = fastreport_cloud_sdk.UpdateUserProfileVM(name, username,
                                                                          email, password_new,
                                                                          password_new2)  # UpdateUserProfileVM |  (optional)

        try:
            # Update profile of the current user
            api_instance.user_profile_update_my_profile(update_user_profile_vm=update_user_profile_vm)
            # print(api_instance.user_profile_get_my_profile())
        except ApiException as e:
            print("Exception when calling UserProfileApi->user_profile_update_my_profile: %s\n" % e)


def get_current_settings():
    with fastreport_cloud_sdk.ApiClient(_config_api(TOKEN)) as api_client:
        # Create an instance of the API class
        api_instance = fastreport_cloud_sdk.UserSettingsApi(api_client)
        try:
            # Return current user settings.
            api_response = api_instance.user_settings_get_current_user_settings()
            pprint(api_response)
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


# update_me('kirill', '0uts1der')

# update_profile_settings(show_hidden_files_and_folders=True)
