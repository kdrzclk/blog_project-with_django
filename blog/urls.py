from django.urls import path
from .views import post_create, post_detail, post_list

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='list'),
    path('create/', post_create, name='create'),
    path('<str:slug>', post_detail, name='detail')
]