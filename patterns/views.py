from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.views.generic import CreateView, UpdateView
from rest_framework import viewsets

from .forms import PatternCreateForm, PatternReportForm, PatternUpdateForm
from .models import Pattern, PatternHistory, PatternStatus
from .serializers import PatternSerializers


def patterns_index(request):
    return render(request, 'patterns/patterns_index.html')


def pattern_card(request, pk):
    pattern = Pattern.objects.get(pk=pk)
    objects = pattern.patternhistory_set.all()
    context = {
        'pattern': pattern,
        'objects': objects,
    }
    return render(request, 'patterns/pattern_card.html', context)


def pattern_status_change(request, pk):
    pattern = Pattern.objects.get(pk=pk)
    if request.method == "POST":
        pattern.status = PatternStatus.objects.get(pk=request.POST.get('status'))
        pattern.move_in = date.today()
        pattern.save()
        last_status = PatternHistory.objects.last()
        if last_status.status != pattern.status:
            PatternHistory.objects.create(pattern=pattern, status=pattern.status, date=pattern.move_in)
        return redirect('/patterns/')

    statuses = PatternStatus.objects.all()
    context = {
        'pattern': pattern,
        'statuses': statuses,
    }
    return render(request, 'patterns/pattern_status_change.html', context)


def pattern_report(request):
    if request.method == "POST":
        patterns = (Pattern.objects
                    .filter(customer__icontains=request.POST.get('customer1'))
                    .exclude(status__in=[4, 5, 6, 7])
                    )
        total_area = patterns.aggregate(total_area=Sum('area'))
        customers = patterns.values('customer').distinct()

        context = {
            'objects': patterns,
            'total_area': total_area,
            'customers': customers,
        }
        return render(request, 'patterns/pattern_report_results.html', context)

    form = PatternReportForm()
    return render(request, 'patterns/pattern_report_form.html', {'form': form})


class PatternViewSet(viewsets.ModelViewSet):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializers


class PatternCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):

    model = Pattern
    form_class = PatternCreateForm
    permission_required = ['patterns.add_pattern']


class PatternUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Pattern
    form_class = PatternUpdateForm
    permission_required = ['patterns.change_pattern']

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            pattern = Pattern.objects.get(pk=kwargs.get('pk'))
            new_status = PatternStatus.objects.get(pk=request.POST.get('status'))
            if pattern.status != new_status:
                move_in_date = request.POST.get('move_in')
                PatternHistory.objects.create(pattern=pattern, status=new_status, date=move_in_date)

        return super().dispatch(request, *args, **kwargs)
