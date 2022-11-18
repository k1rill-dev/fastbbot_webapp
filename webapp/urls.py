from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('docs/', docs, name='docs'),
    path('shablon/', temp, name='temp'),
    path('reports/', reports, name='reports'),
    path('data/', data, name='data'),
    path('groups/', groups, name='groups'),
    path('users/', users, name='users'),
    path('api-keys/', api_keys, name='api-keys'),

]