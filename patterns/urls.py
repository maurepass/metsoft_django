from django.conf.urls import include
from django.urls import path, re_path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'patterns', views.PatternViewSet)

app_name = 'patterns'
urlpatterns = [
    re_path('^api/', include(router.urls)),
    path('', views.patterns_index, name='patterns'),
    path('<int:pk>/', views.pattern_card, name='pattern-card'),
    path('<int:pk>/edit', views.PatternUpdateView.as_view(), name='pattern-edit'),
    path('create/', views.PatternCreateView.as_view(), name='pattern-create'),
    path('<int:pk>/status/', views.pattern_status_change, name='pattern-status-change'),
    path('report/', views.pattern_report, name="pattern-report"),
]
