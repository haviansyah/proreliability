from django.urls import path

from . import views

urlpatterns =[
    path('',views.index, name='Index'),
    path('post/', views.insert, name='Insert'),
    path('uploadAW/', views.insert_asset_wellness, name='Insert AssetWellness'),
    path('getAW/', views.api_get_assetwellness_rekap, name='Get AssetWellness'),
    path('getAW/<unit>', views.api_get_assetwellness_unit, name='Get AssetWellness Unit'),
    path('getAW/report/<int:id>', views.get_assetwellness_report, name='Get AssetWellness Report'),
    path('show/', views.get_report, name='SHOW'),
    path('test/', views.testing, name='test'),
    path('laporan/', views.api_get_laporan),
    path('equipment/', views.api_get_equipment),
    path('header/', views.api_get_header),
    path('unit/', views.api_get_unit),
    path('trend/', views.api_get_trend ),
    path('condition/', views.api_get_condition),
    path('detail/', views.api_get_detail_equipment),
    path('download/', views.api_download_unit_rekap),
    path('dcs/',views.api_get_dcs_realtime, name='DCS REALTIME'),
    path('hapus/',views.api_get_hapus_unit, name='hapus unit'),
    path('dcs/tag',views.api_get_dcs_realtime_tag, name='GET TAG DCS'),
    path('dcs/val', views.api_get_dcs_realtime_val, name='GET VAL DCS'),
    path('dcs/warning', views.api_get_dcs_warning, name='GET WARN DCS'),

]