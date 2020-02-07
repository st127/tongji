from django.urls import path
from django.urls import include
from . import views
app_name = 'xxtj';
urlpatterns = [
    # path('', views.index, name='index'),
    # path('', views.index, name='index'),
    path('index/<int:class_id>/', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('result/', views.result, name='result'),
    path('ajax/', views.ajax, name='ajax'),
]