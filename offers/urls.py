from django.conf.urls import include
from django.urls import path, re_path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'offers', views.OfferViewSet)
router.register(r'materials', views.MaterialViewSet)
router.register(r'details', views.DetailViewSet)

urlpatterns = [
    re_path('^api/', include(router.urls)),
    path('test/', views.test, name='test'),
    path('', views.index_offer, name='offers'),
    path('create/', views.OfferCreateView.as_view(), name='offer-create'),
    path('<int:pk>/update/', views.OfferUpdateView.as_view(), name='offer-update'),
    path('<int:pk>/print/', views.offer_print_view, name='offer-print'),
    path('<int:pk>/details/', views.offer_detail_view, name='offer-details'),
    path('notices/', views.offer_notices_update, name='notices'),
    path('<int:pk>/details/create/', views.DetailCreateView.as_view(), name='detail-create'),
    path('<int:pk>/details/<int:det_pk>/update/', views.DetailUpdateView.as_view(), name='detail-update'),
    path('<int:pk>/details/<int:det_pk>/delete/', views.DetailDeleteView.as_view(), name='detail-delete'),
    path('details/', views.details_index, name='details-index'),
    path('details/searching/', views.details_searching, name='details-searching'),
    path('materials/', views.materials, name='materials'),
    path('materials/create/', views.MaterialCreateView.as_view(), name='material-create'),
    path('materials/<int:pk>/update/', views.MaterialUpdateView.as_view(), name='material-update'),


]
