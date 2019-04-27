from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests
requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth
import json
import base64
from django.views.generic import TemplateView
#from .models import Users2
from shutil import copyfileobj
import os

user = 'RO'
password = 'just4reading'

class ciscoAPI(TemplateView):

    def __init__(self, user, password):
        self.__user = user
        self.__password = password
        self.__host = 'https://cisco-cmx.unit.ua'
        self.__auth = HTTPBasicAuth(self.__user, self.__password)

    def request_get(self, url):
        response = requests.get(
            url=self.__host + url,
            auth=self.__auth,
            verify=False
        )
        if response.status_code == 200:
            return json.loads(response.content)
        print(response.status_code, url)
        return None

    def request_file(self, url, file_name):
        response = requests.get(
            url=self.__host + url,
            auth=self.__auth,
            verify=False,
            stream=True
        )
        if response.status_code == 200:
            if not os.path.exists('maps'):
                os.makedirs('maps')
            full_path = os.path.join('maps', file_name + '.png')
            if os.path.exists(full_path):
                return 1
            with open(full_path, 'wb') as f:
                response.raw.decode_content = True
                copyfileobj(response.raw, f)
            return 1
        else:
            return -1


def index(request):
    client = ciscoAPI(user, password)

    print("____________________________________________")
    print("con: ", client.request_get('/api/analytics/v1/now/connectedDetected')['total']['totalConnected'])
    print("det: ", client.request_get('/api/analytics/v1/now/connectedDetected')['total']['totalDetected'])
    print("all: ", client.request_get('/api/analytics/v1/now/connectedDetected')['total']['totalAll'])
    print("____________________________________________")

    campus_map = client.request_get('/api/config/v1/maps/count')
    for campus in campus_map['campusCounts']:
        print(campus['campusName'])
        for build in campus['buildingCounts']:
            print(build['buildingName'])
            for floor in build['floorCounts']:
                print(floor['floorName'])
                client.request_file('/api/config/v1/maps/image/' + campus['campusName'] + '/' + build['buildingName'] + '/' + floor['floorName'], floor['floorName'])


    print(client.request_get('/api/location/v1/history/clients/'))

    print("____________________________________________")

    print("____________________________________________")

    print("____________________________________________")

    print("____________________________________________")

    return HttpResponse("test")
    #template = loader.get_template('index.html')
    #context = {
    #    'test': 't42'
    #}
    #return HttpResponse(template.render(context, request))