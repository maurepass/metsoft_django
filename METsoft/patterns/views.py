from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Sum
from django.shortcuts import render
from django.views import generic
from rest_framework import viewsets

from .forms import PatternCreateForm, PatternReportForm, PatternUpdateForm
from .models import Pattern, PatternStatus
from .serializers import PatternSerializers


class PatternCardView(generic.DetailView):
    """ Showing history of status changes for the specific pattern"""

    model = Pattern
    template_name = "patterns/pattern_card.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["objects"] = self.object.patternhistory_set.all()
        return context


class PatternStatusChangeView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView
):
    """ Quick changing of the pattern status by clicking the appropriate button. """

    model = Pattern
    template_name = "patterns/pattern_status_change.html"
    permission_required = ["patterns.change_pattern"]
    fields = ["status"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Not possible to set status "Brak weryfikacji"
        context["statuses"] = PatternStatus.objects.all().exclude(pk=8)
        return context

    def get_success_url(self):
        """ If the pattern status is changed, add new status to the pattern history """
        Pattern.if_status_changed_update_history(self.object)
        return super().get_success_url()


class PatternReportFormView(generic.FormView):
    """ Generate a report included all patterns belonging to given customer """

    form_class = PatternReportForm
    template_name = "patterns/pattern_report_form.html"

    def post(self, request, *args, **kwargs):
        """ Preparing results from given data """
        patterns = Pattern.objects.filter(
            customer__icontains=request.POST.get("customer1")
        ).exclude(status__in=[4, 5, 6, 8])
        total_area = patterns.aggregate(total_area=Sum("area"))
        customers = patterns.values("customer").distinct()

        context = {
            "objects": patterns,
            "total_area": total_area,
            "customers": customers,
        }
        return render(request, "patterns/pattern_report_results.html", context)


class PatternViewSet(viewsets.ReadOnlyModelViewSet):
    """ Show all patterns in database"""

    queryset = Pattern.objects.all().order_by("-id")
    serializer_class = PatternSerializers


class PatternCreateView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView
):
    """ Adding new pattern to database """

    model = Pattern
    form_class = PatternCreateForm
    permission_required = ["patterns.add_pattern"]

    def get_success_url(self):
        """ Add record with initial status to the pattern history"""
        Pattern.add_status_to_pattern_history(self.object)
        return super().get_success_url()


class PatternUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView
):
    """ Changing the pattern data"""

    model = Pattern
    form_class = PatternUpdateForm
    permission_required = ["patterns.change_pattern"]

    def get_success_url(self):
        """ If the pattern status is changed, add new status to the pattern history """
        Pattern.if_status_changed_update_history(self.object)
        return super().get_success_url()
