from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.views import generic
from rest_framework import viewsets

from .forms import PatternCreateForm, PatternReportForm, PatternUpdateForm
from .models import Pattern, PatternHistory, PatternStatus
from .serializers import PatternSerializers


class PatternCardView(generic.TemplateView):
    """ Showing history of status changes for the specific pattern"""
    template_name = 'patterns/pattern_card.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        pattern = Pattern.objects.get(pk=kwargs.get('pk'))
        context['pattern'] = pattern
        context['objects'] = pattern.patternhistory_set.all()
        return context


class PatternStatusChangeView(LoginRequiredMixin, PermissionRequiredMixin, generic.TemplateView):
    """ Quick changing of the pattern status by clicking the appropriate button. """
    permission_required = ['patterns.change_pattern']

    def dispatch(self, request, *args, **kwargs):
        pattern = Pattern.objects.get(pk=kwargs.get('pk'))
        statuses = PatternStatus.objects.all()

        if request.method == "POST":
            pattern.status = PatternStatus.objects.get(pk=request.POST.get('status'))
            pattern.move_in = date.today()
            pattern.save()
            last_status = PatternHistory.objects.last()
            if last_status.status != pattern.status:
                PatternHistory.objects.create(pattern=pattern, status=pattern.status, date=pattern.move_in)
            return redirect('/patterns/')

        context = {
            'pattern': pattern,
            'statuses': statuses,
        }
        return render(request, 'patterns/pattern_status_change.html', context)


class PatternReportFormView(generic.FormView):
    """ Generate a report included all patterns belonging to given customer """
    form_class = PatternReportForm()
    template_name = 'patterns/pattern_report_form.html'

    def post(self, request, *args, **kwargs):
        """ Preparing results from given data """
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


class PatternViewSet(viewsets.ModelViewSet):
    """ Show all patterns in database"""
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializers


class PatternCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    """ Adding new pattern to database """
    model = Pattern
    form_class = PatternCreateForm
    permission_required = ['patterns.add_pattern']


class PatternUpdateView(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    """ Changing the pattern data"""
    model = Pattern
    form_class = PatternUpdateForm
    permission_required = ['patterns.change_pattern']

    def dispatch(self, request, *args, **kwargs):
        """ If the pattern status is changed, add new status to the pattern history """
        if request.method == 'POST':
            pattern = Pattern.objects.get(pk=kwargs.get('pk'))
            new_status = PatternStatus.objects.get(pk=request.POST.get('status'))
            if pattern.status != new_status:
                move_in_date = request.POST.get('move_in')
                PatternHistory.objects.create(pattern=pattern, status=new_status, date=move_in_date)

        return super().dispatch(request, *args, **kwargs)
