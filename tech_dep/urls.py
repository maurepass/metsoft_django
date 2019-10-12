from django.urls import include, path, re_path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet, 'orders')

urlpatterns = [
    re_path('^api/', include(router.urls)),
    path('orders/', views.OrdersView.as_view(), name='orders-index'),
    path('<int:pk>/update/', views.OrderUpdateView.as_view(), name='order-update'),
]
