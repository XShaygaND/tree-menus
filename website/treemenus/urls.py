from django.urls import path, re_path

from .views import index, menu_view

urlpatterns = [
    path('', index, name='index'),
    re_path(r'^menu/.*/$', menu_view, name='menu'),
]
