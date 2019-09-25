from django.urls import include, path, re_path
from django.views.generic import TemplateView
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
    path('execution-time/', views.ExecutionTimeView.as_view(), name='execution-time'),
    path('finished/', TemplateView.as_view(template_name='prod_reports/finished.html'), name='finished'),
    path('pouring/', TemplateView.as_view(template_name='prod_reports/pouring.html'), name='pouring'),
    path('nonconformity/', TemplateView.as_view(template_name='prod_reports/nonconformity.html'), name='nonconformity'),
    path('remarks/', TemplateView.as_view(template_name='prod_reports/remarks.html'), name='remarks'),
    path('weight-per-client/', views.WeightPerClientView.as_view(), name='weight-per-client'),
    path('weight-per-group/', views.WeightPerGroupView.as_view(), name='weight-per-group'),
    path('scraps/', TemplateView.as_view(template_name='prod_reports/scraps.html'), name='scraps'),
    path('casting-weights/', TemplateView.as_view(template_name='prod_reports/casting_weights.html'), name='casting-weights'),
    path('monitoring-in-work/', views.MonitoringInWorkList.as_view(), name='monitoring-in-work'),
    path('monitoring-all/', views.MonitoringAllList.as_view(), name='monitoring-all'),
    path('casts-in-stock/', TemplateView.as_view(template_name='prod_reports/casts_in_stock.html'), name='casts-in-stock'),
    path('molding/', TemplateView.as_view(template_name='prod_reports/molding.html'), name='molding'),
    path('non-destructive-testing/', TemplateView.as_view(template_name='prod_reports/non_destructive_testing.html'), name='non-destructive-testing'),
    path('machining/', TemplateView.as_view(template_name='prod_reports/machining.html'), name='machining'),
    path('yields/', TemplateView.as_view(template_name='prod_reports/yields.html'), name='yields'),
    path('inserted-data/', views.InsertedDataList.as_view(), name='inserted-data'),
    path('reports/', TemplateView.as_view(template_name='prod_reports/reports_list.html'), name='reports-list'),
    path('castings-with-machining/', TemplateView.as_view(template_name='prod_reports/casts_with_machining.html'), name='castings-with-machining'),
]
