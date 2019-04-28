from django.http import HttpResponse
import os
from django.shortcuts import render
import requests
from .model.Player import *
from .model.Film import *
from .model.Python import *
import random

variables = {
'x':3,
'y':7,
'length':10,
'width':10,
'films':[
'tt7784604',
'tt1502407',
'tt0460681',
'tt3743822',
'tt5814060',
'tt1520211',
'tt6499752',
'tt6644200',
'tt2798920',
'tt4574334'
]
}

films = []

player = Player(0, 0, 0)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

def menu(request):
    fill_films_array()
    return render(request, 'menu.html', {})

def battle(request, id):
    monster = ''
    count = 0
    for i in films:
        if i.id == id:
            player.enemy = i
            monster = i
            count += 1
    if request.method == "GET" and request.GET:
        if player.boll > 0:
            player.boll -= 1
            try:
                res = 5 - (float(monster.imdbRating) * 10) + (player.power * 5)
            except:
                res = 5 - (1 * 10) + (player.power * 5)
            if res < 0:
                res = 1
            if res > 90:
                res = 90
            print ('fff')
            if random.randint(res, 100) > 75:
                print('win')
                films[count].catch = True
                return render(request, 'options.html', {})
    return render(request, 'battle.html', {'dict': variables,
                                           'length': range(variables['length']),
                                           'width': range(variables['width']),
                                           'monster': monster,
                                           'player' : player
                                           })

def get_moviemon_by_id(id):
    r = requests.get('http://www.omdbapi.com/?apikey=83efbcfd&i=' + id)
    return Film(r.json(), id)


def fill_films_array():
    if not films:
        for film_id in variables['films']:
            films.append(get_moviemon_by_id(film_id))

def get_all_items_for_map(request):
    monster = ''
    width_td = round(520 / variables['width'])
    hight_td = round(520 / variables['length'])
    player.allMonsters = len(films)
    if request.method == 'GET' and request.GET:
        tmpX = variables['x']
        tmpY = variables['y']
        if request.GET['val'] == 'up':
            tmpX -= 1
        elif request.GET['val'] == 'down':
            tmpX += 1
        elif request.GET['val'] == 'right':
            tmpY += 1
        elif request.GET['val'] == 'left':
            tmpY -= 1
        if tmpX < 0:
            tmpX = 0
        if tmpX >= variables['length']:
            tmpX = variables['length'] - 1
        if tmpY < 0:
            tmpY = 0
        if tmpY >= variables['width']:
            tmpY = variables['width'] - 1
        variables['x'] = tmpX
        variables['y'] = tmpY
        if player.power != player.allMonsters:
            if player.lucky < player.allMonsters * 5:
                player.lucky += 5
            else:
                player.lucky = 5
            monsterHere = random.randint(player.lucky, 100)
            if monsterHere >= 75:
                monster = randomMonster(films)
            else:
                player.bollHere = 1 if random.randint(player.lucky, 100) >= 75 else 0
            player.boll += player.bollHere
            if monsterHere or player.bollHere:
                player.lucky = 10
    return render(request, 'worldmap.html', {'dict': variables,
                                           'length': range(variables['length']),
                                           'width': range(variables['width']),
                                           'width_td' : width_td,
                                           'hight_td' : hight_td,
                                           'monster': monster,
                                           'player' : player
                                           })



def randomMonster(monsters):
    monster = ''
    while not monster:
        n = random.randint(0, len(monsters) - 1)
        if not monsters[n].catch:
            monster = monsters[n]
        else:
            monsters.remove(monsters[n])
    return monster

def render_inventory(request):
    return render(request, 'inventory.html', {'array': films})


def get_film_by_name(name):
    for film in films:
        if film.title == name:
            return film


def get_film_by_id(request, id):
    for film in films:
        if film.id == id:
            return render(request, 'film_info.html', {'film': film})


def render_options(request):
    return render(request, 'options.html', {'variables': variables})


def render_save(request):
    return render(request, 'save.html')


def render_load(request):
    return render(request, 'load.html')
