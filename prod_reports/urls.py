from django.urls import include, path, re_path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'non-destructive-testing', views.NonDestructiveTestingViewSet, 'non-destructive-testing')
router.register(r'casts-in-stock', views.CastsInStockViewSet, 'casts-in-stock')
router.register(r'nonconformity', views.NonconformityViewSet, 'nonconformity')
router.register(r'finished', views.FinishedViewSet, 'finished')
router.register(r'remarks', views.RemarksViewSet, 'remarks')
router.register(r'casting-weights', views.CastingWeightsViewSet, 'casting-weights')
router.register(r'molding', views.MoldingViewSet, 'molding')
router.register(r'machining', views.MachiningViewSet, 'machining')
router.register(r'scraps', views.ScrapsViewSet, 'scraps')
router.register(r'yields', views.YieldsViewSet, 'yields')
router.register(r'pouring', views.PouringViewSet, 'pouring')
router.register(r'castings-with-machining', views.CastsWithMachiningViewSet, 'castings-with-machining')

urlpatterns = [
    re_path('^api/', include(router.urls)),
    path('execution-time/', views.execution_time, name='execution-time'),
    path('finished/', views.finished, name='finished'),
    path('pouring/', views.pouring, name='pouring'),
    path('nonconformity/', views.nonconformity, name='nonconformity'),
    path('remarks/', views.remarks, name='remarks'),
    path('weight-per-client/', views.weight_per_client, name='weight-per-client'),
    path('weight-per-group/', views.weight_per_group, name='weight-per-group'),
    path('scraps/', views.scraps, name='scraps'),
    path('casting-weights/', views.casting_weights, name='casting-weights'),
    path('monitoring-in-work/', views.monitoring_in_work, name='monitoring-in-work'),
    path('monitoring-all/', views.monitoring_all, name='monitoring-all'),
    path('casts-in-stock/', views.casts_in_stock, name='casts-in-stock'),
    path('molding/', views.molding, name='molding'),
    path('non-destructive-testing/', views.non_destructive_testing, name='non-destructive-testing'),
    path('machining/', views.machining, name='machining'),
    path('yields/', views.yields, name='yields'),
    path('inserted-data/', views.inserted_data, name='inserted-data'),
    path('reports_list/', views.reports, name='reports-list'),
    path('castings-with-machining/', views.casts_with_machining, name='castings-with-machining'),
]
