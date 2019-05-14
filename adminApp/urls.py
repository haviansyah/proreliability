from django.urls import path

from . import views

urlpatterns =[
    path('',views.index, name='Index'),
    path('post/', views.insert, name='Insert'),
    path('show/', views.get_report, name='SHOW'),
    path('test/', views.testing, name='test'),
    path('laporan/', views.api_get_laporan),
    path('equipment/', views.api_get_equipment),
    path('header/', views.api_get_header),
    path('unit/', views.api_get_unit),
    path('trend/', views.api_get_trend ),
    path('condition/', views.api_get_condition),
]