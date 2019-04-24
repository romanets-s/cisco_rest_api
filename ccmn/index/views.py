from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
#from .models import Users2
import requests
requests.packages.urllib3.disable_warnings()
from requests.auth import HTTPBasicAuth
import json
import base64
from django.views.generic import TemplateView

user = 'RO'
password = 'just4reading'

class ciscoAPI(TemplateView):

    def __init__(self, user, password):
        self.__user = user
        self.__password = password
        self.__host = 'https://cisco-cmx.unit.ua'
        self.__auth = HTTPBasicAuth(self.__user, self.__password)

    def request(self, url):
        response = requests.get(
            url=self.__host + url,
            auth=self.__auth,
            verify=False
        )
        return json.loads(response.content)



def index(request):
    client = ciscoAPI(user, password)

    print("____________________________________________")
    print(client.request('/api/location/v2/clients/count')["count"])
    print("____________________________________________")

    return HttpResponse("test")
    #template = loader.get_template('index.html')
    #context = {
    #    'test': 't42'
    #}
    #return HttpResponse(template.render(context, request))