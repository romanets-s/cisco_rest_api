"""moviemon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('moviedex/', render_inventory),
    path('moviedex/<id>', get_film_by_id),
    path('', menu, name='index'),
    path('film/<id>', get_moviemon_by_id, name='index5'),
    path('battle/<id>', battle),
    path('worldmap/', get_all_items_for_map, name='worldmap'),
    path('options/', render_options),
    path('options/save_game', render_save),
    path('options/load_game', render_load),
]
