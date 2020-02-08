from django.shortcuts import render, redirect

from rest_framework import viewsets

from METsoft_root.users.models import UsedViewsLogs
from METsoft_root.users.serializers import LogSerializer


def base(request):
    return render(request, 'offers/base.html')


def redirect_after_login(request):
    if request.user.id == 25:
        return redirect('patterns:patterns')
    else:
        return redirect('offers')


class LogsViewSet(viewsets.ModelViewSet):
    queryset = UsedViewsLogs.objects.all().order_by('-id')
    serializer_class = LogSerializer
