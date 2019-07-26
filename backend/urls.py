from django.urls import path
from . import views
from django.conf.urls import url,include

# SET THE NAMESPACE!
app_name = 'backend'


urlpatterns = [
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^test/$', views.test, name='test'),
    path('condition/<int:id>/', views.condition,name='condition_page'),
    path('assetwellness/', views.asset_wellness_all,name='assetwellness_page'),
    path('assetwellness/<unit>', views.asset_wellness_unit,name='assetwellness_unit_page'),
    path('unit/<int:kondisi_id>/<int:unit_id>/', views.unit, name='unit_page'),
    path('trend/<int:id>/', views.trend, name='trend_page'),
    path('dcs/', views.dcs_realtime, name='dcs_page'),

]