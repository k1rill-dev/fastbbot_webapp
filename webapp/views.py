from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse(content='<h1>Lolkek</h1>')


def docs(request):
    ...


def temp(request):
    ...


def reports(request):
    ...


def data(request):
    ...


def groups(request):
    ...


def users(request):
    ...


def api_keys(request):
    ...
