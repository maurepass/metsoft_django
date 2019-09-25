from django.urls import include, path, re_path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet, 'orders')

urlpatterns = [
    re_path('^api/', include(router.urls)),
    path('orders/', views.orders, name='orders-index'),
    path('<int:pk>/update/', views.OrderUpdateView.as_view(), name='order-update'),
]
