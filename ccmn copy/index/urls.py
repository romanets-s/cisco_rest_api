from django.urls import path
from ccmn.index import views

urlpatterns = [
    path('', views.index, name='index'),
]
