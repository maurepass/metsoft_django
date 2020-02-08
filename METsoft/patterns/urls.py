from django.conf.urls import include
from django.urls import path, re_path
from django.views.generic import TemplateView
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'patterns', views.PatternViewSet)

app_name = 'patterns'
urlpatterns = [
    re_path('^api/', include(router.urls)),
    path('', TemplateView.as_view(template_name='patterns/patterns_index.html'), name='patterns'),
    path('<int:pk>/', views.PatternCardView.as_view(), name='pattern-card'),
    path('<int:pk>/edit', views.PatternUpdateView.as_view(), name='pattern-edit'),
    path('create/', views.PatternCreateView.as_view(), name='pattern-create'),
    path('<int:pk>/status/', views.PatternStatusChangeView.as_view(), name='pattern-status-change'),
    path('report/', views.PatternReportFormView.as_view(), name="pattern-report"),
]
