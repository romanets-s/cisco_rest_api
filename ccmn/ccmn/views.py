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
from django.shortcuts import redirect
import datetime

userName = 'RO'
password = 'just4reading'

class ciscoAPI(TemplateView):

    def __init__(self, user, password, url):
        self.__user = user
        self.__password = password
        self.__host = url
        self.__auth = HTTPBasicAuth(self.__user, self.__password)

    def request_get(self, url):
        response = requests.get(
            url=self.__host + url,
            auth=self.__auth,
            verify=False
        )
        if response.status_code == 200:
            try:
                return json.loads(response.content)
            except:
                return None
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
            dir_for_maps = 'ccmn/static'
            if not os.path.exists(dir_for_maps):
                os.makedirs(dir_for_maps)
            full_path = os.path.join(dir_for_maps, file_name + '.png')
            if os.path.exists(full_path):
                return 1
            with open(full_path, 'wb') as f:
                response.raw.decode_content = True
                copyfileobj(response.raw, f)
            return 1
        else:
            return -1


client = ciscoAPI(userName, password, 'https://cisco-cmx.unit.ua')
client2 = ciscoAPI(userName, 'Passw0rd', 'https://cisco-presence.unit.ua')
current_floor = ''
floors = []
xlogin = ''
now = datetime.datetime.now()
date_from = now.strftime("%Y-%m-%d")
date_to = now.strftime("%Y-%m-%d")

def statistics(request):
    if request.method == 'GET' and request.GET and not 'from' in request.GET:
        global current_floor, xlogin
        if 'floor' in request.GET:
            current_floor = request.GET['floor']
        elif 'xlogin' in request.GET:
            xlogin = request.GET['xlogin']
        return redirect('index')
    global client, client2, date_to, date_from
    connected = client.request_get('/api/analytics/v1/now/connectedDetected')
    total_all = connected['total']['totalAll']
    if request.method == 'GET' and request.GET:
        date_from = datetime.datetime.strptime(request.GET['from'], "%m/%d/%Y").strftime("%Y-%m-%d")
        date_to = datetime.datetime.strptime(request.GET['to'], "%m/%d/%Y").strftime("%Y-%m-%d")

    siteId = client2.request_get('/api/config/v1/sites')[0]['aesUidString']
    repeat_vis = client2.request_get('/api/presence/v1/repeatvisitors/count?siteId=' + siteId + '&startDate=' + date_from + '&endDate=' + date_to)
    dwell = client2.request_get('/api/presence/v1/dwell/count?siteId=' + siteId + '&startDate=' + date_from + '&endDate=' + date_to)
    correlation = client2.request_get('/api/presence/v1/connected/daily?siteId=' + siteId + '&startDate=2017-12-22&endDate=' + datetime.datetime.now().strftime("%Y-%m-%d"))
    cor_list_val = []
    cor_list_key = []
    for cor in correlation:
        cor_list_key.append(str(cor))
        cor_list_val.append(correlation[cor])
    print(siteId)
    return render(request, 'statistics.html', {'all': total_all,
                                               'repeat': repeat_vis,
                                               'dwell': dwell,
                                               'cor_val': list(cor_list_val),
                                               'cor_key': list(cor_list_key),
                                               })

def index(request):
    global current_floor, client, floors, xlogin
    search_form = ''
    if request.method == 'GET' and request.GET:
        if 'floor' in request.GET:
            current_floor = request.GET['floor']
        elif 'xlogin' in request.GET:
            print(xlogin)
            xlogin = request.GET['xlogin']
        return redirect('index')
    connected = client.request_get('/api/analytics/v1/now/connectedDetected')
    total_con = connected['total']['totalConnected']
    total_det = connected['total']['totalDetected']
    total_all = connected['total']['totalAll']

    campus_map = client.request_get('/api/config/v1/maps/count')
    for campus in campus_map['campusCounts']:
        for build in campus['buildingCounts']:
            for floor in build['floorCounts']:
                floors.append(floor['floorName'])
                if not current_floor:
                    current_floor = floor['floorName']
                client.request_file('/api/config/v1/maps/image/' + campus['campusName'] + '/' + build['buildingName'] + '/' + floor['floorName'], floor['floorName'])
    users = client.request_get('/api/location/v2/clients')
    users_data = []
    for user in users:
        if user['macAddress'] and user['mapCoordinate']:
            users_data.append({'macAddress': user['macAddress'],
                               'x': user['mapCoordinate']['x'],
                               'y': user['mapCoordinate']['y'],
                               'userName': user['userName'],
                               'manufacturer': user['manufacturer'],
                               'floor': user['mapInfo']['mapHierarchyString'],
                               })
            if xlogin:
                search_form = 'not found'
                if xlogin.lower() == user['userName'].lower() or xlogin.lower() == user['macAddress'].lower():
                    for floor in floors:
                        if floor in user['mapInfo']['mapHierarchyString']:
                            current_floor = floor
                    search_form = user['macAddress']
    xlogin = ''
    return render(request, 'index.html', {'all': total_all,
                                          'users': users_data,
                                          'current_floor': current_floor,
                                          'search_form': search_form,
                                          })
