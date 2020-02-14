from django.urls import path

from . import views

app_name = 'advance'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('', views.index, name='index'),
    path('cla_inf/', views.cla_inf, name='cla_inf'),
    path('add_cla/', views.add_cla, name='add_cla'),
    path('del_cla/', views.del_cla, name='del_cla'),
    path('edit_cla/', views.edit_cla, name='edit_cla'),
    path('stu_inf/', views.stu_inf, name='stu_inf'),
    path('add_stu/', views.add_stu, name='add_stu'),
    path('del_stu/', views.del_stu, name='del_stu'),
    path('edit_stu/', views.edit_stu, name='edit_stu'),
    path('sta_inf/', views.sta_inf, name='sta_inf'),
    path('add_sta/', views.add_sta, name='add_sta'),
    path('del_sta/', views.del_sta, name='del_sta'),
    path('edit_sta/', views.edit_sta, name='edit_sta'),
    # path('adm_ind/', views.adm_ind, name='adm_inf'),
    path('personal/', views.personal, name='personal'),
    path('change_password', views.change_password, name='change_password'),
    path('ajax/', views.ajax, name='ajax')
]
