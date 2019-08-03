from django.urls import include, path, re_path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'badania-ndt', views.BadaniaNDTViewSet, 'badania-ndt')
router.register(r'magazyn', views.MagazynViewSet, 'magazyn')
router.register(r'niezgodnosci', views.NiezgodnosciViewSet, 'niezgodnosci')
router.register(r'odbiory', views.OdbioryViewSet, 'odbiory')
router.register(r'uwagi', views.UwagiViewSet, 'uwagi')
router.register(r'wagi-odlewow', views.WagiOdlewowViewSet, 'wagi-odlewow')
router.register(r'zaformowane', views.ZaformowaniaViewSet, 'zaformowane')
router.register(r'machining', views.MachiningViewSet, 'machining')
router.register(r'wybraki', views.WybrakiViewSet, 'wybraki')
router.register(r'uzyski', views.UzyskiViewSet, 'uzyski')
router.register(r'zalania', views.ZalaniaViewSet, 'zalania')

urlpatterns = [
    re_path('^api/', include(router.urls)),
    path('czas-wykonania/', views.czas_wykonania, name='czas-wykonania'),
    path('odbiory/', views.odbiory, name='odbiory'),
    path('zalania/', views.zalania, name='zalania'),
    path('niezgodnosci/', views.niezgodnosci, name='niezgodnosci'),
    path('uwagi/', views.uwagi, name='uwagi'),
    path('weight-per-client/', views.weight_per_client, name='weight-per-client'),
    path('weight-per-group/', views.weight_per_group, name='weight-per-group'),
    path('wybraki/', views.wybraki, name='wybraki'),
    path('wagi-odlewow/', views.wagi_odlewow, name='wagi-odlewow'),
    path('monitoring-in-work/', views.monitoring_in_work, name='monitoring-in-work'),
    path('monitoring-all/', views.monitoring_all, name='monitoring-all'),
    path('magazyn/', views.magazyn, name='magazyn'),
    path('zaformowane/', views.zaformowania, name='zaformowane'),
    path('badania-ndt/', views.badania_ndt, name='badania-ndt'),
    path('machining/', views.machining, name='machining'),
    path('uzyski/', views.uzyski, name='uzyski'),
    path('inserted-data/', views.inserted_data, name='inserted-data'),
]
