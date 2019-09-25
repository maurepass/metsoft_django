from django.conf.urls import include
from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'offers', views.OfferViewSet)
router.register(r'materials', views.MaterialViewSet)
router.register(r'details', views.DetailViewSet)

urlpatterns = [
    re_path('^api/', include(router.urls)),
    path('test/', TemplateView.as_view(template_name='offers/test.html'), name='test'),
    path('', TemplateView.as_view(template_name='offers/index_offers.html'), name='offers'),
    path('create/', views.OfferCreateView.as_view(), name='offer-create'),
    path('<int:pk>/update/', views.OfferUpdateView.as_view(), name='offer-update'),
    path('<int:pk>/print/', views.OfferPrintView.as_view(), name='offer-print'),
    path('<int:pk>/details/', views.OfferDetailView.as_view(), name='offer-details'),
    path('notices/', views.OfferNoticesUpdateView.as_view(), name='notices'),
    path('<int:pk>/details/create/', views.DetailCreateView.as_view(), name='detail-create'),
    path('<int:pk>/details/<int:det_pk>/update/', views.DetailUpdateView.as_view(), name='detail-update'),
    path('<int:pk>/details/<int:det_pk>/delete/', views.DetailDeleteView.as_view(), name='detail-delete'),
    path('details/', TemplateView.as_view(template_name='offers/details_index.html'), name='details-index'),
    path('details/searching/', views.DetailSearchingView.as_view(), name='details-searching'),
    path('materials/', TemplateView.as_view(template_name='offers/material_list.html'), name='materials'),
    path('materials/create/', views.MaterialCreateView.as_view(), name='material-create'),
    path('materials/<int:pk>/update/', views.MaterialUpdateView.as_view(), name='material-update'),


]
